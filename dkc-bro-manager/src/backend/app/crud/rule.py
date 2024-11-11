import logging
from typing import List, Optional, Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import schemas
from app.expert.expert_base import ExpertBase
from app.models import OrganizationRule, Organization, Rule
from app.schemas import RuleBase

logger = logging.getLogger(__name__)


def get_rule_by_id_and_type(
    db: Session, rule_id: str, object_type: str
) -> Optional[Rule]:
    """
    Gets a rule from the database by id and type.

    Returns: The found rule
    """
    return (
        db.query(Rule)
        .filter(and_(Rule.id == rule_id, Rule.object_type == object_type))
        .first()
    )


def get_rules(
    db: Session, org_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[RuleBase]:
    """
    join rule and organization_rule tables to get the following attributes:
    - rule.id as id
    - rule.object_type as object_type
    - rule.ruleType as ruleType
    - organization_rule.name as name
    - organization_rule.importance as importance
    - organization_rule.explanation as explanation
    - organization_rule.docstring as docstring
    - organization_rule.enabled as enabled
    """
    db_result = db.query(
        Rule.id,
        Rule.object_type,
        Rule.ruleType,
        OrganizationRule.name,
        OrganizationRule.importance,
        OrganizationRule.explanation,
        OrganizationRule.docstring,
        OrganizationRule.enabled,
    ).join(
        OrganizationRule,
        and_(
            OrganizationRule.rule_id == Rule.id,
            OrganizationRule.rule_object_type == Rule.object_type,
        ),
    )

    if org_id:
        db_result = db_result.filter(OrganizationRule.org_id == org_id)
    db_result = db_result.all()

    return [
        schemas.Rule(
            id=row[0],
            object_type=row[1],
            ruleType=row[2],
            name=row[3],
            importance=row[4],
            explanation=row[5],
            docstring=row[6],
            enabled=row[7],
        )
        for row in db_result
    ]


def create_rule(db: Session, rule: schemas.rule.RuleCreate) -> Rule:
    """
    Creates a rule based on the given input object and writes it to the database.

    Returns: Created rule object.
    """
    db_rule = Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def update_rule_initialization(db: Session, rule: dict) -> dict:
    """
    Updates a rule based on the status quo database and alembic latest version and writes it to the database.

    Returns: Created rule object.
    """
    db_rule = Rule(**rule)
    db.merge(db_rule)
    db.commit()
    return rule


def add_if_not_exists_rule(
    db: Session, rule: schemas.rule.RuleCreate
) -> Tuple[Rule | dict, bool]:
    """
    Adds a rule to the database if a rule with that type and id does not exist yet.
    Returns: Tuple of the created rule and bool indicating whether a new rule was created
    """
    db_rule = (
        db.query(Rule)
        .filter(Rule.id == rule.id, Rule.object_type == rule.object_type)
        .one_or_none()
    )

    if db_rule is None:
        return create_rule(db=db, rule=rule), False
    else:
        dict_db_rule = schemas.rule.RuleCreate.from_orm(db_rule).dict()

        if rule.dict() != dict_db_rule:
            for key, value in dict_db_rule.items():
                if value is None:
                    dict_db_rule[key] = rule.dict()[key]
            return update_rule_initialization(db=db, rule=dict_db_rule), False
        else:
            return db_rule, True


def add_new_rules(db: Session, expert_class: ExpertBase) -> None:
    """
    Given a class of Expert, this method adds all the rules known by the expert to the database if they do not exist there yet.
    New rules will never start disabled, thus the enabled field is hardcoded to True here.

    Returns: None
    """
    expertInstance = expert_class()
    for ruleInstance in expertInstance.rules:
        ruleCreate = schemas.rule.RuleCreate(
            id=ruleInstance.getCode(),
            name=ruleInstance.getName(),
            object_type=ruleInstance.getObjectType(),
            importance=ruleInstance.getImportance(),
            explanation=ruleInstance.getExplanation(),
            docstring=ruleInstance.getDocstring(),
            ruleType=ruleInstance.getRuleType().value,
            enabled=True,
        )
        add_if_not_exists_rule(db=db, rule=ruleCreate)


def update_rule(db: Session, rule: schemas.rule.RuleCreate, org: Organization) -> Rule:
    """
    Adds a rule if it does not exist yet.
    If it does exist, update the row in the database with the new data.

    Returns: The rule.
    """
    db_org_rule = (
        db.query(OrganizationRule)
        .filter(
            OrganizationRule.rule_id == rule.id,
            OrganizationRule.rule_object_type == rule.object_type,
        )
        .filter(OrganizationRule.org_id == org.id)
    )

    rule_attrs = rule.dict()
    rule_attrs.pop("id")
    rule_attrs.pop("object_type")
    rule_attrs.pop("ruleType")

    db_org_rule.update(rule_attrs)
    db.commit()

    return db_org_rule.one()


def get_enabled_state_of_rule(db: Session, rule_id: str, object_type: str) -> bool:
    """
    Returns the enabled column of the rule with given id and object type.

    Returns: Boolean indicating whether or not the rule is active in the database.
    """
    rule = get_rule_by_id_and_type(db=db, rule_id=rule_id, object_type=object_type)
    if rule:
        return rule.enabled
    else:
        return False


def get_rule_by_object_type(db: Session, object_type: str, org_id: int) -> List[Rule]:
    """
    Returns all rules with the given object type.

    Returns: List of rules.
    """
    return (
        db.query(Rule)
        .join(Rule.organization_rules)
        .filter(Rule.object_type == object_type)
        .filter(OrganizationRule.org_id == org_id)
        .order_by(Rule.id)
        .all()
    )
