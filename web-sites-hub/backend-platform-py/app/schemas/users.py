"""Schemas for user APIs."""

from pydantic import BaseModel, Field


class UserProfileUpdateRequest(BaseModel):
    """Editable user profile fields."""

    nickname: str = Field(..., min_length=1, max_length=50)
    bio: str = Field(default="", max_length=200)
