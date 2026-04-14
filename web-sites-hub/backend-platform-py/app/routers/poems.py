"""Poems router."""

from fastapi import APIRouter, Query

from app.core.response import ok
from app.services import poem_service

router = APIRouter(prefix="/poems", tags=["poems"])


@router.get("")
def list_poems(
    keyword: str | None = Query(default=None, max_length=100),
    category: str | None = Query(default=None, max_length=64),
    dynasty: str | None = Query(default=None, max_length=64),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> dict:
    """List poems with optional filters and pagination."""
    data = poem_service.list_poems(
        keyword=keyword,
        category=category,
        dynasty=dynasty,
        page=page,
        page_size=page_size,
    )
    return ok(data)


@router.get("/meta/categories")
def list_poem_categories() -> dict:
    """List distinct poem categories."""
    categories = poem_service.list_categories()
    return ok(categories)


@router.get("/meta/wordcloud")
def get_poem_wordcloud() -> dict:
    """Get fixed word cloud data for landing page."""
    data = poem_service.get_wordcloud()
    return ok(data)


@router.get("/{poem_id}")
def get_poem(poem_id: int) -> dict:
    """Get one poem by id."""
    poem = poem_service.get_poem(poem_id)
    return ok(poem)

