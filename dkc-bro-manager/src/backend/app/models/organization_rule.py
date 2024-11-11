from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    ForeignKey,
    String,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models import Rule


class OrganizationRule(Base):
    __tablename__ = "organization_rule"

    id = Column(Integer, primary_key=True)
    rule_id = Column(String)
    rule_object_type = Column(String)
    org_id = Column(Integer, ForeignKey("organization.id"))
    name = Column(String)
    importance = Column(Integer)
    explanation = Column(String)
    docstring = Column(String)
    enabled = Column(Boolean, default=True, nullable=False)

    rule = relationship(
        "Rule",
        back_populates="organization_rules",
        foreign_keys=[rule_id, rule_object_type],
    )

    __table_args__ = (
        ForeignKeyConstraint([rule_id, rule_object_type], [Rule.id, Rule.object_type]),
        {},
    )
