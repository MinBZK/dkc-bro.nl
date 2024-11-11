from typing import Optional

from pydantic import BaseModel

from app.schemas import RuleBase
from app.schemas.processing_request import ProcessingRequestBase
from app.schemas.user import UserBase


class OrganizationBase(BaseModel):
    id: int
    name: str
    code: str
    users: Optional[list[UserBase]] = []
    rules: Optional[list[RuleBase]] = []
    processing_requests: Optional[list[ProcessingRequestBase]] = []

    class Config:
        orm_mode = True
