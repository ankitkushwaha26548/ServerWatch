import hashlib
import hmac

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models import ServerAgentCredential


def verify_agent_token(
    server_id: int,
    token: str | None,
    db: Session,
):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing agent token",
        )

    credential = db.query(ServerAgentCredential).filter(
        ServerAgentCredential.server_id == server_id
    ).first()

    if not credential:
        raise HTTPException(
            status_code=401,
            detail="Agent is not registered",
        )

    received_hash = hashlib.sha256(token.encode()).hexdigest()

    if not hmac.compare_digest(
        received_hash,
        credential.token_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid agent token",
        )