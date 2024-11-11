from typing import List, Optional

from pydantic import BaseModel

from app.schemas.finding import Finding


class RuleBase(BaseModel):
    id: str
    name: str
    object_type: str
    importance: int
    explanation: str
    docstring: Optional[str]
    ruleType: int
    enabled: bool

    class Config:
        orm_mode = True


class RuleCreate(RuleBase):
    pass

    class Config:
        orm_mode = True


class Rule(RuleBase):
    findings: List[Finding] = []

    class Config:
        orm_mode = True


class RuleResult(BaseModel):
    document: str
    rule: str
    importance: int
    result: Optional[dict]
    error: Optional[str]


class ProcessXMLResponse(BaseModel):
    results: List[RuleResult]
