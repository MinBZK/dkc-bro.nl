from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependencies

router = APIRouter()


@router.get("", response_model=List[schemas.Project])
async def get_project_nrs(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> List:
    """
    Get all project numbers
    """
    return crud.project.get_project_nrs(db=db, include_inactive=True)
