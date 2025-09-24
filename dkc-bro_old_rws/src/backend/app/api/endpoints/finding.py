from datetime import date
from typing import Dict, List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies

router = APIRouter()


@router.get("")
async def get_findings(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
) -> List:
    """
    Returns: findings
    """
    return crud.finding.get_findings_and_rules(
        db=db, skip=skip, limit=limit, filter_violations=True
    )


@router.get("/documents")
async def get_findings_per_document(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
) -> List:
    """
    Returns: findings grouped per document
    """
    documents = {}
    for result in crud.finding.get_findings_and_rules(db=db, skip=skip, limit=limit):
        truncated_datetime = result.Finding.timestamp.replace(second=0, microsecond=0)
        key_tuple = (truncated_datetime, result.Finding.filename)
        if key_tuple in documents.keys():
            documents[key_tuple]["findings"].append(result)
        else:
            documents[key_tuple] = {
                "filename": result.Finding.filename,
                "object_type": result.Rule.object_type,
                "timestamp": truncated_datetime,
                "findings": [result],
            }

    return list(documents.values())


@router.get("/download")
async def download_findings(
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> StreamingResponse:
    """
    Returns: findings as a CSV file
    """
    return crud.finding.get_findings_and_rules_and_project(
        db=db, start_date=start_date, end_date=end_date
    )


@router.get("/area-chart")
async def get_findings_area_chart(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> List:
    """
    Returns: List of aggregate objects containing a date and true/false count of results for each date.
    """
    return crud.aggregate.get_finding_results_by_date(db)


@router.get("/area-batch-chart")
async def get_findings_area_batch_chart_per_source(
    db: Session = Depends(dependencies.get_db),
) -> Dict:
    """
    Returns: A dict with historical results for each source.
    """
    latest_batches = crud.batch.get_latest_batches_per_source(db)
    result = {}
    for batch in latest_batches:
        batch_id_split = batch.id.split("_")
        source = batch_id_split[1] if len(batch_id_split) > 1 else "Onbekend"
        result[source] = crud.finding.get_previous_batches(db, batch.id, 20)

    return result
