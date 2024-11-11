from sqlalchemy import Boolean, Column, Integer, String

from app.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    totp_seed = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)
