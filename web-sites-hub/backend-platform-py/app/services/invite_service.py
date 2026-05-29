"""Invite key service.

Manages creation, validation and auto-replenishment of invite keys.
Ported from backend-resume (Rust/Actix-web) to Python/FastAPI.
"""

import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import InviteKeyModel, SessionLocal
from app.core.exceptions import AppException


def _utcnow() -> datetime:
    return datetime.utcnow()


def generate_key(
    db: Session,
    purpose: str = "resume_access",
    expire_days: int | None = None,
) -> InviteKeyModel:
    """Generate and persist a single new invite key."""
    if expire_days is None:
        expire_days = settings.invite_key_expire_days
    now = _utcnow()
    obj = InviteKeyModel(
        key=secrets.token_urlsafe(24),
        purpose=purpose,
        created_at=now,
        expires_at=now + timedelta(days=expire_days),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def ensure_minimum_keys(
    db: Session,
    min_count: int | None = None,
    purpose: str = "resume_access",
) -> list[InviteKeyModel]:
    """Generate keys until at least *min_count* valid (unused, non-expired) keys exist.

    Returns the list of newly created keys.
    """
    if min_count is None:
        min_count = settings.invite_key_min_count
    now = _utcnow()
    valid_count = (
        db.query(InviteKeyModel)
        .filter(
            InviteKeyModel.used == False,  # noqa: E712
            InviteKeyModel.expires_at > now,
            InviteKeyModel.purpose == purpose,
        )
        .count()
    )
    created: list[InviteKeyModel] = []
    for _ in range(max(0, min_count - valid_count)):
        created.append(generate_key(db, purpose=purpose))
    return created


def verify_key(db: Session, key: str, visitor_ip: str = "") -> InviteKeyModel:
    """Mark key as used and return the record.

    After consumption, replenish keys to maintain minimum pool.
    Raises AppException on invalid / used / expired key.
    """
    now = _utcnow()
    obj: InviteKeyModel | None = db.query(InviteKeyModel).filter(InviteKeyModel.key == key).first()
    if obj is None:
        raise AppException(404, "INVALID_KEY", "无效的邀请码")
    if obj.used:
        raise AppException(400, "KEY_USED", "邀请码已被使用")
    if obj.expires_at <= now:
        raise AppException(400, "KEY_EXPIRED", "邀请码已过期")

    obj.used = True
    obj.used_at = now
    obj.visitor_ip = visitor_ip or None
    db.commit()
    db.refresh(obj)

    # Replenish pool after consumption.
    ensure_minimum_keys(db, purpose=obj.purpose)
    return obj


def list_keys(db: Session) -> list[InviteKeyModel]:
    """Return all keys ordered by creation time descending."""
    return db.query(InviteKeyModel).order_by(InviteKeyModel.created_at.desc()).all()


def get_stats(db: Session) -> dict:
    """Return aggregate statistics for the invite key pool."""
    now = _utcnow()
    total = db.query(InviteKeyModel).count()
    used = db.query(InviteKeyModel).filter(InviteKeyModel.used == True).count()  # noqa: E712
    expired_unused = (
        db.query(InviteKeyModel)
        .filter(
            InviteKeyModel.used == False,  # noqa: E712
            InviteKeyModel.expires_at <= now,
        )
        .count()
    )
    valid = (
        db.query(InviteKeyModel)
        .filter(
            InviteKeyModel.used == False,  # noqa: E712
            InviteKeyModel.expires_at > now,
        )
        .count()
    )
    return {
        "total": total,
        "used": used,
        "expired_unused": expired_unused,
        "valid": valid,
        "min_pool": settings.invite_key_min_count,
    }


def get_db_session() -> Session:
    """Return a raw session (for use outside request context)."""
    return SessionLocal()
