from enum import StrEnum, auto
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, computed_field


class Authority(BaseModel):
    kvk_number: int = Field(alias="kvkNummer")
    name: str = Field(alias="naam")


class BhpProject(BaseModel):
    id: int = Field(alias="projectId")
    name: str = Field(alias="projectNaam")
    closed: bool = Field(default=False)
    batch_ids: Optional[list[str]] = []
    authority: Authority = Field(alias="bronhouder")


class BhpDocument(BaseModel):
    id: int
    status: str
    filename: str
    last_changed: datetime = Field(alias="lastChanged")


class Importance(StrEnum):
    info = auto()
    warnings = auto()
    errors = auto()


class ManagerResult(BaseModel):
    document: str
    rule: str
    importance: Importance
    result: Optional[dict] = None
    error: Optional[str] = None

    @field_validator("importance", mode="before")
    def convert_importance(cls, value: int):
        if value == 1:
            return Importance.info
        if value == 2:
            return Importance.warnings
        if value == 3:
            return Importance.errors
        raise ValueError("Importance must be 1, 2 or 3")


class BatchInfo(BaseModel):
    id: str = Field(alias="identifier")
    status: str
    documents: list[BhpDocument] = Field(alias="brondocuments")
    last_changed: datetime = Field(alias="lastChanged")


class FullDocumentInfo(BaseModel):
    bhp_document_id: int
    filename: str
    org_code: str
    levering_id: str
    project_nr: int
    project_naam: str
    bronhouder_naam: str
    content: str


class DocumentWithResults(FullDocumentInfo):
    results: list[ManagerResult]


class BatchSummary(BaseModel):
    project_id: int
    batch_id: str
    importance_list: list[Importance] = []
    feedback_messages: list[str] = []

    @computed_field
    @property
    def importance(self) -> Importance:
        if Importance.errors in self.importance_list:
            return Importance.errors
        if Importance.warnings in self.importance_list:
            return Importance.warnings
        return Importance.info

    @computed_field
    @property
    def summary(self) -> str:
        n_errors = self.importance_list.count(Importance.errors)
        n_warnings = self.importance_list.count(Importance.warnings)

        message = "Deze levering heeft na controle "
        if n_errors + n_warnings <= 0:
            message += "geen bijzonderheden"
        if n_errors == 1:
            message += "1 fout"
        elif n_errors > 1:
            message += f"{n_errors} fouten"
        if n_errors > 0 and n_warnings > 0:
            message += " en "
        if n_warnings == 1:
            message += "1 waarschuwing"
        elif n_warnings > 1:
            message += f"{n_warnings} waarschuwingen"
        message += "."
        return message
