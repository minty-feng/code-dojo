"""Database setup and ORM models.

This module owns database engine/session initialization and model definitions.
Keeping models centralized makes schema evolution and migration easier.
"""

from datetime import datetime
from pathlib import Path

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, String, Text, UniqueConstraint, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


class UserModel(Base):
    """User table for basic auth and profile information."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128))
    nickname: Mapped[str] = mapped_column(String(64), default="")
    avatar: Mapped[str] = mapped_column(String(64), default="🐼")
    bio: Mapped[str] = mapped_column(String(255), default="")


class ContentModel(Base):
    """Content table for poems/articles and similar resources."""

    __tablename__ = "contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    author: Mapped[str] = mapped_column(String(64))


class FundModel(Base):
    """Fund table for list and export APIs."""

    __tablename__ = "funds"

    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    nav: Mapped[float] = mapped_column(Float)
    change: Mapped[float] = mapped_column(Float)


class DiaryEntryModel(Base):
    """Diary table for user entry records."""

    __tablename__ = "diary_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class PoemModel(Base):
    """Poems table for showcase poetry module."""

    __tablename__ = "poems"
    __table_args__ = (UniqueConstraint("title_simplified", "author_simplified", name="uq_poems_title_author"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_simplified: Mapped[str] = mapped_column(String(255), default="", index=True)
    title_traditional: Mapped[str] = mapped_column(String(255), default="", index=True)
    author_simplified: Mapped[str] = mapped_column(String(128), default="", index=True)
    author_traditional: Mapped[str] = mapped_column(String(128), default="", index=True)
    dynasty: Mapped[str] = mapped_column(String(64), default="", index=True)
    category: Mapped[str] = mapped_column(String(64), default="", index=True)
    content_simplified: Mapped[str] = mapped_column(Text, default="")
    content_traditional: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(String(255), default="")
    source: Mapped[str] = mapped_column(String(128), default="")
    source_url: Mapped[str] = mapped_column(String(512), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True
    )


class SnippetModel(Base):
    """Code snippets table for algorithm and practice code showcase."""

    __tablename__ = "snippets"
    __table_args__ = (UniqueConstraint("slug", name="uq_snippets_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(64), default="", index=True)
    title: Mapped[str] = mapped_column(String(255), default="", index=True)
    file_name: Mapped[str] = mapped_column(String(128), default="", index=True)
    lang: Mapped[str] = mapped_column(String(32), default="cpp", index=True)
    code: Mapped[str] = mapped_column(Text, default="")
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(64), default="", index=True)
    tags: Mapped[str] = mapped_column(String(255), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, index=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True
    )


class InviteKeyModel(Base):
    """Invite key table for access-controlled resume/feature unlocking."""

    __tablename__ = "invite_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    purpose: Mapped[str] = mapped_column(String(64), default="resume_access", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    used: Mapped[bool] = mapped_column(Integer, default=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    visitor_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)


class PoemFavoriteModel(Base):
    """Poem favorites relation table for user-level collection state."""

    __tablename__ = "poem_favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "poem_id", name="uq_poem_favorites_user_poem"),
        Index("idx_poem_favorites_user_deleted_updated", "user_id", "deleted_at", "updated_at"),
        Index("idx_poem_favorites_user_poem", "user_id", "poem_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    poem_id: Mapped[int] = mapped_column(Integer, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)


def _ensure_poems_columns() -> None:
    """Add bilingual poem columns for legacy databases."""
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(poems)")).fetchall()
        if not rows:
            return
        columns = {row[1] for row in rows}
        if "title_simplified" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN title_simplified VARCHAR(255) NOT NULL DEFAULT ''"))
        if "title_traditional" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN title_traditional VARCHAR(255) NOT NULL DEFAULT ''"))
        if "author_simplified" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN author_simplified VARCHAR(128) NOT NULL DEFAULT ''"))
        if "author_traditional" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN author_traditional VARCHAR(128) NOT NULL DEFAULT ''"))
        if "content_simplified" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN content_simplified TEXT NOT NULL DEFAULT ''"))
        if "content_traditional" not in columns:
            conn.execute(text("ALTER TABLE poems ADD COLUMN content_traditional TEXT NOT NULL DEFAULT ''"))
        if "title" in columns:
            conn.execute(
                text(
                    "UPDATE poems SET title_simplified = title "
                    "WHERE title_simplified = '' AND title IS NOT NULL"
                )
            )
            conn.execute(
                text(
                    "UPDATE poems SET title_traditional = title "
                    "WHERE title_traditional = '' AND title IS NOT NULL"
                )
            )
        if "author" in columns:
            conn.execute(
                text(
                    "UPDATE poems SET author_simplified = author "
                    "WHERE author_simplified = '' AND author IS NOT NULL"
                )
            )
            conn.execute(
                text(
                    "UPDATE poems SET author_traditional = author "
                    "WHERE author_traditional = '' AND author IS NOT NULL"
                )
            )
        if "content" in columns:
            conn.execute(
                text(
                    "UPDATE poems SET content_simplified = content "
                    "WHERE content_simplified = '' AND content IS NOT NULL"
                )
            )
            conn.execute(
                text(
                    "UPDATE poems SET content_traditional = content "
                    "WHERE content_traditional = '' AND content IS NOT NULL"
                )
            )


def _ensure_users_columns() -> None:
    """Add optional user profile columns for legacy databases."""
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(users)")).fetchall()
        if not rows:
            return
        columns = {row[1] for row in rows}
        if "avatar" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN avatar VARCHAR(64) NOT NULL DEFAULT '🐼'"))


def _ensure_invite_keys(min_count: int = 3, expire_days: int = 30) -> None:
    """Ensure at least *min_count* valid (unused, non-expired) invite keys exist."""
    import secrets
    from datetime import timedelta

    now = datetime.utcnow()
    with SessionLocal() as db:
        valid_count = (
            db.query(InviteKeyModel)
            .filter(
                InviteKeyModel.used == False,  # noqa: E712
                InviteKeyModel.expires_at > now,
            )
            .count()
        )
        for _ in range(max(0, min_count - valid_count)):
            db.add(
                InviteKeyModel(
                    key=secrets.token_urlsafe(24),
                    purpose="resume_access",
                    created_at=now,
                    expires_at=now + timedelta(days=expire_days),
                )
            )
        db.commit()


def init_db() -> None:
    """Create tables and seed starter data when database is empty."""
    from app.core.snippet_seed import DEFAULT_SNIPPETS

    Base.metadata.create_all(bind=engine)
    _ensure_poems_columns()
    _ensure_users_columns()

    with SessionLocal() as db:
        if db.query(UserModel).count() == 0:
            db.add(UserModel(username="demo", password="demo123", nickname="Minty", avatar="🐼", bio="single service demo"))
        if db.query(ContentModel).count() == 0:
            db.add_all(
                [
                    ContentModel(id=1, title="定风波", type="poem", author="苏轼"),
                    ContentModel(id=2, title="滕王阁序", type="essay", author="王勃"),
                ]
            )
        if db.query(FundModel).count() == 0:
            db.add_all(
                [
                    FundModel(code="000001", name="成长精选", nav=1.234, change=0.21),
                    FundModel(code="000002", name="价值优选", nav=0.978, change=-0.13),
                ]
            )
        if db.query(SnippetModel).count() == 0:
            db.add_all(
                [
                    SnippetModel(
                        slug=item["slug"],
                        title=item["title"],
                        file_name=item["file_name"],
                        lang=item["lang"],
                        code=item["code"],
                        description=item.get("description", ""),
                        category=item.get("category", ""),
                        tags=item.get("tags", ""),
                        sort_order=item.get("sort_order", 0),
                        is_published=True,
                    )
                    for item in DEFAULT_SNIPPETS
                ]
            )
        db.commit()
    _ensure_invite_keys()
