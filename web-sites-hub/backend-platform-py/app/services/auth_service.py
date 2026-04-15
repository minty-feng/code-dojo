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


def register(username: str, password: str, nickname: str = "", avatar: str = "🐼") -> dict:
    """Register a new user and return token pair."""
    normalized_username = username.strip()
    normalized_nickname = nickname.strip()
    if not normalized_username:
        raise AppException(400, "INVALID_USERNAME", "Username cannot be empty")
    if " " in normalized_username:
        raise AppException(400, "INVALID_USERNAME", "Username cannot contain spaces")

    exists = repo.get_user(normalized_username)
    if exists:
        raise AppException(409, "USERNAME_ALREADY_EXISTS", "Username already exists")

    repo.create_user(
        username=normalized_username,
        password=password,
        nickname=normalized_nickname or normalized_username,
        avatar=(avatar or "🐼").strip() or "🐼",
        bio="",
    )

    return {
        "access_token": create_access_token(normalized_username),
        "refresh_token": create_refresh_token(normalized_username),
        "token_type": "bearer",
    }
