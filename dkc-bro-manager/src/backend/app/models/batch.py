from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Batch(Base):
    id = Column(String, primary_key=True)
    org_id = Column(Integer, ForeignKey("organization.id"))

    findings = relationship("Finding", back_populates="batch")
    organization = relationship("Organization", back_populates="batches")
