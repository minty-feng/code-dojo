"""Importer for persisting parsed poems into database."""

from __future__ import annotations

from app.repositories.sqlalchemy_repo import repo


def import_poems(items: list[dict], dry_run: bool = False) -> dict:
    """Import normalized poems into database with upsert strategy."""
    if dry_run:
        return {"inserted": 0, "updated": 0, "total": len(items), "dry_run": True}
    result = repo.upsert_poems(items)
    result["dry_run"] = False
    return result

