from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

import app.app_factory as af
from app import crud, schemas
from app.api import dependencies
from app.models.user import User

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.rule.RuleBase],
)
async def get_rules(
    request: Request,
    db: Session = Depends(dependencies.get_db),
    user: User = Depends(dependencies.get_current_user),
) -> List[schemas.rule.RuleBase]:
    return crud.rule.get_rules(db=db, org_id=user.org_id)


@router.get(
    "-demo",
    summary="Kwaliteitsregels ophalen",
    response_model=List[schemas.rule.RuleBase],
    response_description="Alle kwaliteitsregels in het systeem van RWS",
)
@af.limiter.shared_limit("30/5minute", scope="")
async def get_rws_rules(
    request: Request,
    db: Session = Depends(dependencies.get_db),
) -> List[schemas.rule.RuleBase]:
    """
    Alle kwaliteitsregels worden opgehaald specifiek van RWS, inclusief de weging en ID's.
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
    return crud.rule.get_rules(db=db, org_id=1)


@router.put("/{object_type}/{rule_id}", response_model=schemas.rule.RuleCreate)
def update_rule(
    rule: schemas.rule.RuleCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> schemas.rule.RuleCreate:
    """
    Updates a given rule in the database

    Returns: None
    """
    org = current_user.organization
    db_org_rule = crud.rule.update_rule(db=db, rule=rule, org=org)
    rule.name = db_org_rule.name
    rule.importance = db_org_rule.importance
    rule.explanation = db_org_rule.explanation
    rule.docstring = db_org_rule.docstring
    rule.enabled = db_org_rule.enabled
    return rule
