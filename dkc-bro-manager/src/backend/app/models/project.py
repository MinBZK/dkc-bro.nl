from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    project_nr = Column(Integer, comment="project nummer")
    project_name = Column(String, comment="project naam")
    source_holder = Column(String, comment="Bronhouder")
    environment = Column(
        String, index=True, comment="Omgeving waarin de projecten zich bevinden."
    )
    active = Column(Boolean, comment="Actief project")
    timestamp = Column(
        String, comment="Tijdstempel van het toegevoegde projectnummer"
    )
    org_id = Column(Integer, ForeignKey("organization.id", name="fk_project_org_id"))

    findings = relationship("Finding", back_populates="project")
    organization = relationship("Organization", back_populates="projects")
