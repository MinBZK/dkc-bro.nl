from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from app.database.base_class import Base


class Rule(Base):
    id = Column(String, primary_key=True)
    object_type = Column(String, primary_key=True, index=True)
    name = Column(String)
    importance = Column(Integer)
    explanation = Column(String)
    docstring = Column(String)
    ruleType = Column(Integer)
    enabled = Column(Boolean, default=True, nullable=False)

    findings = relationship("Finding", back_populates="rule")
