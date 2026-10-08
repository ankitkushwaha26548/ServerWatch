from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import datetime

from app.database.connection import get_db

from app.database.models import (
    ApiEndpoint,
    ApiCheck
)

from app.schemas.api_monitor import (
    ApiCreate,
    ApiResponse,
    ApiCheckResponse
)

from app.services.api_monitor import check_api
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api-monitor",
    tags=["API Monitoring"]
)


@router.post(
    "/",
    response_model=ApiResponse
)
def create_api(
    api: ApiCreate,
    db: Session = Depends(get_db)
):

    new_api = ApiEndpoint(
        name=api.name,
        url=api.url,
        method=api.method.upper()
    )

    db.add(new_api)
    db.commit()
    db.refresh(new_api)

    return new_api


@router.get(
    "/",
    response_model=list[ApiResponse]
)
def get_apis(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    apis = (
        db.query(ApiEndpoint)
        .order_by(ApiEndpoint.id.desc())
        .all()
    )

    return apis


@router.post(
    "/{api_id}/check",
    response_model=ApiCheckResponse
)
def check_monitored_api(
    api_id: int,
    db: Session = Depends(get_db)
):

    api = (
        db.query(ApiEndpoint)
        .filter(
            ApiEndpoint.id == api_id
        )
        .first()
    )

    if not api:
        raise HTTPException(
            status_code=404,
            detail="API endpoint not found"
        )

    result = check_api(api.url)

    new_check = ApiCheck(
        api_id=api.id,
        status_code=result["status_code"],
        response_time=result["response_time"],
        status=result["status"],
        error_message=result["error_message"]
    )

    db.add(new_check)

    api.status = result["status"]
    api.last_status_code = result["status_code"]
    api.last_response_time = result["response_time"]
    api.last_checked = datetime.utcnow()

    db.commit()
    db.refresh(new_check)

    return new_check


@router.get(
    "/{api_id}/history",
    response_model=list[ApiCheckResponse]
)
def get_api_history(
    api_id: int,
    db: Session = Depends(get_db)
):

    api = (
        db.query(ApiEndpoint)
        .filter(
            ApiEndpoint.id == api_id
        )
        .first()
    )

    if not api:
        raise HTTPException(
            status_code=404,
            detail="API endpoint not found"
        )

    checks = (
        db.query(ApiCheck)
        .filter(
            ApiCheck.api_id == api_id
        )
        .order_by(
            ApiCheck.checked_at.desc()
        )
        .limit(100)
        .all()
    )

    return checks