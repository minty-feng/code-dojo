"""Schemas for poems APIs."""

from pydantic import BaseModel, Field


class PoemListQueryRequest(BaseModel):
    """Query payload model for poems list API."""

    keyword: str | None = Field(default=None, max_length=100)
    author: str | None = Field(default=None, max_length=128)
    tag: str | None = Field(default=None, max_length=64)
    category: str | None = Field(default=None, max_length=64)
    dynasty: str | None = Field(default=None, max_length=64)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort: str = Field(default="default")

