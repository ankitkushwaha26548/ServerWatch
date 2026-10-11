from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Server, User
from app.schemas.server import ServerCreate, ServerResponse
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/servers",
    tags=["Servers"]
)

HEARTBEAT_TIMEOUT = timedelta(seconds=30)


def update_server_status(server: Server, now: datetime) -> None:
    last_seen = server.last_seen

    if last_seen is not None and last_seen.tzinfo is not None:
        last_seen = last_seen.astimezone(timezone.utc).replace(tzinfo=None)

    server.status = (
        "online"
        if last_seen is not None and last_seen >= now - HEARTBEAT_TIMEOUT
        else "offline"
    )


@router.post("/", response_model=ServerResponse)
def create_server(
    server: ServerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    
    new_server = Server(
        name=server.name,
        hostname=server.hostname,
        ip_address=server.ip_address,
        operating_system=server.operating_system
    )

    db.add(new_server)
    db.commit()
    db.refresh(new_server)

    return new_server


@router.get("/", response_model=list[ServerResponse])
def get_servers(
    db: Session = Depends(get_db)
):
    servers = db.query(Server).all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for server in servers:
        update_server_status(server, now)

    return servers


@router.get("/{server_id}", response_model=ServerResponse)
def get_server(
    server_id: int,
    db: Session = Depends(get_db)
):
    server = db.query(Server).filter(
        Server.id == server_id
    ).first()

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    update_server_status(server, datetime.now(timezone.utc).replace(tzinfo=None))

    return server


@router.put("/{server_id}", response_model=ServerResponse)
def update_server(
    server_id: int,
    server_data: ServerCreate,
    db: Session = Depends(get_db)
):
    server = db.query(Server).filter(
        Server.id == server_id
    ).first()

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    server.name = server_data.name
    server.hostname = server_data.hostname
    server.ip_address = server_data.ip_address
    server.operating_system = server_data.operating_system

    db.commit()
    db.refresh(server)

    return server


@router.delete("/{server_id}")
def delete_server(
    server_id: int,
    db: Session = Depends(get_db)
):
    server = db.query(Server).filter(
        Server.id == server_id
    ).first()

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    db.delete(server)
    db.commit()

    return {
        "message": "Server deleted successfully"
    }