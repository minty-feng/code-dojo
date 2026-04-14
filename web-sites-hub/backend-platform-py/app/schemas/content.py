"""Schemas for content APIs."""

from pydantic import BaseModel, Field


class ContentQuery(BaseModel):
    """Optional query model for content list API."""

    keyword: str | None = Field(default=None, max_length=100)
