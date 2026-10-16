import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.database.connection import get_db
from app.database.models import User
from app.schemas.auth import (
    LoginRequest,
    ResendVerificationRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.email_service import send_verification_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
VERIFICATION_HOURS = 24


def _verification_token() -> tuple[str, str, datetime]:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(hours=VERIFICATION_HOURS)
    return token, token_hash, expires_at


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if not os.getenv("SMTP_HOST"):
        raise HTTPException(
            status_code=503,
            detail="Email verification is not configured. Set SMTP_* variables first.",
        )

    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    token, token_hash, expires_at = _verification_token()
    try:
        send_verification_email(user_data.email, token)
    except (OSError, RuntimeError, ValueError) as error:
        raise HTTPException(status_code=503, detail=f"Verification email could not be sent: {error}")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="USER",
        email_verified=False,
        verification_token_hash=token_hash,
        verification_token_expires_at=expires_at,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user = db.query(User).filter(User.verification_token_hash == token_hash).first()
    if not user or not user.verification_token_expires_at or user.verification_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification link is invalid or expired")

    user.email_verified = True
    user.verification_token_hash = None
    user.verification_token_expires_at = None
    db.commit()
    return {"message": "Email verified successfully. You can now log in."}


@router.post("/resend-verification")
def resend_verification(request: ResendVerificationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or user.email_verified:
        return {"message": "If the account exists and needs verification, an email was sent."}

    token, token_hash, expires_at = _verification_token()
    try:
        send_verification_email(user.email, token)
    except (OSError, RuntimeError, ValueError) as error:
        raise HTTPException(status_code=503, detail=f"Verification email could not be sent: {error}")
    user.verification_token_hash = token_hash
    user.verification_token_expires_at = expires_at
    db.commit()
    return {"message": "If the account exists and needs verification, an email was sent."}


@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    try:
        password_valid = verify_password(user_data.password, user.hashed_password)
    except ValueError:
        password_valid = False
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
