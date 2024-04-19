from pydantic import BaseModel


class BatchBase(BaseModel):
    id: str


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    class Config:
        orm_mode = True
