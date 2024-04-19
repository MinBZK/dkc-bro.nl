import logging
from typing import List, Optional, Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import schemas
from app.expert.expert_base import ExpertBase
from app.models.rule import Rule

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


def get_rules(db: Session, skip: int = 0, limit: int = 100) -> List[Rule]:
    """
    Retrieves rules from the database.

    Returns: List of rule objects.
    """
    return db.query(Rule).all()


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
    for rule in expertInstance.rules:
        ruleInstance = rule()
        ruleCreate = schemas.rule.RuleCreate(
            id=ruleInstance.getCode(),
            name=ruleInstance.getName(),
            object_type=ruleInstance.getObjectType(),
            importance=ruleInstance.getImportance().value,
            explanation=ruleInstance.getExplanation(),
            docstring=ruleInstance.getDocstring(),
            ruleType=ruleInstance.getRuleType().value,
            enabled=True,
        )
        add_if_not_exists_rule(db=db, rule=ruleCreate)


def update_rule(db: Session, rule: schemas.rule.RuleCreate) -> Rule:
    """
    Adds a rule if it does not exist yet.
    If it does exist, update the row in the database with the new data.

    Returns: The rule.
    """
    db_rule = (
        db.query(Rule)
        .filter(Rule.id == rule.id, Rule.object_type == rule.object_type)
        .one_or_none()
    )
    for var, value in vars(rule).items():
        setattr(db_rule, var, value) if value or str(value) == "False" else None

    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


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
