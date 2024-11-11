import io
import os
from typing import List
import logging

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

import app.app_factory as af
import app.crud.batch as crud_batch
import app.crud.finding as crud_finding
from app import models, schemas
from app.api import dependencies
from app.expert.expert_base import ExpertBase
from app.api.endpoints.poller import process_xml

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _perform_demo(dataset, db, org_code="rws"):
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
    return await process_xml(db=db, documents=documents, org_code=org_code)


@router.post(
    "/rws-demo-dry",
    summary="XML bestanden scannen op kwaliteitsregels van Rijkswaterstaat",
    response_model=schemas.rule.ProcessXMLResponse,
    response_description="Resultaat van de expert-service mochten kwaliteitsregels zijn overtreden",
)
@af.limiter.shared_limit("30/5minute", scope="demo-dry")
async def validate_rws_documents_demo_dry(
    request: Request,
    documents: List[UploadFile] = File(...),
    db: Session = Depends(dependencies.get_db),
):
    """
    XML-bestanden worden ingelezen en de kwaliteitsregels van RWS worden erop losgelaten.
    Hiervoor hoeft een gebruiker niet ingelogd te zijn.
    Resultaten worden **NIET** opgeslagen.

    **Let op**, er zit een rate limit op van 20 requests per 5 minuten.
    """
    return await process_xml(db=db, documents=documents, org_code="rws")


@router.post(
    "/demo-dry",
    summary="XML bestanden scannen op kwaliteitsregels van de huidige organisatie",
    response_model=schemas.rule.ProcessXMLResponse,
    response_description="Resultaat van de expert-service mochten kwaliteitsregels zijn overtreden",
)
@af.limiter.shared_limit("30/5minute", scope="demo-dry")
async def validate_documents_demo_dry(
    request: Request,
    documents: List[UploadFile] = File(...),
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
):
    """
    XML-bestanden worden ingelezen en de kwaliteitsregels van de huidige organisatie worden erop losgelaten.
    De gebruiker moet ingelogd zijn en gekoppeld zijn aan de gespecificeerde organisatie.
    Resultaten worden **NIET** opgeslagen.

    **Let op**, er zit een rate limit op van 20 requests per 5 minuten.
    """
    org_code = current_user.organization.code
    return await process_xml(db=db, documents=documents, org_code=org_code)


@router.post("/rws-demo-examples-files")
@af.limiter.shared_limit("30/5minute", scope="demo-examples-files")
async def perform_rws_example_demo(
    request: Request,
    dataset: str = Body(...),
    db: Session = Depends(dependencies.get_db)
):
    return await _perform_demo(dataset, db)


@router.post("/demo-examples-files")
async def perform_example_demo(
    request: Request,
    dataset: str = Body(...),
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
):
    """
    Demo for organizations, uses only the rules associated with the organization.
    """
    org_code = current_user.organization.code
    return await _perform_demo(dataset, db, org_code)


@router.post("")
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
    org_id = current_user.organization.id
    response_object = {"message": "Succesfully received document"}
    background_tasks.add_task(
        validate_and_register_documents, expert, db, org_id, documents, batch_id
    )
    return JSONResponse(response_object, 202, background=background_tasks)


async def validate_and_register_documents(
    expert,
    db,
    org_id: int,
    documents: List[UploadFile] = File(...),
    batch_id: str = None,
    project_nr: int = None,
) -> List[UploadFile]:
    documents = await run_in_threadpool(lambda: expert.validate_documents(documents))

    if batch_id:
        crud_batch.create_batch_if_not_exists(
            db=db, batch=schemas.batch.BatchCreate(id=batch_id, org_id=org_id)
        )
    crud_finding.create_rule_findings_from_documents(
        db=db, documents=documents, batch_id=batch_id, project_nr=project_nr
    )
    return documents
