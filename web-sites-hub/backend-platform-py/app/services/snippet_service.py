"""Snippets domain service."""

from app.core.exceptions import AppException
from app.repositories.sqlalchemy_repo import repo

MAX_PAGE_SIZE = 100


def list_snippets(
    keyword: str | None,
    lang: str | None,
    category: str | None,
    page: int,
    page_size: int,
) -> dict:
    """List published snippets without full code bodies."""
    if page < 1:
        raise AppException(400, "INVALID_PAGE", "page must be greater than or equal to 1")
    if page_size < 1 or page_size > MAX_PAGE_SIZE:
        raise AppException(400, "INVALID_PAGE_SIZE", f"page_size must be between 1 and {MAX_PAGE_SIZE}")
    return repo.list_snippets(
        keyword=keyword,
        lang=lang,
        category=category,
        page=page,
        page_size=page_size,
    )


def get_snippet(identifier: str) -> dict:
    """Get one snippet by numeric id or slug."""
    identifier = identifier.strip()
    if not identifier:
        raise AppException(400, "INVALID_SNIPPET_ID", "snippet identifier is required")

    snippet = None
    if identifier.isdigit():
        snippet = repo.get_snippet(int(identifier))
    if not snippet:
        snippet = repo.get_snippet_by_slug(identifier)
    if not snippet:
        raise AppException(404, "SNIPPET_NOT_FOUND", "Snippet does not exist")
    return snippet


def list_categories() -> list[str]:
    """List distinct snippet categories."""
    return repo.list_snippet_categories()


def list_langs() -> list[str]:
    """List distinct snippet languages."""
    return repo.list_snippet_langs()
