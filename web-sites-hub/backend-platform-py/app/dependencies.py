"""Shared dependency functions for routers."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.core.exceptions import AppException

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_username(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Extract current username from Bearer access token."""
    if not credentials or not credentials.credentials:
        raise AppException(401, "UNAUTHORIZED", "Missing bearer token")

    payload = decode_token(credentials.credentials, expected_type="access")
    return payload["sub"]
