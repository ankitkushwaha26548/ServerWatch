from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.database.models import Deployment

from app.schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)


@router.post(
    "/",
    response_model=DeploymentResponse
)
def create_deployment(
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    new_deployment = Deployment(
        version=deployment_data.version,
        environment=deployment_data.environment,
        status=deployment_data.status.upper(),
        commit_hash=deployment_data.commit_hash
    )

    db.add(new_deployment)

    db.commit()

    db.refresh(new_deployment)

    return new_deployment


@router.get(
    "/",
    response_model=list[DeploymentResponse]
)
def get_deployments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    deployments = (
        db.query(Deployment)
        .order_by(
            Deployment.deployed_at.desc()
        )
        .limit(100)
        .all()
    )

    return deployments


@router.get(
    "/{deployment_id}",
    response_model=DeploymentResponse
)
def get_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    deployment = (
        db.query(Deployment)
        .filter(
            Deployment.id == deployment_id
        )
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    return deployment