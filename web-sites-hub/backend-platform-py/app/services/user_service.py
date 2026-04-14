"""User domain service."""

from app.core.exceptions import AppException
from app.repositories.sqlalchemy_repo import repo


def get_me(username: str) -> dict:
    """Return current user profile."""
    user = repo.get_user(username)
    if not user:
        raise AppException(404, "USER_NOT_FOUND", "User does not exist")
    return {
        "id": user["id"],
        "username": user["username"],
        "nickname": user["nickname"],
        "bio": user["bio"],
    }


def update_me(username: str, nickname: str, bio: str) -> dict:
    """Update current user profile."""
    updated = repo.update_user_profile(username, nickname, bio)
    if not updated:
        raise AppException(404, "USER_NOT_FOUND", "User does not exist")
    return {
        "id": updated["id"],
        "username": updated["username"],
        "nickname": updated["nickname"],
        "bio": updated["bio"],
    }
