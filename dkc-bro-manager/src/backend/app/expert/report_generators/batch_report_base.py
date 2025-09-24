import os
from abc import ABC, abstractmethod
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate


from fastapi import Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models
from app.crud import finding as crud_finding
from app.expert.expert_base import ExpertBase


def get_batch_report(
    batch_id: str,
    org_id: int,
    background_tasks: BackgroundTasks,
    db: Session,
    expert: ExpertBase,
) -> FileResponse:
    """
    Returns: a pdf file which contains all failed findings of a given batch
    """
    # Check if org has access to this batch
    batch = (
        db.query(models.Batch)
        .filter(models.Batch.id == batch_id)
        .filter(models.Batch.org_id == org_id)
        .one_or_none()
    )

    if not batch:
        raise HTTPException(
            status_code=404,
            detail=f"Batch {batch_id} not found for provided organization.",
        )

    data = crud_finding.get_findings_per_document_by_batch_id(db=db, batch_id=batch_id)
    historicaldata = crud_finding.get_previous_batches(db=db, batch_id=batch_id)
    try:
        tempFilePath = expert.generate_report(
            batch_id=batch_id,
            data=data,
            historicaldata=historicaldata,
        )
    except IndexError:
        raise HTTPException(
            status_code=424,
            detail="Generation of report not possible for invalid document.",
        )


    background_tasks.add_task(os.unlink, tempFilePath)

    return FileResponse(tempFilePath)


class BatchReporterBase(ABC):
    def __init__(self, batch_id, data, historicaldata=None):
        self.data = data
        self.historicaldata = historicaldata
        self.datetime = datetime.now()
        self.fileName = f"/tmp/report_{str(self.datetime.date())}.pdf"
        self.batch_id = batch_id
        pdf = SimpleDocTemplate(filename=self.fileName, pagesize=A4)

        contentBuilder = [].append

        # get content from subclass
        self.getContent(contentBuilder)

        # creates actual pdf file
        pdf.build(contentBuilder.__self__)


@abstractmethod
def getContent(self, contentBuilder):
    """Creates the content of the pdf document"""
    raise NotImplementedError
