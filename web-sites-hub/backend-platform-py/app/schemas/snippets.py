"""Schemas for snippets APIs."""

from pydantic import BaseModel, Field


class SnippetListQueryRequest(BaseModel):
    """Query payload model for snippets list API."""

    keyword: str | None = Field(default=None, max_length=100)
    lang: str | None = Field(default=None, max_length=32)
    category: str | None = Field(default=None, max_length=64)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)
