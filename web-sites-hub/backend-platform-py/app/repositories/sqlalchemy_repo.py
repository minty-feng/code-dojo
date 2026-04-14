"""SQLAlchemy repository implementation.

Repository methods intentionally return plain dict/list so service and router
layers remain storage-agnostic.
"""

from sqlalchemy import func, or_
from opencc import OpenCC

from app.core.database import ContentModel, DiaryEntryModel, FundModel, PoemModel, SessionLocal, UserModel

T2S = OpenCC("t2s")
S2T = OpenCC("s2t")


class SqlAlchemyRepository:
    """Repository backed by SQLAlchemy and SQLite."""

    def _normalize_existing_poem_titles(self, db) -> None:
        rows = db.query(PoemModel).order_by(PoemModel.id.asc()).all()
        for row in rows:
            source_title = row.title_simplified or row.title or ""
            row.title_simplified = T2S.convert(source_title)
            row.title_traditional = S2T.convert(source_title)
        db.commit()

    def get_user(self, username: str) -> dict | None:
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                return None
            return {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "nickname": user.nickname,
                "bio": user.bio,
            }

    def update_user_profile(self, username: str, nickname: str, bio: str) -> dict | None:
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                return None
            user.nickname = nickname
            user.bio = bio
            db.commit()
            db.refresh(user)
            return {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "nickname": user.nickname,
                "bio": user.bio,
            }

    def list_contents(self, keyword: str | None = None) -> list[dict]:
        with SessionLocal() as db:
            query = db.query(ContentModel)
            if keyword:
                query = query.filter(ContentModel.title.contains(keyword))
            rows = query.order_by(ContentModel.id.asc()).all()
            return [{"id": r.id, "title": r.title, "type": r.type, "author": r.author} for r in rows]

    def get_content(self, item_id: int) -> dict | None:
        with SessionLocal() as db:
            row = db.query(ContentModel).filter(ContentModel.id == item_id).first()
            if not row:
                return None
            return {"id": row.id, "title": row.title, "type": row.type, "author": row.author}

    def list_funds(self) -> list[dict]:
        with SessionLocal() as db:
            rows = db.query(FundModel).order_by(FundModel.code.asc()).all()
            return [{"code": r.code, "name": r.name, "nav": r.nav, "change": r.change} for r in rows]

    def create_diary(self, title: str, content: str) -> dict:
        with SessionLocal() as db:
            row = DiaryEntryModel(title=title, content=content)
            db.add(row)
            db.commit()
            db.refresh(row)
            return {
                "id": row.id,
                "title": row.title,
                "content": row.content,
                "created_at": row.created_at.isoformat(),
            }

    def list_diary(self) -> list[dict]:
        with SessionLocal() as db:
            rows = db.query(DiaryEntryModel).order_by(DiaryEntryModel.id.desc()).all()
            return [
                {
                    "id": r.id,
                    "title": r.title,
                    "content": r.content,
                    "created_at": r.created_at.isoformat(),
                }
                for r in rows
            ]

    def list_poems(
        self,
        keyword: str | None,
        category: str | None,
        dynasty: str | None,
        page: int,
        page_size: int,
    ) -> dict:
        with SessionLocal() as db:
            query = db.query(PoemModel)
            if keyword:
                like = f"%{keyword}%"
                query = query.filter(
                    or_(
                        PoemModel.title.like(like),
                        PoemModel.title_simplified.like(like),
                        PoemModel.title_traditional.like(like),
                        PoemModel.author.like(like),
                        PoemModel.content_simplified.like(like),
                        PoemModel.content_traditional.like(like),
                    )
                )
            if category:
                query = query.filter(PoemModel.category == category)
            if dynasty:
                query = query.filter(PoemModel.dynasty == dynasty)

            total = query.with_entities(func.count(PoemModel.id)).scalar() or 0
            offset = (page - 1) * page_size
            rows = (
                query.order_by(PoemModel.id.asc())
                .offset(offset)
                .limit(page_size)
                .all()
            )
            items = [
                {
                    "id": row.id,
                    "title": row.title_simplified or row.title,
                    "title_simplified": row.title_simplified,
                    "title_traditional": row.title_traditional,
                    "author": row.author,
                    "dynasty": row.dynasty,
                    "category": row.category,
                    "content": row.content_simplified,
                    "content_simplified": row.content_simplified,
                    "content_traditional": row.content_traditional,
                    "tags": row.tags,
                    "source": row.source,
                    "source_url": row.source_url,
                }
                for row in rows
            ]
            return {"items": items, "page": page, "page_size": page_size, "total": total}

    def get_poem(self, poem_id: int) -> dict | None:
        with SessionLocal() as db:
            row = db.query(PoemModel).filter(PoemModel.id == poem_id).first()
            if not row:
                return None
            return {
                "id": row.id,
                "title": row.title_simplified or row.title,
                "title_simplified": row.title_simplified,
                "title_traditional": row.title_traditional,
                "author": row.author,
                "dynasty": row.dynasty,
                "category": row.category,
                "content": row.content_simplified,
                "content_simplified": row.content_simplified,
                "content_traditional": row.content_traditional,
                "tags": row.tags,
                "source": row.source,
                "source_url": row.source_url,
            }

    def list_poem_categories(self) -> list[str]:
        with SessionLocal() as db:
            rows = (
                db.query(PoemModel.category)
                .filter(PoemModel.category != "")
                .distinct()
                .order_by(PoemModel.category.asc())
                .all()
            )
            return [row[0] for row in rows]

    def upsert_poems(self, items: list[dict]) -> dict:
        inserted = 0
        updated = 0
        deduplicated = 0
        with SessionLocal() as db:
            # Step 0: normalize existing title fields.
            self._normalize_existing_poem_titles(db)
            # Step 1: de-duplicate within current import batch by (title_simplified, author).
            # Keep the last occurrence to make repeated source entries idempotent.
            batch_map: dict[tuple[str, str], dict] = {}
            for item in items:
                key = (item.get("title_simplified", item["title"]), item["author"])
                if key in batch_map:
                    deduplicated += 1
                batch_map[key] = item

            # Step 2: fetch existing rows once, then update/insert in memory.
            authors = list({key[1] for key in batch_map.keys()})
            title_variants = list(
                {
                    title
                    for item in batch_map.values()
                    for title in [
                        item.get("title", ""),
                        item.get("title_simplified", ""),
                        item.get("title_traditional", ""),
                    ]
                    if title
                }
            )
            existing_rows = (
                db.query(PoemModel)
                .filter(
                    PoemModel.author.in_(authors),
                    or_(
                        PoemModel.title.in_(title_variants),
                        PoemModel.title_simplified.in_(title_variants),
                        PoemModel.title_traditional.in_(title_variants),
                    ),
                )
                .all()
            )
            existing_map: dict[tuple[str, str], PoemModel] = {}
            for row in existing_rows:
                for variant in [row.title, row.title_simplified, row.title_traditional]:
                    if variant:
                        existing_map[(variant, row.author)] = row

            for key, item in batch_map.items():
                row = None
                for variant in [item.get("title", ""), item.get("title_simplified", ""), item.get("title_traditional", "")]:
                    row = existing_map.get((variant, item["author"]))
                    if row:
                        break
                if row:
                    row.title_simplified = item.get("title_simplified", row.title_simplified)
                    row.title_traditional = item.get("title_traditional", row.title_traditional)
                    row.dynasty = item.get("dynasty", "")
                    row.category = item.get("category", "")
                    row.content = item.get("content_simplified", "")
                    row.content_simplified = item.get("content_simplified", "")
                    row.content_traditional = item.get("content_traditional", "")
                    row.tags = item.get("tags", "")
                    row.source = item.get("source", "")
                    row.source_url = item.get("source_url", "")
                    updated += 1
                else:
                    db.add(
                        PoemModel(
                            title=item["title"],
                            title_simplified=item.get("title_simplified", item["title"]),
                            title_traditional=item.get("title_traditional", item["title"]),
                            author=item["author"],
                            dynasty=item.get("dynasty", ""),
                            category=item.get("category", ""),
                            content=item.get("content_simplified", ""),
                            content_simplified=item.get("content_simplified", ""),
                            content_traditional=item.get("content_traditional", ""),
                            tags=item.get("tags", ""),
                            source=item.get("source", ""),
                            source_url=item.get("source_url", ""),
                        )
                    )
                    inserted += 1
            db.commit()
        return {"inserted": inserted, "updated": updated, "total": len(items), "deduplicated": deduplicated}


repo = SqlAlchemyRepository()
