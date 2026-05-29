"""Snippets router."""

from fastapi import APIRouter, Query

from app.core.response import ok
from app.services import snippet_service

router = APIRouter(prefix="/snippets", tags=["snippets"])


@router.get("")
def list_snippets(
    keyword: str | None = Query(default=None, max_length=100),
    lang: str | None = Query(default=None, max_length=32),
    category: str | None = Query(default=None, max_length=64),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
) -> dict:
    """List snippets with optional filters and pagination."""
    data = snippet_service.list_snippets(
        keyword=keyword,
        lang=lang,
        category=category,
        page=page,
        page_size=page_size,
    )
    return ok(data)


@router.get("/meta/categories")
def list_snippet_categories() -> dict:
    """List distinct snippet categories."""
    categories = snippet_service.list_categories()
    return ok(categories)


@router.get("/meta/langs")
def list_snippet_langs() -> dict:
    """List distinct snippet languages."""
    langs = snippet_service.list_langs()
    return ok(langs)


@router.get("/{identifier}")
def get_snippet(identifier: str) -> dict:
    """Get one snippet by numeric id or slug."""
    snippet = snippet_service.get_snippet(identifier)
    return ok(snippet)
