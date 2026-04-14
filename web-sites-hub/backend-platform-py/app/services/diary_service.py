"""Diary domain service."""

from app.core.exceptions import AppException
from app.repositories.sqlalchemy_repo import repo


def create_entry(title: str, content: str) -> dict:
    """Create a diary entry after basic business validation."""
    if not title.strip():
        raise AppException(400, "DIARY_EMPTY_TITLE", "Diary title cannot be empty")
    return repo.create_diary(title=title.strip(), content=content.strip())


def list_entries() -> list[dict]:
    """List all diary entries."""
    return repo.list_diary()
