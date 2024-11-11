from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import ProcessingRequest, Organization, User
from app.api import dependencies
import logging


router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/processing-request", response_model=List[dict])
def get_processing_request(
    db: Session = Depends(dependencies.get_db),
    status: Optional[bool] = Query(None, description="Filter by status"),
    current_user: User = Depends(dependencies.get_current_user),
):
    """
    Returns: Organization ID, Rule ID and rule Object type (e.g. GLD)
    """
    org_id = current_user.organization.id
    try:
        query = (
            db.query(
            ProcessingRequest.rule_id,
            ProcessingRequest.rule_object_type,
            ProcessingRequest.org_id,
            ProcessingRequest.status,
            ProcessingRequest.timestamp,
            Organization.name.label("org_name"),
            )
            .join(Organization, ProcessingRequest.org_id == Organization.id)
            .filter(ProcessingRequest.org_id == org_id)
        )

        if status is not None:
            query = query.filter(ProcessingRequest.status == status)

        results = query.all()

        response = [
            {
                "rule_code": f"{result.rule_object_type}{result.rule_id}",
                "org_name": result.org_name,
                "status": result.status,
                "timestamp": result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for result in results
        ]

        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error occured: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
