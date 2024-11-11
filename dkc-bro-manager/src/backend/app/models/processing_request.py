from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models import Rule


class ProcessingRequest(Base):
    __tablename__ = "processing_request"

    id = Column(Integer, primary_key=True)
    rule_id = Column(String)
    rule_object_type = Column(String)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    status = Column(Boolean, nullable=False)
    timestamp = Column(
        DateTime, default=func.now(), server_default=func.now(), nullable=False
    )

    rule = relationship("Rule", back_populates="processing_requests", lazy="joined")
    organization = relationship(
        "Organization", back_populates="processing_requests", lazy="joined"
    )
    __table_args__ = (
        ForeignKeyConstraint([rule_id, rule_object_type], [Rule.id, Rule.object_type]),
        {},
    )
