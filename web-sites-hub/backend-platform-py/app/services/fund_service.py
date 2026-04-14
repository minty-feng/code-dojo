"""Fund domain service."""

from app.repositories.sqlalchemy_repo import repo


def list_funds() -> list[dict]:
    """Return fund list."""
    return repo.list_funds()


def export_funds_csv() -> str:
    """Return CSV content as plain text.

    In production this can be changed to file streaming.
    """
    rows = ["code,name,nav,change"]
    for fund in repo.list_funds():
        rows.append(f"{fund['code']},{fund['name']},{fund['nav']},{fund['change']}")
    return "\n".join(rows)
