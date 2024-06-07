# schemas.py
from pydantic import BaseModel
from datetime import datetime

class SpeedDataCreate(BaseModel):
    speed: float

class SpeedData(BaseModel):
    id: int
    timestamp: datetime
    speed: float

    class Config:
        orm_mode = True
