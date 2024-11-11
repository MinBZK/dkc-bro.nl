from datetime import timedelta
from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app import schemas
from app.models import OrganizationRule
from app.models.batch import Batch
from app.models.finding import Finding
from app.models.rule import Rule


def get_expert_statistics(db: Session, org_id: int) -> schemas.aggregate.StatisticsAggregate:
    """
    Calculates some simple statistics about the amount of rules, findings and batches known to the database.

    Returns: Aggregate object containing the counts of each table.
    """
    rules = (
        db.query(Rule)
        .join(
            OrganizationRule,
            and_(
                OrganizationRule.rule_id == Rule.id,
                OrganizationRule.rule_object_type == Rule.object_type,
            ),
        )
        .filter(OrganizationRule.org_id == org_id)
        .count()
    )
    findings = (
        db.query(Finding)
        .join(Batch, Finding.batch_id == Batch.id)
        .filter(Batch.org_id == org_id)
        .count()
    )
    batches = db.query(Batch).filter(Batch.org_id == org_id).count()
    return schemas.aggregate.StatisticsAggregate(
        rules=rules, findings=findings, batches=batches
    )


def get_finding_results_by_date(
    db: Session,
    org_id: int,
) -> List[schemas.aggregate.FindingDateResultAggregate]:
    """
    Calculates the ratio of true false results of findings grouped by date.
    Returns: List of aggregates containing a date, true,false each.
    """
    dates = (
        db.query(
            func.date_trunc(
                "day",
                func.generate_series(
                    func.min(Finding.timestamp),
                    func.max(Finding.timestamp) + timedelta(days=1),
                    timedelta(days=1),
                ),
            ).label("ts"),
        )
        .join(Batch, Finding.batch_id == Batch.id)
        .filter(Batch.org_id == org_id)
        .subquery()
    )

    values = (
        db.query(
            func.date_trunc("day", Finding.timestamp).label("timestamp"),
            func.count(Finding.result)
            .filter(Finding.result == True)  # noqa: E712
            .label("true"),
            func.count(Finding.result)
            .filter(Finding.result == False)  # noqa: E712
            .label("false"),
        )
        .join(Batch, Finding.batch_id == Batch.id)
        .filter(Batch.org_id == org_id)
        .group_by(func.date_trunc("day", Finding.timestamp))
        .subquery()
    )

    rows = (
        db.query(
            dates.c.ts,
            func.coalesce(values.c.true, 0),
            func.coalesce(values.c.false, 0),
        )
        .outerjoin(values, values.c.timestamp == dates.c.ts)
        .order_by(dates.c.ts)
        .all()
    )

    result = [
        schemas.aggregate.FindingDateResultAggregate(
            date=row[0], true=row[1], false=row[2]
        )
        for row in rows
    ]
    return result
