"""Poems router."""

from enum import Enum

from fastapi import APIRouter, Depends, Query

from app.core.exceptions import AppException
from app.core.response import ok
from app.dependencies import get_current_username
from app.schemas.poems import PoemFavoriteCreateRequest, PoemFavoriteSyncRequest
from app.services import poem_service

router = APIRouter(prefix="/poems", tags=["poems"])


class PoemListSort(str, Enum):
    default = "default"
    title_asc = "title_asc"
    author_asc = "author_asc"
    dynasty_asc = "dynasty_asc"


class PoemFavoriteSort(str, Enum):
    updated_desc = "updated_desc"
    updated_asc = "updated_asc"
    created_desc = "created_desc"
    created_asc = "created_asc"


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


@router.get("/favorites")
def list_favorites(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort: PoemFavoriteSort = Query(default=PoemFavoriteSort.updated_desc),
    username: str = Depends(get_current_username),
) -> dict:
    """List current user's poem favorites."""
    data = poem_service.list_favorites(username=username, page=page, page_size=page_size, sort=sort.value)
    return ok(data)


@router.post("/favorites")
def add_favorite(payload: PoemFavoriteCreateRequest, username: str = Depends(get_current_username)) -> dict:
    """Add one poem to favorites, idempotently."""
    data = poem_service.add_favorite(username=username, poem_id=payload.poem_id)
    return ok(data)


@router.delete("/favorites/{poem_id}")
def remove_favorite(poem_id: int, username: str = Depends(get_current_username)) -> dict:
    """Remove one poem from favorites, idempotently."""
    data = poem_service.remove_favorite(username=username, poem_id=poem_id)
    return ok(data)


@router.get("/favorites/status")
def favorite_status(poem_ids: str = Query(default=""), username: str = Depends(get_current_username)) -> dict:
    """Get favorite status map for multiple poem ids."""
    ids = []
    if poem_ids.strip():
        try:
            ids = [int(x.strip()) for x in poem_ids.split(",") if x.strip()]
        except ValueError:
            raise AppException(400, "INVALID_POEM_IDS", "poem_ids must be comma-separated integers")
    data = poem_service.favorite_status(username=username, poem_ids=ids)
    return ok({"map": data})


@router.post("/favorites/sync")
def sync_favorites(payload: PoemFavoriteSyncRequest, username: str = Depends(get_current_username)) -> dict:
    """Merge local favorites into server-side favorites."""
    data = poem_service.sync_favorites(username=username, poem_ids=payload.poem_ids)
    return ok(data)


@router.get("/{poem_id}")
def get_poem(poem_id: int) -> dict:
    """Get one poem by id."""
    poem = poem_service.get_poem(poem_id)
    return ok(poem)

