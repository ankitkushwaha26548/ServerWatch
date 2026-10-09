from pydantic import BaseModel
from datetime import datetime


class MetricCreate(BaseModel):
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_sent_mb: float
    network_received_mb: float
    uptime_seconds: int


class MetricResponse(BaseModel):
    id: int
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_sent_mb: float
    network_received_mb: float
    uptime_seconds: int
    timestamp: datetime

    class Config:
        from_attributes = True