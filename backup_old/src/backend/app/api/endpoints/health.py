from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud
from app.api import dependencies
from app.api.exceptions import PollerNotActive, PollerTimestampError
from app.utils.pingdom import generate_pingdom_xml

router = APIRouter()


@router.get("/poller")
async def get_health(
    db: Session = Depends(dependencies.get_db),
) -> Response:
    """
    Returns: check whether the latest logging is not older than 10 minute and has a 200 OK status code.
    """
    query_object = crud.log_poller.get_log_poller(db=db)
    time_difference = datetime.now() - query_object.timestamp
    if query_object.request_status_code != 200:
        http_exception = PollerNotActive()
        data = generate_pingdom_xml(http_exception.detail, http_exception.status_code)
    elif time_difference > timedelta(minutes=30):
        http_exception = PollerTimestampError()
        data = generate_pingdom_xml(http_exception.detail, http_exception.status_code)
    else:
        data = generate_pingdom_xml("OK", 200)

    return Response(content=data, media_type="application/xml")


@router.get("/dkc")
def healthcheck(
    db: Session = Depends(dependencies.get_db),
) -> Response:
    """
    check whether the database still responds
    """
    db.execute(text("SELECT 1"))  # random query
    data = generate_pingdom_xml("OK", 200)
    return Response(content=data, media_type="application/xml")
