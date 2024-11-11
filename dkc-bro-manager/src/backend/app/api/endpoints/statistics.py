from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependencies

router = APIRouter()


@router.get("")
async def get_statistics(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> schemas.aggregate.StatisticsAggregate:
    """
    Returns: statistics aggregate
    """
    org_id = current_user.organization.id
    return crud.aggregate.get_expert_statistics(db=db, org_id=org_id)
