"""Diary router."""

from fastapi import APIRouter

from app.core.response import ok
from app.schemas.diary import DiaryCreateRequest
from app.services import diary_service

router = APIRouter(prefix="/diary", tags=["diary"])


@router.post("/entries")
def create_entry(payload: DiaryCreateRequest) -> dict:
    """Create a diary entry."""
    entry = diary_service.create_entry(payload.title, payload.content)
    return ok(entry, "entry created")


@router.get("/entries")
def list_entries() -> dict:
    """List diary entries."""
    entries = diary_service.list_entries()
    return ok(entries)
