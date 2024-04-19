import io
import os
from typing import List
from zipfile import ZipFile

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false, true
from starlette.requests import Request

import app.app_factory as af
import app.crud.batch as crud_batch
import app.crud.finding as crud_finding
import app.crud.rule as crud_rule
from app import models, schemas
from app.api import dependencies
from app.expert.expert_base import ExpertBase

router = APIRouter()


def __filter_violations(documents: List) -> List:
    """
    Filters a list of findings per document such that only violations are returned.

    Returns: List of documents with only violations.
    """
    output = []
    for doc in documents:
        violations = [f for f in doc.get("findings") if not f.get("result")]
        output.append({"filename": doc.get("filename"), "findings": violations})
    return output


async def __validate(
    expert: ExpertBase, db: Session, documents: List[UploadFile], dry_run=false
) -> List:
    """
    Takes a list of input files and applies all relevant rules.
    Findings are stored in the connected database.

    Returns: Report containing findings and linked importance levels of rules.
    """
    unzipped_documents = []
    for doc in documents:
        if doc.content_type in ["application/zip", "application/x-zip-compressed"]:
            with ZipFile(io.BytesIO(doc.file.read()), "r") as zf:
                for item in zf.namelist():
                    f = zf.open(item)
                    unzipped_documents.append(UploadFile(filename=f.name, file=f))
        elif doc.content_type in ["text/xml", "application/xml"]:
            unzipped_documents.append(doc)
        else:
            unzipped_documents.append(doc)

    documents = await expert.validate_documents(unzipped_documents)
    # Enrich findings with importance levels of associated rules.
    for document in documents:
        for finding in document.get("findings"):
            rule = crud_rule.get_rule_by_id_and_type(
                db=db,
                rule_id=str(finding.get("ruleId")),
                object_type=finding.get("objectType"),
            )
            finding["importance"] = rule.importance
    if not dry_run:
        crud_finding.create_rule_findings_from_documents(
            db=db, documents=documents, batch_id=None, project_nr=None
        )
    return __filter_violations(documents)


@router.post("/demo", include_in_schema=False)
async def validate_documents_demo(
    documents: List[UploadFile] = File(...),
    expert: ExpertBase = Depends(af.expert),
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> List:
    """
    Takes a list of input files and applies all relevant rules.
    Findings are stored in the connected database.

    Returns: Report containing findings and linked importance levels of rules.
    """
    return await __validate(expert, db, documents, false)


@router.post(
    "/demo-dry",
    summary="XML bestanden scannen op kwaliteitsregels",
    response_model=List[schemas.finding.FindingsDocument],
    response_description="Resultaat van de expert-service mochten kwaliteitsregels zijn overtreden",
)
@af.limiter.shared_limit("20/5minute", scope="demo-dry")
async def validate_documents_demo_dry(
    request: Request,
    documents: List[UploadFile] = File(...),
    expert: ExpertBase = Depends(af.expert),
    db: Session = Depends(dependencies.get_db),
) -> List:
    """
    XML bestanden worden ingelezen en de kwaliteitsregels worden erop losgelaten.
    Resultaten worden **NIET** opgeslagen.

    **Let op**, er zit een rate limit op van 20 requests per 5 minuten.
    """
    return await __validate(expert, db, documents, true)


@router.post("/demo-examples-files", include_in_schema=False)
@af.limiter.shared_limit("2/minute", scope="demo-examples-files")
async def perform_example_demo(
    request: Request,
    dataset: str = Body(...),
    expert: ExpertBase = Depends(af.expert),
    db: Session = Depends(dependencies.get_db),
) -> List:
    """
    Performs a demonstration of the application by using a preset zipfile with files.

    Returns: Report containing findings and linked importance levels of rules.
    """
    if dataset == "waterdomein":
        zip_path = os.path.dirname(__file__) + "/../../resources/waterdomein.zip"
    elif dataset == "bodemdomein":
        zip_path = os.path.dirname(__file__) + "/../../resources/bodemdomein.zip"
    else:
        return None
    with open(zip_path, "rb") as f:
        documents = [
            UploadFile(
                filename=f"{dataset}.zip",
                file=io.BytesIO(f.read()),
                content_type="application/x-zip-compressed",
            )
        ]
    return await __validate(expert, db, documents, true)


@router.post("", include_in_schema=False)
async def validate_documents(
    background_tasks: BackgroundTasks,
    documents: List[UploadFile] = File(...),
    batch_id: str = None,
    expert: ExpertBase = Depends(af.expert),
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> JSONResponse:
    """
    Takes a list of input files and applies all relevant rules.
    Findings are stored in the connected database

    Returns: Report containing findings.
    """
    response_object = {"message": "Succesfully received document"}
    background_tasks.add_task(
        validate_and_register_documents, expert, db, documents, batch_id
    )
    return JSONResponse(response_object, 202, background=background_tasks)


async def validate_and_register_documents(
    expert,
    db,
    documents: List[UploadFile] = File(...),
    batch_id: str = None,
    project_nr: int = None,
) -> List[UploadFile]:
    documents = await run_in_threadpool(lambda: expert.validate_documents(documents))

    if batch_id:
        crud_batch.create_batch_if_not_exists(
            db=db, batch=schemas.batch.BatchCreate(id=batch_id)
        )
    crud_finding.create_rule_findings_from_documents(
        db=db, documents=documents, batch_id=batch_id, project_nr=project_nr
    )
    return documents
