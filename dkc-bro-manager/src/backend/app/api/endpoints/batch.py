from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

import app.app_factory as af
import app.crud.batch as crud_batch
from app.api import dependencies
from app.expert.expert_base import ExpertBase
from app.expert.report_generators import batch_report_base
from app.models import User

router = APIRouter()


@router.get("")
async def get_batches(
    db: Session = Depends(dependencies.get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=1000, ge=1),
    current_user: User = Depends(dependencies.get_current_user),
) -> List:
    """
    Returns: batches
    """
    org_id = current_user.organization.id
    return crud_batch.get_batches(db=db, org_id=org_id, skip=skip, limit=limit)


@router.get("/report/{batch_id}")
async def get_batch_report(
    batch_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
    expert: ExpertBase = Depends(af.expert),
    current_user: User = Depends(dependencies.get_current_user),
) -> FileResponse:
    """
    Returns: a pdf file which contains all failed findings of a given batch
    """
    org_id = current_user.organization.id
    return batch_report_base.get_batch_report(
        batch_id=batch_id,
        org_id=org_id,
        background_tasks=background_tasks,
        db=db,
        expert=expert,
    )


@router.get("/scan")
async def validate_etl_transform_data(
    background_tasks: BackgroundTasks,
    expert: ExpertBase = Depends(af.expert),
) -> JSONResponse:
    """
    Executes a scan and expert analysis on current data in mounted transform folder
    """
    response_object = {"message": "Succesfully received batch validation job"}
    background_tasks.add_task(expert.scan_and_validate_documents)

    return JSONResponse(response_object, 202, background=background_tasks)


@router.get("/statistics")
async def get_statistics(
    db: Session = Depends(dependencies.get_db),
) -> List:
    """
    get latest statistics from each source
    """
    batches = crud_batch.get_latest_batches_per_source(db=db)
    result = [
        crud_batch.get_batch_statistics_with_trend(db, batch.id) for batch in batches
    ]

    return result
