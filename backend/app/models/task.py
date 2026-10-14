
from sqlalchemy import Column, DateTime, Integer, String, Time
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    status = Column(String, default="pending", nullable=False)

    actual_started_at = Column(DateTime, nullable=True)
    actual_finished_at = Column(DateTime, nullable=True)
