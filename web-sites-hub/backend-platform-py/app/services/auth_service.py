"""Auth domain service."""

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.exceptions import AppException
from app.repositories.sqlalchemy_repo import repo


def login(username: str, password: str) -> dict:
    """Validate credentials and return JWT token pair."""
    user = repo.get_user(username)
    if not user or user["password"] != password:
        raise AppException(401, "INVALID_CREDENTIALS", "Invalid username or password")

    return {
        "access_token": create_access_token(username),
        "refresh_token": create_refresh_token(username),
        "token_type": "bearer",
    }


def refresh_token(refresh_token_value: str) -> dict:
    """Refresh access token from valid refresh token."""
    payload = decode_token(refresh_token_value, expected_type="refresh")
    username = payload["sub"]
    return {"access_token": create_access_token(username), "token_type": "bearer"}
