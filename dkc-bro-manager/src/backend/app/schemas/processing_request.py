from pydantic import BaseModel

from app.schemas import RuleBase
from app.schemas.organization import OrganizationBase


class ProcessingRequestBase(BaseModel):
    id: int
    rule_id: int
    org_id: int
    status: bool
    rule: RuleBase
    organization: OrganizationBase
