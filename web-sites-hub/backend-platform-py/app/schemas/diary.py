"""Schemas for diary APIs."""

from pydantic import BaseModel, Field


class DiaryCreateRequest(BaseModel):
    """Payload for creating a diary entry."""

    title: str = Field(..., min_length=1, max_length=120)
    content: str = Field(..., min_length=1)
