from pydantic import BaseModel

class ServerCreate(BaseModel):
    name: str
    hostname: str
    ip_address: str
    operating_system: str

class ServerResponse(BaseModel):
    id: int
    name: str
    hostname: str
    ip_address: str
    operating_system: str
    status: str

    class Config:
        from_attributes = True
        