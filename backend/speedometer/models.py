# models.py
from sqlalchemy import Column, Integer, Float, DateTime
from .database import Base
from datetime import datetime

class SpeedData(Base):
    __tablename__ = "speed_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    speed = Column(Float)

