from datetime import datetime

from pydantic import BaseModel


class StatisticsAggregate(BaseModel):
    rules: int
    findings: int
    batches: int


class FindingDateResultAggregate(BaseModel):
    date: datetime
    true: int
    false: int
