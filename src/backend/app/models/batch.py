from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Batch(Base):
    id = Column(String, primary_key=True)

    findings = relationship("Finding", back_populates="batch")
