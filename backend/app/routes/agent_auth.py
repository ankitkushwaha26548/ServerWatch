import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Server, ServerAgentCredential
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/servers", tags=["Agent Authentication"])


@router.post("/{server_id}/agent-token")
def generate_agent_token(
    server_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    server = db.query(Server).filter(
        Server.id == server_id
    ).first()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    credential = db.query(ServerAgentCredential).filter(
        ServerAgentCredential.server_id == server_id
    ).first()

    if credential:
        credential.token_hash = token_hash
    else:
        credential = ServerAgentCredential(
            server_id=server_id,
            token_hash=token_hash,
        )
        db.add(credential)

    db.commit()

    # The raw token is returned only now.
    return {
        "server_id": server_id,
        "agent_token": token,
        "message": "Save this token securely. It cannot be retrieved later.",
    }