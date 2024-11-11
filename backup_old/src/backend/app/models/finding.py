from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database.base_class import Base
from app.models.rule import Rule


class Finding(Base):
    id = Column(Integer, primary_key=True)
    result = Column(Boolean, index=True)
    feedbackMessage = Column(String)
    timestamp = Column(DateTime, index=True)
    filename = Column(String, index=True)
    rule_id = Column(String)
    rule_object_type = Column(String)
    batch_id = Column(String, ForeignKey("batch.id"))
    project_id = Column(Integer, ForeignKey("project.id"))

    rule = relationship(
        "Rule", back_populates="findings", foreign_keys=[rule_id, rule_object_type]
    )
    batch = relationship("Batch", back_populates="findings")
    project = relationship("Project", back_populates="findings")

    __table_args__ = (
        ForeignKeyConstraint([rule_id, rule_object_type], [Rule.id, Rule.object_type]),
        {},
    )
