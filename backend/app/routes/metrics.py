from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Server, ServerMetric
from app.schemas.metric import MetricCreate, MetricResponse
from app.services.websocket import manager
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.post("/", response_model=MetricResponse)
async def create_metric(
    metric: MetricCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    # Check whether server exists
    server = db.query(Server).filter(
        Server.id == metric.server_id
    ).first()

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    # Create metric
    new_metric = ServerMetric(
        server_id=metric.server_id,
        cpu_usage=metric.cpu_usage,
        memory_usage=metric.memory_usage,
        disk_usage=metric.disk_usage,
        network_sent_mb=metric.network_sent_mb,
        network_received_mb=metric.network_received_mb,
        uptime_seconds=metric.uptime_seconds
    )

    db.add(new_metric)

    # Update server status
    server.status = "online"
    server.last_seen = new_metric.timestamp

    db.commit()

    db.refresh(new_metric)

    await manager.broadcast(
    {
        "type": "metric_update",
        "server_id": new_metric.server_id,
        "metric": {
            "id": new_metric.id,
            "cpu_usage": new_metric.cpu_usage,
            "memory_usage": new_metric.memory_usage,
            "disk_usage": new_metric.disk_usage,
            "network_sent_mb": new_metric.network_sent_mb,
            "network_received_mb": new_metric.network_received_mb,
            "uptime_seconds": new_metric.uptime_seconds,
            "timestamp": new_metric.timestamp.isoformat()
        }
    }
)

    return new_metric


@router.get("/{server_id}", response_model=list[MetricResponse])
def get_server_metrics(
    server_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):
    
    # Check whether server exists
    server = db.query(Server).filter(
        Server.id == server_id
    ).first()

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found"
        )

    metrics = (
        db.query(ServerMetric)
        .filter(ServerMetric.server_id == server_id)
        .order_by(ServerMetric.timestamp.desc())
        .limit(100)
        .all()
    )

    return metrics