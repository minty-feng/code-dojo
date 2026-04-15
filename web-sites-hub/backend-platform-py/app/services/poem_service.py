"""Poems domain service."""

from app.core.exceptions import AppException
from app.core.poems_wordcloud import PoemsWordCloudConstant
from app.repositories.sqlalchemy_repo import repo

MAX_PAGE_SIZE = 100


def list_poems(
    keyword: str | None,
    author: str | None,
    tag: str | None,
    category: str | None,
    dynasty: str | None,
    page: int,
    page_size: int,
    sort: str,
) -> dict:
    """List poems with filters and pagination."""
    if page < 1:
        raise AppException(400, "INVALID_PAGE", "page must be greater than or equal to 1")
    if page_size < 1 or page_size > MAX_PAGE_SIZE:
        raise AppException(400, "INVALID_PAGE_SIZE", f"page_size must be between 1 and {MAX_PAGE_SIZE}")
    allowed_sort = {"default", "title_asc", "author_asc", "dynasty_asc"}
    if sort not in allowed_sort:
        raise AppException(400, "INVALID_SORT", f"sort must be one of: {', '.join(sorted(allowed_sort))}")
    return repo.list_poems(
        keyword=keyword,
        author=author,
        tag=tag,
        category=category,
        dynasty=dynasty,
        page=page,
        page_size=page_size,
        sort=sort,
    )


def get_poem(poem_id: int) -> dict:
    """Get one poem by id."""
    poem = repo.get_poem(poem_id)
    if not poem:
        raise AppException(404, "POEM_NOT_FOUND", "Poem does not exist")
    return poem


def list_categories() -> list[str]:
    """List available poem categories."""
    return repo.list_poem_categories()


def list_dynasties() -> list[str]:
    """List distinct poem dynasties for filter UI."""
    return repo.list_poem_dynasties()


def get_wordcloud() -> dict:
    """Return fixed word cloud data grouped by category."""
    data_map = PoemsWordCloudConstant.load_all()
    categories: list[dict] = []
    for key in PoemsWordCloudConstant.CATEGORY_ORDER:
        category_data = data_map.get(key, {})
        categories.append(
            {
                "key": key,
                "name": category_data.get("name", key),
                "words": category_data.get("words", []),
            }
        )
    return {"categories": categories}

