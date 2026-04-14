"""Content domain service."""

from app.core.exceptions import AppException
from app.repositories.sqlalchemy_repo import repo


def list_items(keyword: str | None) -> list[dict]:
    """List content items by optional keyword."""
    return repo.list_contents(keyword=keyword)


def get_item(item_id: int) -> dict:
    """Get a single content item by id."""
    item = repo.get_content(item_id)
    if not item:
        raise AppException(404, "CONTENT_NOT_FOUND", "Content item does not exist")
    return item
