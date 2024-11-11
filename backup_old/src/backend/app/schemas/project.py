from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    project_nr: int
    project_name: Optional[str]
    source_holder: Optional[str]
    timestamp: datetime
    active: bool

    class Config:
        orm_mode = True
