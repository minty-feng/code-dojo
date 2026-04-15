"""SQLAdmin registration module.

This module exposes a small helper to mount admin views on FastAPI app.
"""

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.core.admin_auth import AdminAuthBackend
from app.core.database import (
    ContentModel,
    DiaryEntryModel,
    FundModel,
    PoemFavoriteModel,
    PoemModel,
    UserModel,
    engine,
)


class UserAdmin(ModelView, model=UserModel):
    """Admin page for user records."""

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [UserModel.id, UserModel.username, UserModel.nickname, UserModel.bio]
    column_searchable_list = [UserModel.username, UserModel.nickname]
    form_columns = [UserModel.username, UserModel.password, UserModel.nickname, UserModel.bio]


class ContentAdmin(ModelView, model=ContentModel):
    """Admin page for content records."""

    name = "Content"
    name_plural = "Contents"
    icon = "fa-solid fa-book"
    column_list = [ContentModel.id, ContentModel.title, ContentModel.type, ContentModel.author]
    column_searchable_list = [ContentModel.title, ContentModel.author]
    form_columns = [ContentModel.title, ContentModel.type, ContentModel.author]


class FundAdmin(ModelView, model=FundModel):
    """Admin page for fund records."""

    name = "Fund"
    name_plural = "Funds"
    icon = "fa-solid fa-coins"
    column_list = [FundModel.code, FundModel.name, FundModel.nav, FundModel.change]
    column_searchable_list = [FundModel.code, FundModel.name]
    form_columns = [FundModel.code, FundModel.name, FundModel.nav, FundModel.change]


class DiaryEntryAdmin(ModelView, model=DiaryEntryModel):
    """Admin page for diary entry records."""

    name = "Diary Entry"
    name_plural = "Diary Entries"
    icon = "fa-solid fa-note-sticky"
    column_list = [DiaryEntryModel.id, DiaryEntryModel.title, DiaryEntryModel.created_at]
    column_searchable_list = [DiaryEntryModel.title]
    form_columns = [DiaryEntryModel.title, DiaryEntryModel.content]


class PoemAdmin(ModelView, model=PoemModel):
    """Admin page for poem records."""

    name = "Poem"
    name_plural = "Poems"
    icon = "fa-solid fa-feather-pointed"
    column_list = [PoemModel.id, PoemModel.title_simplified, PoemModel.author_simplified, PoemModel.dynasty, PoemModel.category]
    column_searchable_list = [PoemModel.title_simplified, PoemModel.title_traditional, PoemModel.author_simplified, PoemModel.author_traditional, PoemModel.category]
    form_columns = [
        PoemModel.title_simplified,
        PoemModel.title_traditional,
        PoemModel.author_simplified,
        PoemModel.author_traditional,
        PoemModel.dynasty,
        PoemModel.category,
        PoemModel.content_simplified,
        PoemModel.content_traditional,
        PoemModel.tags,
        PoemModel.source,
        PoemModel.source_url,
    ]


class PoemFavoriteAdmin(ModelView, model=PoemFavoriteModel):
    """Admin page for poem favorite records."""

    name = "Poem Favorite"
    name_plural = "Poem Favorites"
    icon = "fa-solid fa-heart"
    column_list = [
        PoemFavoriteModel.id,
        PoemFavoriteModel.user_id,
        PoemFavoriteModel.poem_id,
        PoemFavoriteModel.created_at,
        PoemFavoriteModel.updated_at,
        PoemFavoriteModel.deleted_at,
    ]
    column_searchable_list = [PoemFavoriteModel.user_id, PoemFavoriteModel.poem_id]
    form_columns = [
        PoemFavoriteModel.user_id,
        PoemFavoriteModel.poem_id,
        PoemFavoriteModel.created_at,
        PoemFavoriteModel.updated_at,
        PoemFavoriteModel.deleted_at,
    ]


def setup_admin(app: FastAPI) -> None:
    """Attach SQLAdmin to FastAPI app and register model views."""
    admin = Admin(
        app,
        engine,
        title="Backend Platform Admin",
        authentication_backend=AdminAuthBackend(),
    )
    admin.add_view(UserAdmin)
    admin.add_view(ContentAdmin)
    admin.add_view(FundAdmin)
    admin.add_view(DiaryEntryAdmin)
    admin.add_view(PoemAdmin)
    admin.add_view(PoemFavoriteAdmin)
