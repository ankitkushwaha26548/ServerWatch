from pydantic import BaseModel
from datetime import datetime


class DeploymentCreate(BaseModel):
    version: str
    environment: str
    status: str
    commit_hash: str


class DeploymentResponse(BaseModel):
    id: int
    version: str
    environment: str
    status: str
    commit_hash: str
    deployed_at: datetime

    class Config:
        from_attributes = True