from abc import ABC, abstractmethod
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate


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
