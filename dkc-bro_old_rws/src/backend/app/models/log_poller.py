from sqlalchemy import Column, DateTime, Integer, String

from app.database.base_class import Base


class LogPoller(Base):
    __tablename__ = "log_poller"

    id = Column(Integer, primary_key=True)
    request_url = Column(String)
    request_status_code = Column(Integer)
    log_message = Column(String)
    timestamp = Column(DateTime)
