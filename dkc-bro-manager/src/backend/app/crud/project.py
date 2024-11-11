import logging
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.project import Project

logger = logging.getLogger(__name__)
load_dotenv()

env = os.environ.get("ENVIRONMENT", "TEST")


def get_projects(db: Session, org_id: int, include_inactive: bool = False) -> List[Project]:
    """
    Gets all project numbers from the database.

    Returns: List of project numbers
    """
    if include_inactive:
        query = (
            db.query(Project)
            .filter(Project.environment == env)
            .filter(Project.org_id == org_id)
            .order_by(Project.project_nr)
        )
    else:
        query = (
            db.query(Project)
            .filter(Project.org_id == org_id)
            .filter(
                (Project.environment == env) & (Project.active == True)  # noqa: E712
            )
            .order_by(Project.project_nr)
        )
    return query.all()


def get_project_nrs(db: Session, org_id: int) -> List[int]:
    """
    Get only project numbers from the database.
    """
    query = (
        db.query(Project)
        .filter(Project.environment == env)
        .filter(Project.org_id == org_id)
        .order_by(Project.project_nr)
    )
    return [project.project_nr for project in query.all()]


def create_project_nrs(
    db: Session,
    org_id: int,
    project_id: int,
    project_name: str,
    source_holder: str,
    closed: bool
) -> str:
    active = not closed
    existing_project = (
        db.query(Project)
        .filter(
            (Project.project_nr == project_id) &
            (Project.project_name == project_name) &
            (Project.org_id == org_id)
        )
        .first()
    )

    same_project_status = (
        db.query(Project)
        .filter(
            (Project.project_nr == project_id) &
            (Project.project_name == project_name) &
            (Project.org_id == org_id) &
            (Project.active == active)
        )
        .first()
    )

    if existing_project and same_project_status:
        return "OK"
    elif existing_project and not same_project_status:
        logging.info(
            f"Project number {project_id} with name: {project_name} and source holder {source_holder} active status is set to {active}."
        )
        payload = {
            "active": active,
            "timestamp": datetime.now(),
        }
        db.execute(
            update(Project)
            .filter(
                (Project.project_nr == project_id) &
                (Project.project_name == project_name) &
                (Project.org_id == org_id)
            )
            .values(payload)
            .execution_options(synchronize_session="fetch")
        )
        db.commit()
    else:
        logging.info(
            f"Project number {project_id} with name: {project_name} and source holder {source_holder} will be added to the database."
        )
        payload = {
            "org_id": org_id,
            "project_nr": project_id,
            "project_name": project_name,
            "source_holder": source_holder,
            "environment": env,
            "active": True,
            "timestamp": datetime.now(),
        }
        db_project_nr = Project(**payload)

        db.add(db_project_nr)
        db.commit()
        db.refresh(db_project_nr)
        return "OK"
