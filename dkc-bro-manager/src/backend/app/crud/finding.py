import csv
import io
import json
from datetime import datetime
from typing import List, Optional

import pandas as pd
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas
from app.api import exceptions
from app.models import OrganizationRule
from app.models.batch import Batch
from app.models.finding import Finding
from app.models.project import Project
from app.models.rule import Rule


def get_findings_and_rules(
    db: Session,
    org_id: int,
    skip: int = 0,
    limit: int = 100,
    filter_violations=False
) -> List:
    """
    Gets Findings and related rules from the database. Optionally filter out non violations.

    Returns: List of joined Rules+Findings
    """
    query = (
        db.query(Finding, OrganizationRule)
        .join(OrganizationRule, (Finding.rule_id == OrganizationRule.rule_id) & (Finding.rule_object_type == OrganizationRule.rule_object_type))
        .join(Batch)
        .filter(Batch.org_id == org_id)
        .order_by(Finding.timestamp.desc())
    )
    if filter_violations:
        query = query.filter(Finding.result == False)  # noqa: E712
    return query.offset(skip).limit(limit).all()


def get_findings_and_rules_and_project(
    db: Session, start_date: datetime.date, end_date: datetime.date, org_id: int
):
    """
    Gets Findings, related rules and projects from the database

    Returns: List of joined Rules+Findings+Projects
    """
    query_object = (
        db.query(Finding)
        .filter((Finding.timestamp >= start_date) & (Finding.timestamp <= end_date))
        .filter(Finding.project.has(org_id=org_id))
        .all()
    )
    if query_object:

        json_data = [
            schemas.finding.FindingsDump.from_orm(r).json() for r in query_object
        ]
        data = []
        for item in json_data:
            item_dict = json.loads(item)
            row = {
                "result": item_dict.get("result", ""),
                "feedbackMessage": item_dict.get("feedbackMessage", ""),
                "rule_id": item_dict.get("rule_id", ""),
                "rule_object_type": item_dict.get("rule_object_type", ""),
                "batch_id": item_dict.get("batch_id", ""),
                "filename": item_dict.get("filename", ""),
                "timestamp": item_dict.get("timestamp", ""),
                "project_nr": (
                    item_dict.get("project", {}).get("project_nr", "")
                    if item_dict.get("project") is not None
                    else ""
                ),
                "project_name": (
                    item_dict.get("project", {}).get("project_name", "")
                    if item_dict.get("project") is not None
                    else ""
                ),
                "source_holder": (
                    item_dict.get("project", {}).get("source_holder", "")
                    if item_dict.get("project") is not None
                    else ""
                ),
                "importance": (
                    item_dict.get("rule", {}).get("importance", "")
                    if item_dict.get("rule") is not None
                    else ""
                ),
            }
            data.append(row)

        df = pd.DataFrame(data)
        stream = io.BytesIO()
        df = df.rename(
            columns={
                "project_nr": "project_nr",
                "project_name": "project_naam",
                "source_holder": "bronhouder",
                "batch_id": "leveringsnummer",
                "filename": "naam_brondocument",
                "timestamp": "datum_uitvoering",
                "result": "geslaagd",
                "feedbackMessage": "feedbackbericht",
                "rule_object_type": "regel_object_type",
                "rule_id": "regel_nr",
                "importance": "gewicht",
            }
        )
        df = df[
            [
                "project_nr",
                "project_naam",
                "bronhouder",
                "leveringsnummer",
                "naam_brondocument",
                "datum_uitvoering",
                "geslaagd",
                "feedbackbericht",
                "regel_object_type",
                "regel_nr",
                "gewicht",
            ]
        ]
        df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"dump_bevindingen_{timestamp}.csv"

        response.headers["Content-Encoding"] = "UTF-8"
        response.headers["Content-type"] = "text/csv; charset=UTF-8"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"

        return response
    else:
        raise exceptions.NoFindingsFound


def get_findings_and_rules_by_batch_id(db: Session, batch_id: str) -> List:
    """
    Gets Findings and related rules from the database by batch id.

    Returns: List of joined Rules+Findings
    """
    return (
        db.query(Finding, OrganizationRule)
        .join(
            OrganizationRule,
            (Finding.rule_id == OrganizationRule.rule_id) & (Finding.rule_object_type == OrganizationRule.rule_object_type)
        )
        .filter(Finding.batch_id == batch_id)
        .order_by(Finding.timestamp.desc())
        .all()
    )


