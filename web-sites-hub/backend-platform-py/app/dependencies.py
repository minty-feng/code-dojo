"""Shared dependency functions for routers."""

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.security import decode_token
from app.core.exceptions import AppException

bearer_scheme = HTTPBearer(auto_error=False)


def require_admin_api_key(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")) -> None:
    """Gate invite management APIs with a shared secret header."""
    if not settings.admin_api_key:
        raise AppException(503, "ADMIN_KEY_NOT_CONFIGURED", "Admin API key is not configured on server")
    if not x_admin_key or x_admin_key != settings.admin_api_key:
        raise AppException(403, "FORBIDDEN", "Admin API key required")


def get_current_username(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Extract current username from Bearer access token."""
    if not credentials or not credentials.credentials:
        raise AppException(401, "UNAUTHORIZED", "Missing bearer token")

    payload = decode_token(credentials.credentials, expected_type="access")
    return payload["sub"]
