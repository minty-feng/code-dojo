"""Poems domain service."""

from app.core.exceptions import AppException
from app.core.poems_wordcloud import PoemsWordCloudConstant
from app.repositories.sqlalchemy_repo import repo

MAX_PAGE_SIZE = 100
MAX_SYNC_BATCH_SIZE = 500


def _get_user_id(username: str) -> int:
    user = repo.get_user(username)
    if not user:
        raise AppException(404, "USER_NOT_FOUND", "User does not exist")
    return int(user["id"])


def _ensure_poem_exists(poem_id: int) -> None:
    if poem_id < 1:
        raise AppException(400, "INVALID_POEM_ID", "poem_id must be greater than or equal to 1")
    poem = repo.get_poem(poem_id)
    if not poem:
        raise AppException(404, "POEM_NOT_FOUND", "Poem does not exist")


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


def list_favorites(username: str, page: int, page_size: int, sort: str) -> dict:
    """List poem favorites for current user."""
    if page < 1:
        raise AppException(400, "INVALID_PAGE", "page must be greater than or equal to 1")
    if page_size < 1 or page_size > MAX_PAGE_SIZE:
        raise AppException(400, "INVALID_PAGE_SIZE", f"page_size must be between 1 and {MAX_PAGE_SIZE}")
    allowed_sort = {"updated_desc", "updated_asc", "created_desc", "created_asc"}
    if sort not in allowed_sort:
        raise AppException(400, "INVALID_SORT", f"sort must be one of: {', '.join(sorted(allowed_sort))}")
    user_id = _get_user_id(username)
    return repo.list_poem_favorites(user_id=user_id, page=page, page_size=page_size, sort=sort)


def add_favorite(username: str, poem_id: int) -> dict:
    """Favorite one poem with idempotent semantics."""
    _ensure_poem_exists(poem_id)
    user_id = _get_user_id(username)
    return repo.add_poem_favorite(user_id=user_id, poem_id=poem_id)


def remove_favorite(username: str, poem_id: int) -> dict:
    """Remove poem favorite with idempotent semantics."""
    _ensure_poem_exists(poem_id)
    user_id = _get_user_id(username)
    return repo.remove_poem_favorite(user_id=user_id, poem_id=poem_id)


def favorite_status(username: str, poem_ids: list[int]) -> dict[str, bool]:
    """Return favorite status map for requested poem ids."""
    if len(poem_ids) > MAX_SYNC_BATCH_SIZE:
        raise AppException(400, "INVALID_POEM_IDS", f"poem_ids size must be <= {MAX_SYNC_BATCH_SIZE}")
    user_id = _get_user_id(username)
    return repo.get_poem_favorite_status_map(user_id=user_id, poem_ids=poem_ids)


def sync_favorites(username: str, poem_ids: list[int]) -> dict:
    """Merge local favorites into server-side favorites."""
    if len(poem_ids) > MAX_SYNC_BATCH_SIZE:
        raise AppException(400, "INVALID_POEM_IDS", f"poem_ids size must be <= {MAX_SYNC_BATCH_SIZE}")

    normalized_ids = sorted({int(poem_id) for poem_id in poem_ids if int(poem_id) > 0})
    existing_ids = repo.list_existing_poem_ids(normalized_ids)
    missing = [poem_id for poem_id in normalized_ids if poem_id not in existing_ids]
    if missing:
        raise AppException(404, "POEM_NOT_FOUND", f"Poem does not exist: {missing[0]}")

    user_id = _get_user_id(username)
    return repo.sync_poem_favorites(user_id=user_id, poem_ids=normalized_ids)


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

