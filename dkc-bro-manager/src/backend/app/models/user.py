from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    totp_seed = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)
    org_id = Column(Integer, ForeignKey("organization.id"))

    organization = relationship("Organization", back_populates="users")
