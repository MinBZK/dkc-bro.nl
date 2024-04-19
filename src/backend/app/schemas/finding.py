from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class FindingBase(BaseModel):
    result: bool
    feedbackMessage: Optional[str]
    ruleId: str
    objectType: str
    importance: int


class FindingCreate(BaseModel):
    result: bool
    feedbackMessage: Optional[str]
    timestamp: datetime
    filename: str
    batch_id: Optional[str] = None


class Finding(FindingBase):
    id: int
    rule_id: str

    class Config:
        orm_mode = True


class FindingsDocument(BaseModel):
    filename: str
    findings: List[FindingBase]


class RuleRelated(BaseModel):
    importance: int

    class Config:
        orm_mode = True


class ProjectRelated(BaseModel):
    project_nr: int
    project_name: Optional[str]
    source_holder: Optional[str]

    class Config:
        orm_mode = True


class FindingsDump(BaseModel):
    result: bool
    feedbackMessage: Optional[str]
    rule_id: str
    rule_object_type: str
    batch_id: str
    filename: str
    timestamp: datetime

    project: Optional[ProjectRelated]
    rule: Optional[RuleRelated]

    class Config:
        orm_mode = True
