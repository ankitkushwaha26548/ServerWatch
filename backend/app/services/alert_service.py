from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Alert


def create_alert(
    db: Session,
    api_id: int,
    alert_type: str,
    message: str,
    severity: str = "warning"
):

    existing_alert = (
        db.query(Alert)
        .filter(
            Alert.api_id == api_id,
            Alert.alert_type == alert_type,
            Alert.is_resolved == False
        )
        .first()
    )

    if existing_alert:
        return existing_alert

    alert = Alert(
        api_id=api_id,
        alert_type=alert_type,
        message=message,
        severity=severity,
        is_resolved=False
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def resolve_alerts(
    db: Session,
    api_id: int
):

    alerts = (
        db.query(Alert)
        .filter(
            Alert.api_id == api_id,
            Alert.is_resolved == False
        )
        .all()
    )

    for alert in alerts:

        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()

    db.commit()
    