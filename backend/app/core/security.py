import os

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from jose import JWTError, jwt

import bcrypt


load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "serverwatch-development-secret-change-me"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
):

    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
