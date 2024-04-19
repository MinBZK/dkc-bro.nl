import os
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

import app.app_factory as af
import app.crud.batch as crud_batch
import app.crud.finding as crud_finding
from app import models
from app.api import dependencies
from app.expert.expert_base import ExpertBase

router = APIRouter()


@router.get("")
async def get_batches(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=1000, ge=1),
) -> List:
    """
    Returns: batches
    """
    return crud_batch.get_batches(db=db, skip=skip, limit=limit)


@router.get("/report/{batch_id}")
async def get_batch_report(
    batch_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
    expert: ExpertBase = Depends(af.expert),
) -> FileResponse:
    """
    Returns: a pdf file which contains all failed findings of a given batch
    """
    # project_nr = crud_batch.get_project_nr_by_batch_id(db=db, batch_id=batch_id)
    data = crud_finding.get_findings_per_document_by_batch_id(db=db, batch_id=batch_id)
    historicaldata = crud_finding.get_previous_batches(db=db, batch_id=batch_id)
    tempFilePath = expert.generate_report(
        batch_id=batch_id,
        data=data,
        historicaldata=historicaldata,
    )

    background_tasks.add_task(remove_file, tempFilePath)

    return FileResponse(tempFilePath)


@router.get("/scan")
async def validate_etl_transform_data(
    background_tasks: BackgroundTasks,
    expert: ExpertBase = Depends(af.expert),
) -> JSONResponse:
    """
    Executes a scan and expert analysis on curent data in mounted transform folder
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


def remove_file(path: str) -> None:
    os.unlink(path)
