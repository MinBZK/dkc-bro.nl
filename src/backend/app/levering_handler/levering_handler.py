import logging
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List

from dotenv import load_dotenv
from requests.sessions import Session

import app.crud.batch as crud_batch
import app.crud.finding as crud_finding
import app.crud.log_poller as crud_log_poller
import app.crud.project as crud_project
import app.crud.rule as crud_rule
import app.enums as enums
from app import schemas
from app.api import dependencies
from app.expert.expert_rws import ExpertRws
from app.levering_handler.utils import (
    construct_summary_string,
    count_errors_in_violations,
    count_warnings_in_violations,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class Logger(Enum):
    STARTING_BHP_POLL = "Starting bhp poll"
    FINISHING_BHP_POLL = "Finished bhp poll"


class LeveringHandler:
    def __init__(self):
        """
        Creates an instance of the levering handler.
        """
        self.bhp_api_url = os.environ.get("BHP-ENDPOINT", "")
        self.bhp_session = Session()
        self.bhp_session.auth = (
            os.environ.get("BHP-USERNAME", ""),
            os.environ.get("BHP-TOKEN", ""),
        )
        self.rules = self.__init_rule_dict()

    def __init_rule_dict(self) -> Dict:
        """
        Initializes an in memory dictionary containing all known rules to prevent unnecessary DB calls.

        Returns: Dict containing all rules with as key a combination of object_type and id.
        """
        with next(dependencies.get_db()) as db:
            return {
                f"{rule.object_type}-{rule.id}": rule
                for rule in crud_rule.get_rules(db=db)
            }

    def __post_pdf_report_to_levering(
        self, db: Session, batch_id: str, project_nr: int, report_bytes: bytes
    ) -> None:
        """
        Posts a generated pdf report containing findings to the levering in BHP with the given id.

        Returns: None
        """
        try:
            self.bhp_session.post(
                url=f"{self.bhp_api_url}/{project_nr}/leveringen/{batch_id}/attachments/{batch_id}-rapportage.pdf",
                data=report_bytes,
            )
            logger.info(f"Posted report to levering in BHP with id {batch_id}")
        except Exception as e:
            logger.warning(
                f"Failed posting document to levering due to an exception: {e}"
            )

    def __post_finding_summary_to_levering(
        self, levering_id: int, project_nr: int, violations: List
    ) -> None:
        """
        Posts a finding on levering level to BHP containing a summary of found violations.
        """
        warnings = count_warnings_in_violations(self.rules, violations)
        errors = count_errors_in_violations(self.rules, violations)
        if errors > 0:
            endpoint = "errors"
        elif warnings > 0:
            endpoint = "warnings"
        else:
            endpoint = "info"
        url = f"{self.bhp_api_url}/{project_nr}/leveringen/{levering_id}/{endpoint}"
        message = construct_summary_string(errors, warnings)
        try:
            self.bhp_session.post(
                url, data=message, headers={"Content-Type": "text/plain"}
            )
            logger.info(
                f"Posted summary to levering in BHP with project nr {project_nr} and levering id {levering_id}"
            )
        except Exception as e:
            logger.warning(
                f"Failed posting verrijking to levering due to an exception: {e}"
            )

    def __post_finding_to_brondocument(
        self,
        brondocument_id: int,
        project_nr: int,
        finding,
        importance: enums.Importance,
    ) -> None:
        """
        Posts a finding message to a brondocument with the given brondocument id.
        Depending on the importance of the finding, a different endpoint is called.

        Returns: None
        """
        url = f"{self.bhp_api_url}/{project_nr}/brondocumenten/{brondocument_id}/"
        if importance == enums.Importance.INFO:
            logger.info(
                f"INFO level finding reported for document {brondocument_id}. Will not post to BHP."
            )
            return
        elif importance == enums.Importance.WARNING:
            url += "warnings"
        elif importance == enums.Importance.ERROR:
            url += "errors"
        try:
            self.bhp_session.post(
                url, data=str(finding), headers={"Content-Type": "text/plain"}
            )
            logger.info(
                f"Posted {str(importance)} finding to document in BHP with id {brondocument_id}"
            )
        except Exception as e:
            logger.warning(
                f"Failed posting verrijking to document due to an exception: {e}"
            )

    def __get_brondocument(self, brondocument_id: int, project_nr: int) -> str:
        """
        Gets the content of a brondocument from the bronhouder portaal by given brondocument id.

        Returns: String content of the xml brondocument.
        """
        try:
            response = self.bhp_session.get(
                f"{self.bhp_api_url}/{project_nr}/brondocumenten/{brondocument_id}"
            )
            return str(response.content, "utf-8")
        except Exception as e:
            logger.warning(f"Could not get brondocument due to an exception: {e}")
            return []

    def __get_levering_documents(self, levering_id: int, project_nr: int) -> List:
        """
        Gets a list of brondocument info belonging to a levering with the given levering id.

        Returns: List of brondocument objects from bronhouder portaal.
        """
        try:
            response = self.bhp_session.get(
                f"{self.bhp_api_url}/{project_nr}/leveringen/{levering_id}"
            )
            return response.json().get("brondocuments")
        except Exception as e:
            logger.warning(f"Could not get levering documents due to an exception: {e}")
            return []

    def __retrieve_save_project_nrs(self, db: Session):
        """
        Retrieves project numbers from the BHP API and saves them to the database.

        Returns: None
        """
        response = self.bhp_session.get(url=f"{self.bhp_api_url}/projecten")
        projects = response.json()
        [
            (
                crud_project.create_project_nrs(
                    db=db,
                    project_id=project.get("projectId"),
                    project_name=project.get("projectNaam"),
                    source_holder=project.get("bronhouder").get("naam"),
                    closed=project.get("closed"),
                )
            )
            for project in projects
        ]
        return projects

    def __get_project_nrs(self, db: Session) -> List:
        """
        Gets all project numbers from the bronhouder portaal belonging to the current token.

        Returns: List of project numbers
        """
        return [
            project_nr.project_nr for project_nr in crud_project.get_project_nrs(db=db)
        ]

    def __get_leveringen(self, db: Session) -> dict[str, List]:
        """
        Gets all leveringen from the bronhouder portaal belonging to the current token and with current action CONTROLEREN.

        Returns: List of levering ids to be checked by the expert
        """
        self.__retrieve_save_project_nrs(db=db)
        project_nr_active = self.__get_project_nrs(db=db)
        project_with_levering_ids = {}

        for project_nr in project_nr_active:
            url = f"{self.bhp_api_url}/{project_nr}/leveringen?actie=CONTROLEREN"
            response = self.bhp_session.get(url=url)
            if response.status_code == 200:
                if response.json():
                    project_with_levering_ids[project_nr] = response.json()
            elif response.status_code == 403:
                logger.warning(
                    f"The token is not authorized to access the leveringen for this project_nr: {project_nr}"
                )
            elif response.status_code == 404:
                logger.warning(f"Found no leveringen for this project_nr: {project_nr}")
            else:
                crud_log_poller.create_log_poller(
                    db=db,
                    request_url=url,
                    request_status_code=response.status_code,
                    log_message=f"Found no leveringen due to an error: {response.status_code} : {response.reason}",
                )
                Session().close()
                return {}
        return project_with_levering_ids

    def __handle_finding(
        self, db: Session, levering_id: int, project_nr: int, brondocument, finding
    ) -> None:
        """
        Handles a single finding. Gets the importance of the rule belonging to the finding from the db.
        Posts the finding to the expert service database.
        If the rule is a violation, post the finding to the endpoint of the correct level in the bronhouder portaal.

        Returns: None
        """
        importance = enums.Importance(
            self.rules[
                finding.get("objectType") + "-" + str(finding.get("ruleId"))
            ].importance
        )
        findingCreate = schemas.finding.FindingCreate(
            result=finding.get("result"),
            feedbackMessage=finding.get("feedbackMessage"),
            timestamp=datetime.now(),
            filename=brondocument.get("filename"),
            batch_id=levering_id,
        )
        crud_finding.create_rule_finding(
            db=db,
            finding=findingCreate,
            rule_id=finding.get("ruleId"),
            rule_object_type=finding.get("objectType"),
            project_nr=project_nr,
        )
        if not finding.get("result"):
            self.__post_finding_to_brondocument(
                brondocument_id=brondocument.get("id"),
                project_nr=project_nr,
                finding=finding.get("feedbackMessage"),
                importance=importance,
            )

    def __handle_brondocument(
        self,
        expert: ExpertRws,
        db: Session,
        levering_id: int,
        project_nr: int,
        brondocument,
    ) -> List:
        """
        Handles one brondocument from a levering. Downloads the file from the bronhouder portaal and use the expert to get a list of findings.
        These findings are later handled and posted to the bronhouder portaal if they contain violations.

        Returns: Found violations in this document
        """
        brondocument_blob = self.__get_brondocument(
            brondocument.get("id"), project_nr=project_nr
        )
        try:
            findings = expert.handle_bhp_document(
                brondocument_blob, brondocument.get("filename")
            )
            for finding in findings:
                self.__handle_finding(
                    db=db,
                    levering_id=levering_id,
                    project_nr=project_nr,
                    brondocument=brondocument,
                    finding=finding,
                )
            violations = [
                f
                for f in findings
                if not f.get("result")
                and self.rules[
                    f.get("objectType") + "-" + str(f.get("ruleId"))
                ].importance
                > 1
            ]
            return violations
        except Exception as e:
            file_name = brondocument.get("filename", "bestand")
            logger.warning(
                f"Failed to analyze brondocument {file_name} with exception: {e}. Skipping brondocument."
            )

    def __handle_levering(
        self,
        expert: ExpertRws,
        db: Session,
        levering_id: int,
        brondocuments: list,
        project_nr: int,
    ) -> int:
        """
        Handles one levering. Creates a batch object in the database if it does not exist yet.
        If one does exist, this levering already has been checked and we can return.
        For new leveringen, all brondocumenten are imported and checked by the expert.

        Returns: Number of violations in this levering.
        """
        new_batch = crud_batch.create_batch_if_not_exists(
            db=db, batch=schemas.batch.BatchCreate(id=levering_id)
        )
        if new_batch is None:
            logger.info(
                f"Skipping levering {levering_id} from project nr {project_nr} since it already has been processed."
            )
            return
        violations = []
        for brondocument in brondocuments:
            violations += self.__handle_brondocument(
                expert=expert,
                db=db,
                levering_id=levering_id,
                brondocument=brondocument,
                project_nr=project_nr,
            )
        logger.info(
            f"Posting summary for levering {levering_id} from project nr {project_nr}. Found {len(violations)} violations."
        )
        self.__post_finding_summary_to_levering(
            levering_id=levering_id, project_nr=project_nr, violations=violations
        )
        logger.info(
            f"Done handling levering {levering_id} from project nr {project_nr}."
        )
        return len(violations)

    def __get_levering_document_dict(self, db: Session) -> dict:
        """
        Genarates a dictionary of leveringId-[brondocument] pairs based on the current token.
        Filters out leveringen that are already handled by the expert, validated by checking the batch database.

        Returns: dict with leveringIds as keys and lists of brondocuments in that levering as a value.
        """
        project_with_levering_ids = self.__get_leveringen(db=db)
        levering_ids = [
            levering_id
            for _, levering_id_list in project_with_levering_ids.items()
            for levering_id in levering_id_list
        ]
        filtered_levering_ids = list(
            filter(
                lambda levering_id: not crud_batch.get_existance_of_batch(
                    db=db, batch_id=levering_id
                ),
                levering_ids,
            )
        )
        project_with_filtered_levering_ids = {
            project: [
                levering_id
                for levering_id in levering_ids
                if levering_id in filtered_levering_ids
            ]
            for project, levering_ids in project_with_levering_ids.items()
        }

        logger.info(
            f"Found {len(levering_ids)} leveringen in bronhouderportaal with status 'CONTROLEREN', of which {len(filtered_levering_ids)} have not been checked yet."
        )
        if len(filtered_levering_ids) > 0:
            logger.info(
                "Retrieving documents for all leveringen from bronhouderportaal."
            )
        return {
            project_nr: {
                levering_id: self.__get_levering_documents(
                    levering_id=levering_id, project_nr=project_nr
                )
            }
            for project_nr, levering_id_list in project_with_filtered_levering_ids.items()
            for levering_id in levering_id_list
        }

    def poll_and_handle_leveringen(self) -> None:
        """
        Polls the bronhouder-portaal for leveringen belonging to the handlers token.
        All found leveringen and its containing documents are checked by the expert and findings are posted
        as verrijkingen if rules are violated.

        Returns: None
        """
        logger.info(f"{Logger.STARTING_BHP_POLL.value}")
        with next(dependencies.get_db()) as db:
            expert = ExpertRws()
            leveringen_document_dict = self.__get_levering_document_dict(db=db)
            for project_nr, levering_brondocument in leveringen_document_dict.items():
                for levering_id, brondocuments in levering_brondocument.items():
                    violations = self.__handle_levering(
                        expert=expert,
                        db=db,
                        levering_id=levering_id,
                        brondocuments=brondocuments,
                        project_nr=project_nr,
                    )
                    report_data = crud_finding.get_findings_per_document_by_batch_id(
                        db=db, batch_id=levering_id
                    )
                    if violations == 0:
                        logger.info(
                            f"No violations found in levering {levering_id} from project nr {project_nr}. Will not generate report."
                        )
                        continue
                    report = expert.generate_report(
                        batch_id=levering_id, data=report_data
                    )
                    with open(report, "rb") as report_file:
                        self.__post_pdf_report_to_levering(
                            db=db,
                            batch_id=levering_id,
                            project_nr=project_nr,
                            report_bytes=report_file.read(),
                        )
                    os.unlink(report)
            crud_log_poller.create_log_poller(
                db=db,
                request_url=self.bhp_api_url,
                request_status_code=200,
                log_message=Logger.FINISHING_BHP_POLL.value,
            )
            logger.info(f"{Logger.FINISHING_BHP_POLL.value}")
