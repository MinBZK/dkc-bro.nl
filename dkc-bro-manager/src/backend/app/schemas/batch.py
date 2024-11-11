from pydantic import BaseModel


class BatchBase(BaseModel):
    id: str


class BatchCreate(BatchBase):
    org_id: int


class Batch(BatchBase):
    class Config:
        orm_mode = True
