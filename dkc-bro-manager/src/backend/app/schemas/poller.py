from typing import Optional

from pydantic import BaseModel


class PollerProcessingRequest(BaseModel):
    org_code: str
    levering_id: str
    project_nr: int
    project_naam: Optional[str] = None
    project_closed: Optional[bool] = False
    bronhouder_naam: Optional[str] = None
