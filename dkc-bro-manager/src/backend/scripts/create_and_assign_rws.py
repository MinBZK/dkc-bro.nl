from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models import User, Batch, Project
from app.models.organization import Organization


def organization_exists(session: Session) -> bool:
    print("Checking if there are organizations present...")
    existing_org = (
        session
        .query(Organization)
        .count()
    )
    return existing_org > 0


def create_rws(session: Session) -> None:
    print("Creating Rijkswaterstaat organization.")
    rws = Organization(name="Rijkswaterstaat", code="rws")
    session.add(rws)
    session.commit()
    session.refresh(rws)


def add_users_to_rws(session: Session) -> None:
    print("Assigning all existing users to Rijkswaterstaat.")
    rws_org = session.query(Organization).filter(Organization.code == "rws").first()
    session.query(User).update({"org_id": rws_org.id})
    session.commit()


def add_projects_and_batches_to_rws(session: Session) -> None:
    print("Assigning all existing projects and batches to Rijkswaterstaat.")
    rws_org = session.query(Organization).filter(Organization.code == "rws").first()
    session.query(Batch).update({"org_id": rws_org.id})
    session.query(Project).update({"org_id": rws_org.id})
    session.commit()


def main_assign_resources_to_rws() -> None:
    session = next(get_db())
    if not organization_exists(session):
        create_rws(session)
        add_users_to_rws(session)
        add_projects_and_batches_to_rws(session)
        print("Finished assigning resources to Rijkswaterstaat.")
    else:
        print("There already are organizations.")
    session.close()


if __name__ == "__main__":
    main_assign_resources_to_rws()