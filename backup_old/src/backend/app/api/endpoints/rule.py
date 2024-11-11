from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

import app.app_factory as af
from app import crud, schemas
from app.api import dependencies

router = APIRouter()


@router.get(
    "",
    summary="Kwaliteitsregels ophalen",
    response_model=List[schemas.rule.RuleBase],
    response_description="Alle kwaliteitsregels in het systeem",
)
@af.limiter.shared_limit("2/minute", scope="")
async def get_rules(
    request: Request,
    db: Session = Depends(dependencies.get_db),
) -> List:
    """
    Alle kwaliteitsregels worden opgehaald, inclusief de weging en ID's.
    - **id**: id van regel
    - **name**: naam van regel
    - **object_type**: groep waar de regel toebehoort
    - **importance**: weging (info=1, waarschuwing=2, fout=3)
    - **explanation**: korte uitleg regel
    - **docstring**: uitgebreide uitleg regel
    - **ruleType**: regel die individueel of tot een groep behoort (1=individueel, 2=group)
    - **enabled**: boolean voor actief/inactief

    **Let op**, er zit een rate limit op van 4 per minuut.
    """
    return crud.rule.get_rules(db=db)


@router.put(
    "/{object_type}/{rule_id}",
    response_model=schemas.rule.RuleCreate,
    include_in_schema=False,
)
def update_rule(
    rule: schemas.rule.RuleCreate,
    db: Session = Depends(dependencies.get_db),
    # current_user: models.user.User = Depends(dependencies.get_current_user),
) -> None:
    """
    Updates a given rule in the database

    Returns: None
    """
    crud.rule.update_rule(db=db, rule=rule)
