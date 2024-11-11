from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="organization")
    rules = relationship(
        "Rule",
        secondary="organization_rule",
        back_populates="organizations",
        lazy="select",
    )
    processing_requests = relationship(
        "ProcessingRequest", back_populates="organization", lazy="select"
    )
    projects = relationship("Project", back_populates="organization", lazy="select")
    batches = relationship("Batch", back_populates="organization", lazy="select")
