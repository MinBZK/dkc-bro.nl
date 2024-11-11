import io
import logging
import os
from datetime import datetime
from typing import List, Optional
from zipfile import ZipFile

import httpx
from fastapi import UploadFile, File, Depends, HTTPException, APIRouter, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import schemas, models, crud
import app.app_factory as af
from app.api import dependencies
from app.crud import rule as crud_rule, batch as crud_batch, finding as crud_finding
from app.expert.expert_base import ExpertBase
from app.expert.expert_rws import ExpertRws
from app.expert.report_generators import batch_report_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def _check_project(db, org_id, project_nr):
    project = (
        db.query(models.Project)
        .filter(models.Project.project_nr == project_nr)
        .filter(models.Project.org_id == org_id)
        .all()
    )
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Er is geen project met projectnummer {project_nr} gevonden voor uw organisatie.",
        )


def _get_org(db, org_code):
    org = (
        db.query(models.Organization)
        .filter(models.Organization.code == org_code)
        .one_or_none()
    )
    if not org:
        raise HTTPException(
            status_code=404,
            detail=f"Er is geen organisatie met code {org_code} gevonden.",
        )
    return org


async def __handle_results(db, document, levering_id, project_nr, rule, rule_result):
    finding = schemas.RuleResult(
        document=document.filename,
        rule=rule.id + rule.object_type,
        result=rule_result,
        importance=rule.importance,
    )
    findingCreate = schemas.finding.FindingCreate(
        result=finding.result["passed"],
        feedbackMessage=finding.result["feedback_message"],
        timestamp=datetime.now(),
        filename=document.filename,
        batch_id=levering_id,
    )
    crud_finding.create_rule_finding(
        db=db,
        finding=findingCreate,
        rule_id=rule.id,
        rule_object_type=rule.object_type,
        project_nr=project_nr,
        auto_commit=False,
    )


def _update_project(
    org_id: int,
    project_nr: int,
    project_name: Optional[str] = "",
    bronhouder_naam: Optional[str] = "",
    project_closed: Optional[bool] = False,
    db: Session = Depends(dependencies.get_db),
) -> None:
    crud.project.create_project_nrs(
        db=db,
        org_id=org_id,
        project_id=project_nr,
        project_name=project_name,
        source_holder=bronhouder_naam,
        closed=project_closed,
    )


@router.get("/project-nrs", response_model=List[int])
async def get_project_nrs(
    org_code: str,
    db: Session = Depends(dependencies.get_db)
) -> List[int]:
    """
    Get all project numbers
    """
    org = _get_org(db, org_code)
    return crud.project.get_project_nrs(db=db, org_id=org.id)


@router.get("/batch-ids")
async def get_batch_ids(
    org_code: str,
    db: Session = Depends(dependencies.get_db)
) -> List:
    """
    Returns: batches
    """
    org = _get_org(db, org_code)
    return crud_batch.get_all_batch_ids(db=db, org_id=org.id)


@router.post("/process-xml", response_model=schemas.ProcessXMLResponse)
async def process_xml(
    org_code: str = Form(...),
    levering_id: Optional[str] = Form(None),
    project_nr: Optional[int] = Form(None),
    project_naam: Optional[str] = Form(None),
    project_closed: Optional[bool] = Form(False),
    bronhouder_naam: Optional[str] = Form(None),
    documents: List[UploadFile] = File(...),
    db: Session = Depends(dependencies.get_db),
):
    org = _get_org(db, org_code)
    if isinstance(levering_id, str) and isinstance(project_nr, int):
        _update_project(org.id, project_nr, project_naam, bronhouder_naam, project_closed, db)
        _check_project(db, org.id, project_nr)

    unzipped_documents = []
    # Unzip documents if necessary
    for document in documents:
        if document.content_type in ["application/zip", "application/x-zip-compressed"]:
            with ZipFile(io.BytesIO(document.file.read()), "r") as zip_file:
                for item in zip_file.namelist():
                    file = zip_file.open(item)
                    unzipped_documents.append(UploadFile(filename=file.name, file=file))
        else:
            unzipped_documents.append(document)

    expert = ExpertRws()
    results = []
    for document in unzipped_documents:
        file_content = await document.read()
        file_content_str = file_content.decode("utf-8")
        parser = expert._find_parser_for_document(file_content_str)
        if parser is None:
            continue

        applicable_rules = crud_rule.get_rule_by_object_type(
            db=db,
            object_type=parser.get_object_type(),
            org_id=org.id,
        )
        gen_rules = crud_rule.get_rule_by_object_type(
            db=db,
            object_type="GEN",
            org_id=org.id,
        )
        applicable_rules.extend(gen_rules)

        if isinstance(levering_id, str):
            crud_batch.create_batch_if_not_exists(
                db=db, batch=schemas.batch.BatchCreate(id=levering_id, org_id=org.id)
            )
        # Process each applicable rule
        for rule in applicable_rules:
            processing_request = models.ProcessingRequest(
                rule_id=rule.id,
                rule_object_type=rule.object_type,
                org_id=org.id,
                status=False,  # Not yet processed, set to True after processing
            )
            rule_code = rule.object_type + rule.id
            # Prepare the file for sending
            file = io.BytesIO(file_content)
            files = {"payload": (document.filename, file, "text/xml")}
            data = {"rule_code": rule_code}
            logger.debug(f"Processing rule: {data}")

            # Make the request to the ES processor
            base_url = os.getenv("PROCESSOR_URL", "http://localhost:8006/api")
            if not base_url:
                raise ValueError("BASE_URL environment variable is missing")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{base_url}/rule/apply", files=files, data=data
                )

            # Process the response
            if response.status_code == 200:
                rule_result = response.json()
                if isinstance(levering_id, str) and isinstance(project_nr, int):
                    await __handle_results(
                        db, document, levering_id, project_nr, rule, rule_result
                    )
                processing_request.status = True
                results.append(
                    schemas.RuleResult(
                        document=document.filename,
                        rule=rule_code,
                        result=rule_result,
                        importance=rule.importance,
                    )
                )
            else:
                logger.error(
                    f"Failed to process rule for document: {document.filename}. Status code: {response.status_code}"
                )
                results.append(
                    schemas.RuleResult(
                        document=document.filename,
                        rule=rule_code,
                        error=f"Failed to process. Status code: {response.status_code}",
                        importance=rule.importance,
                    )
                )
            db.add(processing_request)
    db.commit()

    try:
        return schemas.ProcessXMLResponse(results=results)
    except Exception as e:
        logger.exception("An error occurred while processing XML documents")
        raise HTTPException(status_code=500, detail=e)


@router.get("/report/{batch_id}")
async def get_batch_report(
    batch_id: str,
    org_code: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
    expert: ExpertBase = Depends(af.expert),
) -> FileResponse:
    """
    Returns: a pdf file which contains all failed findings of a given batch
    """
    org = _get_org(db, org_code)
    return batch_report_base.get_batch_report(
        batch_id=batch_id,
        org_id=org.id,
        background_tasks=background_tasks,
        db=db,
        expert=expert,
    )
