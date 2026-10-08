from pydantic import BaseModel
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    api_id: int | None
    alert_type: str
    message: str
    severity: str
    is_resolved: bool
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True
        