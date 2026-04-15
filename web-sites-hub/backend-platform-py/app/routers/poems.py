"""Poems router."""

from enum import Enum

from fastapi import APIRouter, Query

from app.core.response import ok
from app.services import poem_service

router = APIRouter(prefix="/poems", tags=["poems"])


class PoemListSort(str, Enum):
    default = "default"
    title_asc = "title_asc"
    author_asc = "author_asc"
    dynasty_asc = "dynasty_asc"


@router.get("")
def list_poems(
    keyword: str | None = Query(default=None, max_length=100),
    author: str | None = Query(default=None, max_length=128),
    tag: str | None = Query(default=None, max_length=64),
    category: str | None = Query(default=None, max_length=64),
    dynasty: str | None = Query(default=None, max_length=64),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort: PoemListSort = Query(default=PoemListSort.default),
) -> dict:
    """List poems with optional filters and pagination."""
    data = poem_service.list_poems(
        keyword=keyword,
        author=author,
        tag=tag,
        category=category,
        dynasty=dynasty,
        page=page,
        page_size=page_size,
        sort=sort.value,
    )
    return ok(data)


@router.get("/meta/categories")
def list_poem_categories() -> dict:
    """List distinct poem categories."""
    categories = poem_service.list_categories()
    return ok(categories)


@router.get("/meta/dynasties")
def list_poem_dynasties() -> dict:
    """List distinct poem dynasties for filter dropdowns."""
    dynasties = poem_service.list_dynasties()
    return ok(dynasties)


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

