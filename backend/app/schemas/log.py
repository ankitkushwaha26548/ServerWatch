from pydantic import BaseModel
from datetime import datetime


class LogCreate(BaseModel):
    server_id: int
    level: str
    message: str
    source: str = "agent"


class LogResponse(BaseModel):
    id: int
    server_id: int
    level: str
    message: str
    source: str
    timestamp: datetime

    class Config:
        from_attributes = True