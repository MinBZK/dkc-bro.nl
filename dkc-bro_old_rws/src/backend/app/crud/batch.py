from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

import app.crud.finding as crud_finding
from app import schemas
from app.models.batch import Batch


def get_existance_of_batch(db: Session, batch_id: str) -> bool:
    """
    Checks the database for the existance of a batch with the given id.

    Returns: Boolean indication whether the batch has been found or not.
    """
    db_batch = db.query(Batch).filter(Batch.id == batch_id).one_or_none()
    return db_batch is not None


def create_batch_if_not_exists(db: Session, batch: schemas.batch.BatchCreate) -> Batch:
    """
    Creates a new record for a batch in the batch table in the database, if a batch with that id does not exist yet.

    Returns: the created batch object.
    """
    if get_existance_of_batch(db=db, batch_id=batch.id):
        return None
    db_batch = Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


def get_batches(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
    """
    Gets batches from the database.

    Returns: List of batch objects.
    """
    return db.query(Batch).order_by(Batch.id.desc()).offset(skip).limit(limit).all()


def get_latest_batches_per_source(db: Session, nr_of_sources: int = 4) -> List[Batch]:
    """
    Gets latest batches from the database from all sources

    Returns: List of batch objects.
    """

    return db.query(Batch).order_by(Batch.id.desc()).limit(nr_of_sources).all()


def get_historical_trend_batch(db: Session, source: str, offset: int = 2) -> Batch:
    """
    Retrieves a batch of a source with a given offset

    Returns: The retrieved batch
    """

    return (
        db.query(Batch)
        .filter(Batch.id.endswith(source))
        .order_by(Batch.id.desc())
        .offset(offset)
        .limit(1)
        .first()
    )


def get_batch_statistics(db: Session, batch_id: str) -> Dict:
    """
    Calculates statistics about the a given batch

    Returns: a dictionary including the source/date of a batch and a number of statistics
    """
    batch_id_split = batch_id.split("_")
    source = batch_id_split[1] if len(batch_id_split) > 1 else "Onbekend"
    datetime_object = datetime.strptime(batch_id_split[0].split(" ")[0], "%Y-%m-%d")
    date = datetime_object.strftime("%d %b %Y")

    data = crud_finding.get_findings_per_document_by_batch_id(db=db, batch_id=batch_id)

    nr_active_rules = len(data[0]["findings"])
    nr_records = len(data)
    nr_failed_records = len(
        [
            document
            for document in data
            if any(not f.Finding.result for f in document["findings"])
        ]
    )

    percentage_failed = (nr_failed_records / nr_records) * 100 if nr_records > 0 else 0

    return {
        "source": source,
        "date": date,
        "nrActiveRules": nr_active_rules,
        "nrRecords": nr_records,
        "nrFailedRecords": nr_failed_records,
        "percentageFailed": percentage_failed,
    }


def get_batch_statistics_with_trend(db: Session, batch_id) -> Dict:
    """
    retrieves statistics about the latest batches including a trend value which indicates the change over time

    Returns: a dictionary including the source/date of a batch and a nr of statistics
    """
    batch_id_split = batch_id.split("_")
    source = batch_id_split[1] if len(batch_id_split) > 1 else "Onbekend"
    trend_batch = get_historical_trend_batch(db, source, offset=14)
    previous_stats = (
        get_batch_statistics(db, trend_batch.id)
        if trend_batch is not None
        else {"percentageFailed": 0}
    )
    current_stats = get_batch_statistics(db, batch_id)
    current_stats["trend"] = (
        current_stats["percentageFailed"] - previous_stats["percentageFailed"]
    )
    return current_stats
