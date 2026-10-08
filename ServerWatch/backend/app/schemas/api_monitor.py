from pydantic import BaseModel
from datetime import datetime


class ApiCreate(BaseModel):
    name: str
    url: str
    method: str = "GET"


class ApiResponse(BaseModel):
    id: int
    name: str
    url: str
    method: str
    status: str
    last_status_code: int | None
    last_response_time: float | None
    last_checked: datetime | None

    class Config:
        from_attributes = True


class ApiCheckResponse(BaseModel):
    id: int
    api_id: int
    status_code: int | None
    response_time: float | None
    status: str
    error_message: str | None
    checked_at: datetime

    class Config:
        from_attributes = True