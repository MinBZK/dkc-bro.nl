import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api import dependencies

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=List[schemas.Project])
async def get_projects(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> List:
    """
    Get all projects
    """
    org_id = current_user.organization.id
    return crud.project.get_projects(db, org_id, include_inactive=True)
