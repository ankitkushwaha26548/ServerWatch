import logging
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, text

from app.core.security import hash_password
from app.database.connection import SessionLocal, engine
from app.database.models import User


logger = logging.getLogger(__name__)


def migrate_user_verification_columns() -> None:
    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    additions = {
        "email_verified": "BOOLEAN NOT NULL DEFAULT FALSE",
        "verification_token_hash": "VARCHAR",
        "verification_token_expires_at": "TIMESTAMP",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(
                    f"ALTER TABLE users ADD COLUMN {name} {definition}"
                ))


def seed_admin_user() -> None:
    email = os.getenv("ADMIN_EMAIL")
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if not all((email, username, password)):
        logger.info("Admin seeding skipped: ADMIN_* variables are incomplete")
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing:
            if existing.role == "ADMIN" and not existing.email_verified:
                existing.email_verified = True
                db.commit()
            logger.info("Configured admin already exists; no account changes made")
            return

        db.add(User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="ADMIN",
        ))
        db.commit()
        logger.info("Configured admin account created")
    except IntegrityError:
        db.rollback()
        logger.info("Configured admin already exists; no account changes made")
    finally:
        db.close()
