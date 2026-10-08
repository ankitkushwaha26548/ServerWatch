from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.database.models import Alert

from app.schemas.alert import (
    AlertResponse
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "/",
    response_model=list[AlertResponse]
)
def get_alerts(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    alerts = (
        db.query(Alert)
        .order_by(
            Alert.created_at.desc()
        )
        .limit(100)
        .all()
    )

    return alerts


@router.get(
    "/active",
    response_model=list[AlertResponse]
)
def get_active_alerts(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    alerts = (
        db.query(Alert)
        .filter(
            Alert.is_resolved == False
        )
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )

    return alerts