from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogPoller(BaseModel):
    request_url: Optional[str]
    request_status_code: Optional[int]
    log_message: Optional[str]
    timestamp: datetime
