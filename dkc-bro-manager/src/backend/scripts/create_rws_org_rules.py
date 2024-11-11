from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.organization import Organization
from app.models.rule import Rule
from app.models.organization_rule import OrganizationRule


def org_rules_already_exist(session: Session) -> bool:
    print("Checking if organization rules already exist...")
    existing_org_rules = session.query(OrganizationRule).count()
    return existing_org_rules > 0


def create_rws_org_rules(session: Session) -> None:
    rws_org = session.query(Organization).filter(Organization.code == "rws").first()
    rws_rules = session.query(Rule).all()
    print("Creating organization rules for RWS...")
    for rule in rws_rules:
        org_rule = OrganizationRule(
            rule_id=rule.id,
            rule_object_type=rule.object_type,
            org_id=rws_org.id,
            name=rule.name,
            importance=rule.importance,
            explanation=rule.explanation,
            docstring=rule.docstring,
            enabled=rule.enabled,
        )
        session.add(org_rule)
    session.commit()


def main_create_rws_org_rules() -> None:
    session = next(get_db())
    if not org_rules_already_exist(session):
        create_rws_org_rules(session)
        print("Finished creating organization rules.")
    else:
        print("There already are organization rules.")
    session.close()



if __name__ == "__main__":
    main_create_rws_org_rules()