def create_rule_findings_from_documents(
    db: Session, documents: List, batch_id: Optional[str], project_nr: Optional[int]
) -> None:
    """
    Creates findings based on a finding and its related rule. Optionally adds a batch_id to the finding.

    Returns: None
    """
    now = datetime.now()
    for document in documents:
        for finding in document["findings"]:
            findingCreate = schemas.finding.FindingCreate(
                result=finding["result"],
                feedbackMessage=finding["feedbackMessage"],
                timestamp=now,
                filename=document["filename"],
                batch_id=batch_id,
            )
            create_rule_finding(
                db=db,
                finding=findingCreate,
                rule_id=finding["ruleId"],
                rule_object_type=finding["objectType"],
                project_nr=project_nr,
            )


def create_rule_finding(
    db: Session,
    finding: schemas.finding.FindingCreate,
    rule_id: str,
    rule_object_type: str,
    project_nr: int,
    auto_commit: bool = True,
) -> Finding:
    """
    Inserts a rule-finding combo into the database.
    Returns: The finding
    """
    project_pk = db.query(Project).filter(Project.project_nr == project_nr).first().id

    db_finding = Finding(
        **finding.dict(),
        project_id=project_pk,
        rule_id=rule_id,
        rule_object_type=rule_object_type,
    )
    db.add(db_finding)
    if auto_commit:
        db.commit()
        db.refresh(db_finding)
        return db_finding


def get_findings_per_document_by_batch_id(
    db: Session, batch_id: str, only_violations: bool = False
) -> List:
    """
    Gets all findings for a batch, grouped by document.

    Returns: List of documents with their findings.
    """
    documents = {}
    for result in get_findings_and_rules_by_batch_id(db=db, batch_id=batch_id):
        if only_violations and result.Finding.result:
            continue
        if result.Finding.timestamp in documents.keys():
            documents[result.Finding.timestamp]["findings"].append(result)
        else:
            documents[result.Finding.timestamp] = {
                "filename": result.Finding.filename,
                "project_nr": (
                    result.Finding.project.project_nr
                    if result.Finding.project
                    else None
                ),
                "object_type": result.OrganizationRule.rule_object_type,
                "timestamp": result.Finding.timestamp,
                "findings": [result],
            }

    return list(documents.values())


def get_previous_batches(db: Session, batch_id: str, n: int = 10) -> List:
    """
    Gets all finding results for a given number of historical batches

    Returns: List of documents with their findings.
    """
    source = ""
    if len(batch_id.split("_")) > 1:
        source = batch_id.split("_")[1]

    all_batch_ids = (
        db.query(Batch.id)
        .filter(Batch.id.endswith(source))
        .order_by(Batch.id.desc())
        .all()
    )
    offset = [x[0] for x in all_batch_ids].index(batch_id)
    batch_ids = (
        db.query(Batch.id)
        .filter(Batch.id.endswith(source))
        .order_by(Batch.id.desc())
        .offset(offset)
        .limit(n)
        .all()
    )
    batches = []
    batch_ids.reverse()
    for batch in batch_ids:
        batches.append(
            (
                batch[0],
                get_historical_results_previous_batches_by_ruleid(db, batch[0]),
            )
        )
    return batches


def get_historical_results_previous_batches_by_ruleid(
    db: Session, batch_id: str
) -> List:
    """
    Gets all the results findings for a given batch id grouped by rule id

    Returns: List of documents with their findings.
    """
    finding_results = (
        db.query(
            Finding.rule_id,
            Rule.name,
            func.count(Finding.result)
            .filter(Finding.batch_id == batch_id, Finding.result == True)  # noqa: E712
            .label("pass"),
            func.count(Finding.result)
            .filter(Finding.batch_id == batch_id, Finding.result == False)  # noqa: E712
            .label("fail"),
        )
        .join(Rule)
        .group_by(Finding.rule_id, Rule.name)
        .order_by(Finding.rule_id)
        .all()
    )
    return finding_results
