"""Users router."""

from fastapi import APIRouter, Depends

from app.core.response import ok
from app.dependencies import get_current_username
from app.schemas.users import UserProfileUpdateRequest
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(username: str = Depends(get_current_username)) -> dict:
    """Get current user profile."""
    profile = user_service.get_me(username)
    return ok(profile)


@router.put("/me")
def update_me(
    payload: UserProfileUpdateRequest,
    username: str = Depends(get_current_username),
) -> dict:
    """Update current user profile."""
    updated = user_service.update_me(username, payload.nickname, payload.bio)
    return ok(updated, "profile updated")
