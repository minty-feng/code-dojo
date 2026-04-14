"""Content router."""

from fastapi import APIRouter, Query

from app.core.response import ok
from app.services import content_service

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/items")
def list_items(keyword: str | None = Query(default=None, max_length=100)) -> dict:
    """List content items with optional keyword filter."""
    items = content_service.list_items(keyword)
    return ok(items)


@router.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    """Get one content item by id."""
    item = content_service.get_item(item_id)
    return ok(item)
