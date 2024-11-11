import logging
import os
import requests
from pathlib import Path
from typing import List, Optional

import app.crud.rule as crud_rule
from app.api import dependencies
from app.expert.expert_base import ExpertBase
from app.expert.parsers.bhrgt_parser import BHRGT_Parser
from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.parsers.gar_parser import GAR_Parser
from app.expert.parsers.gld_parser import GLD_Parser
from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.parsers.xml_parser import XmlParser
from app.expert.report_generators.rws_report_generator import RwsReportGenerator
from app.expert.rules._superrule import superRule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExpertRws(ExpertBase):
    def __init__(self):
        super().__init__()
        self.rule_path = Path(__file__).parent / "rules"
        self.parsers = self.__register_parsers()
        self.rules = self.__register_rules()

    def __register_parsers(self) -> List[XmlParser]:
        """
        Register the document parsers to be used by the expert.
        BHRGT = BoreholeResearch-Geotechnics
        CPT = ConePenetrometerTest
        GAR = GroundwaterAnalysisReport
        GLD = GroundwaterLevelDossier
        GMW = GroundwaterMonitoringWell

        Returns list of parser objects
        """
        return [BHRGT_Parser, CPT_Parser, GAR_Parser, GLD_Parser, GMW_Parser]

    def __register_rules(self) -> List[superRule]:
        """
        Registers the defined rules by fetching all available rules from the processor service.

        Returns the found set of rule class objects.
        """
        processor_url = os.getenv("PROCESSOR_URL", "http://localhost:8006/api")
        if processor_url is None:
            raise ValueError("Processor URL not set.")
        rules = []
        response = requests.get(f"{processor_url}/rule/")
        response.raise_for_status()
        for rule in response.json():
            rules.append(
                superRule(
                    code=rule["code"],
                    name=rule["name"],
                    object_type=rule["object_type"],
                    importance=1,
                    feedbackMessage=rule["feedback_message"],
                    explanation=rule["explanation"],
                    docstring=rule["docstring"],
                )
            )
        return rules

    def _find_parser_for_document(self, document) -> Optional[XmlParser]:
        """
        Matches the experts known parsers against the given document.
        Returns the parser fit to handle the document.

        Returns a fitting parser, if one is known.
        """
        valid_parsers = [
            p.from_string(str.encode(document))
            for p in self.parsers
            if p.from_string(str.encode(document)).is_of_type()
        ]
        if len(valid_parsers) == 1:
            return valid_parsers[0]
        return None

    def __validate_document(self, document_blob: str, document_name: str) -> List:
        """
        Validates a single document. First the objecttype is determined by matching a parser.
        When the object type is known, applicable rules for that type are selected and applied.

        Returns: List of findings
        """
        findings = []
        parser = self._find_parser_for_document(document_blob)
        if parser is not None:
            with next(dependencies.get_db()) as db:
                applicable_rules = [
                    r()
                    for r in self.rules
                    if (
                        r.object_type == parser.get_object_type()
                        or r.object_type == "GEN"
                    )
                    and crud_rule.get_enabled_state_of_rule(
                        db=db,
                        rule_id=str(r.code),
                        object_type=r.object_type,
                    )
                ]
            for rule in applicable_rules:
                result = rule.applyRule(parser)
                findings.append(
                    {
                        "result": result == None,  # noqa: E711
                        "feedbackMessage": result,
                        "ruleId": rule.getCode(),
                        "objectType": rule.getObjectType(),
                    }
                )
            return findings
        else:
            print(
                f"Skipping document since no valid parser has been found for: {document_name}."
            )
            return []

    async def validate_documents(self, documents: List) -> List:
        """
        Validates a list of documents.

        Returns: List of findings.
        """
        findings = []
        for document in documents:
            file_name = document.filename
            file_content = str(document.file.read(), "utf-8")

            try:
                document_findings = self.__validate_document(file_content, file_name)
                if document_findings:
                    findings.append(
                        {"filename": file_name, "findings": document_findings}
                    )
            except Exception as e:
                logger.warning(
                    f"Exception occurred during the handling of document {file_name}"
                )
                logger.warning(e)
        return findings

    def handle_bhp_document(self, document: str, file_name: str) -> List:
        """
        Handles a singular document in the format as given when downloaded from the bronhouder portal.

        Returns: List of findings
        """
        try:
            findings = self.__validate_document(document, file_name)
        except Exception as e:
            findings = []
            logger.warning(
                f"Exception occured during the handling of document {file_name}"
            )
            logger.warning(e)
        return findings

    def generate_report(self, batch_id: str, data, historicaldata=None) -> str:
        """
        Generates a report for the given batch. Set historicaldata to None and dont pass it to report generator since we dont use
        historical data in RWS reports.

        Returns: generated filename.
        """
        generator = RwsReportGenerator(batch_id=batch_id, data=data)
        return generator.fileName

    def scan_and_validate_documents(self) -> None:
        """Needed because of superclass but wont be used for this expert."""
        raise NotImplementedError
