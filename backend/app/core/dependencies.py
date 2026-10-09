from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.database.models import User

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)


security = HTTPBearer()


def get_current_user(
    credentials:
        HTTPAuthorizationCredentials =
        Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )


    return user