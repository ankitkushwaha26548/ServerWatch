from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.database.models import (
    Server,
    ServerLog
)

from app.schemas.log import (
    LogCreate,
    LogResponse
)


router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)

@router.post(
    "/",
    response_model=LogResponse
)
def create_log(
    log: LogCreate,
    db: Session = Depends(get_db)
):

    server = (
        db.query(Server)
        .filter(
            Server.id == log.server_id
        )
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    new_log = ServerLog(
        server_id=log.server_id,
        level=log.level.upper(),
        message=log.message,
        source=log.source
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

@router.get(
    "/{server_id}",
    response_model=list[LogResponse]
)
def get_server_logs(
    server_id: int,
    db: Session = Depends(get_db)
):

    server = (
        db.query(Server)
        .filter(
            Server.id == server_id
        )
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    logs = (
        db.query(ServerLog)
        .filter(
            ServerLog.server_id == server_id
        )
        .order_by(
            ServerLog.timestamp.desc()
        )
        .limit(200)
        .all()
    )

    return logs

@router.get(
    "/{server_id}",
    response_model=list[LogResponse]
)
def get_server_logs(
    server_id: int,
    level: str | None = Query(
        default=None
    ),
    db: Session = Depends(get_db)
):

    server = (
        db.query(Server)
        .filter(
            Server.id == server_id
        )
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    query = (
        db.query(ServerLog)
        .filter(
            ServerLog.server_id == server_id
        )
    )

    if level:

        query = query.filter(
            ServerLog.level == level.upper()
        )

    logs = (
        query
        .order_by(
            ServerLog.timestamp.desc()
        )
        .limit(200)
        .all()
    )

    return logs