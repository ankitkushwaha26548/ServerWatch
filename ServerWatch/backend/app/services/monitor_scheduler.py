import asyncio

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal

from app.database.models import ApiEndpoint

from app.services.api_monitor import check_api

from app.services.alert_service import (
    create_alert,
    resolve_alerts
)


CHECK_INTERVAL = 30


def monitor_all_apis():

    db: Session = SessionLocal()

    try:

        apis = (
            db.query(ApiEndpoint)
            .all()
        )

        for api in apis:

            result = check_api(api.url)

            api.status = result["status"]

            api.last_status_code = (
                result["status_code"]
            )

            api.last_response_time = (
                result["response_time"]
            )

            from datetime import datetime

            api.last_checked = datetime.utcnow()

            if result["status"] == "down":

                create_alert(
                    db=db,
                    api_id=api.id,
                    alert_type="api_down",
                    message=f"{api.name} is down",
                    severity="critical"
                )

            elif result["status"] == "unhealthy":

                create_alert(
                    db=db,
                    api_id=api.id,
                    alert_type="api_unhealthy",
                    message=(
                        f"{api.name} returned "
                        f"status code "
                        f"{result['status_code']}"
                    ),
                    severity="warning"
                )

            elif (
                result["response_time"]
                and result["response_time"] > 1000
            ):

                create_alert(
                    db=db,
                    api_id=api.id,
                    alert_type="slow_api",
                    message=(
                        f"{api.name} response time "
                        f"is {result['response_time']} ms"
                    ),
                    severity="warning"
                )

            else:

                resolve_alerts(
                    db=db,
                    api_id=api.id
                )

        db.commit()

    except Exception as error:

        print(
            "Monitoring error:",
            error
        )

    finally:

        db.close()


async def monitoring_loop():

    while True:

        print(
            "Running automatic API monitoring..."
        )

        await asyncio.to_thread(
            monitor_all_apis
        )

        await asyncio.sleep(
            CHECK_INTERVAL
        )