import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.log_poller import LogPoller

logger = logging.getLogger(__name__)


def get_log_poller(db: Session) -> LogPoller:
    """
    Retrieves logging from rws poller from the database.

    Returns: List of rule objects.
    """
    return db.query(LogPoller).one()


def create_log_poller(
    db: Session,
    log_message: str,
    request_url: str,
    request_status_code: int,
) -> LogPoller:
    """
    Writes logging of the poller to the database.

    Returns: List of rule objects.
    """
    model = LogPoller
    payload = {
        "request_url": request_url,
        "request_status_code": request_status_code,
        "log_message": log_message,
        "timestamp": datetime.now(),
    }
    db_log_poller = model(**payload)
    if len(db.query(model).all()) == 0:
        db.add(db_log_poller)
    else:
        db.query(model).update(payload, synchronize_session="fetch")
    db.commit()
    db.refresh(db_log_poller)
    return db_log_poller
