"""Invite key router.

Provides endpoints to verify, generate and inspect invite keys.
Ported from backend-resume (Rust/Actix-web).
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.response import ok
from app.dependencies import require_admin_api_key
from app.schemas.invite import GenerateKeyRequest, InviteKeyOut, VerifyKeyRequest
from app.services import invite_service

router = APIRouter(prefix="/invite", tags=["invite"])


def _get_db():
    with SessionLocal() as db:
        yield db


@router.post("/verify")
def verify_invite_key(
    payload: VerifyKeyRequest,
    request: Request,
    db: Session = Depends(_get_db),
) -> dict:
    """Verify and consume an invite key.

    On success the key is marked as used and the pool is replenished
    automatically to maintain the configured minimum.
    """
    client_ip = request.client.host if request.client else ""
    obj = invite_service.verify_key(db, payload.key, visitor_ip=client_ip)
    return ok(InviteKeyOut.model_validate(obj).model_dump(), "验证成功")


@router.post("/generate")
def generate_invite_key(
    payload: GenerateKeyRequest = GenerateKeyRequest(),
    db: Session = Depends(_get_db),
    _: None = Depends(require_admin_api_key),
) -> dict:
    """Manually trigger creation of one new invite key."""
    obj = invite_service.generate_key(db, purpose=payload.purpose, expire_days=payload.expire_days)
    return ok(InviteKeyOut.model_validate(obj).model_dump(), "生成成功")


@router.get("/list")
def list_invite_keys(
    db: Session = Depends(_get_db),
    _: None = Depends(require_admin_api_key),
) -> dict:
    """List all invite keys ordered by creation time descending."""
    keys = invite_service.list_keys(db)
    return ok([InviteKeyOut.model_validate(k).model_dump() for k in keys])


@router.get("/stats")
def invite_stats(
    db: Session = Depends(_get_db),
    _: None = Depends(require_admin_api_key),
) -> dict:
    """Return aggregate statistics for the invite key pool."""
    return ok(invite_service.get_stats(db))
