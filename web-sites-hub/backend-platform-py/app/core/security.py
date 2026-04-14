"""JWT security utilities."""

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.core.exceptions import AppException


def _create_token(username: str, token_type: str, expires_delta: timedelta) -> str:
    """Create signed JWT with token type and expiration."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(username: str) -> str:
    """Create access token for API authorization."""
    return _create_token(
        username=username,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_exp_minutes),
    )


def create_refresh_token(username: str) -> str:
    """Create refresh token for access token renewal."""
    return _create_token(
        username=username,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_exp_days),
    )


def decode_token(token: str, expected_type: str | None = None) -> dict:
    """Decode and validate JWT.

    If expected_type is provided, token type must match.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise AppException(401, "TOKEN_EXPIRED", "Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise AppException(401, "UNAUTHORIZED", "Invalid token") from exc

    token_type = payload.get("type")
    username = payload.get("sub")
    if not username or not token_type:
        raise AppException(401, "UNAUTHORIZED", "Malformed token")

    if expected_type and token_type != expected_type:
        raise AppException(401, "UNAUTHORIZED", "Invalid token type")

    return payload
