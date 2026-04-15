"""SQLAlchemy repository implementation.

Repository methods intentionally return plain dict/list so service and router
layers remain storage-agnostic.
"""

from sqlalchemy import func, or_, asc

from app.core.database import ContentModel, DiaryEntryModel, FundModel, PoemModel, SessionLocal, UserModel


class SqlAlchemyRepository:
    """Repository backed by SQLAlchemy and SQLite."""

    def scan_duplicate_poem_keys(self, limit: int = 200) -> list[dict]:
        """Return duplicate (title_simplified, author_simplified) groups."""
        with SessionLocal() as db:
            rows = (
                db.query(
                    PoemModel.title_simplified.label("title_simplified"),
                    PoemModel.author_simplified.label("author_simplified"),
                    func.count(PoemModel.id).label("count"),
                    func.group_concat(PoemModel.id, ",").label("ids"),
                )
                .group_by(PoemModel.title_simplified, PoemModel.author_simplified)
                .having(func.count(PoemModel.id) > 1)
                .order_by(func.count(PoemModel.id).desc())
                .limit(limit)
                .all()
            )
            result: list[dict] = []
            for row in rows:
                ids = [int(x) for x in str(row.ids).split(",") if str(x).strip()]
                result.append(
                    {
                        "title_simplified": row.title_simplified,
                        "author_simplified": row.author_simplified,
                        "count": int(row.count),
                        "ids": ids,
                    }
                )
            return result

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

    def list_poem_dynasties(self) -> list[str]:
        with SessionLocal() as db:
            rows = (
                db.query(PoemModel.dynasty)
                .filter(PoemModel.dynasty != "")
                .distinct()
                .order_by(PoemModel.dynasty.asc())
                .all()
            )
            return [row[0] for row in rows]

    def list_poems(
        self,
        keyword: str | None,
        author: str | None,
        tag: str | None,
        category: str | None,
        dynasty: str | None,
        page: int,
        page_size: int,
        sort: str,
    ) -> dict:
        with SessionLocal() as db:
            query = db.query(PoemModel)
            if keyword:
                like = f"%{keyword}%"
                query = query.filter(
                    or_(
                        PoemModel.title_simplified.like(like),
                        PoemModel.title_traditional.like(like),
                        PoemModel.author_simplified.like(like),
                        PoemModel.author_traditional.like(like),
                        PoemModel.content_simplified.like(like),
                        PoemModel.content_traditional.like(like),
                    )
                )
            if author:
                author_like = f"%{author}%"
                query = query.filter(
                    or_(
                        PoemModel.author_simplified.like(author_like),
                        PoemModel.author_traditional.like(author_like),
                    )
                )
            if tag:
                query = query.filter(PoemModel.tags.like(f"%{tag}%"))
            if category:
                query = query.filter(PoemModel.category == category)
            if dynasty:
                query = query.filter(PoemModel.dynasty == dynasty)

            total = query.with_entities(func.count(PoemModel.id)).scalar() or 0
            offset = (page - 1) * page_size
            title_col = func.coalesce(PoemModel.title_simplified, "")
            if sort == "title_asc":
                query = query.order_by(asc(title_col), PoemModel.id.asc())
            elif sort == "author_asc":
                query = query.order_by(asc(PoemModel.author_simplified), PoemModel.id.asc())
            elif sort == "dynasty_asc":
                query = query.order_by(asc(PoemModel.dynasty), PoemModel.id.asc())
            else:
                query = query.order_by(PoemModel.id.asc())
            rows = query.offset(offset).limit(page_size).all()
            items = [
                {
                    "id": row.id,
                    "title_simplified": row.title_simplified,
                    "title_traditional": row.title_traditional,
                    "author_simplified": row.author_simplified,
                    "author_traditional": row.author_traditional,
                    "dynasty": row.dynasty,
                    "category": row.category,
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
                "title_simplified": row.title_simplified,
                "title_traditional": row.title_traditional,
                "author_simplified": row.author_simplified,
                "author_traditional": row.author_traditional,
                "dynasty": row.dynasty,
                "category": row.category,
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

        def _chunks(values: list[str], size: int) -> list[list[str]]:
            return [values[i:i + size] for i in range(0, len(values), size)]

        with SessionLocal() as db:
            # Step 1: de-duplicate within current import batch by (title_simplified, author_simplified).
            # Keep the last occurrence to make repeated source entries idempotent.
            batch_map: dict[tuple[str, str], dict] = {}
            for item in items:
                key = (item["title_simplified"], item["author_simplified"])
                if key in batch_map:
                    deduplicated += 1
                batch_map[key] = item

            # Step 2: fetch existing rows in chunks to avoid SQLite bind-variable limit.
            # A full-batch IN query can exceed max SQL parameters on large imports.
            authors = list({key[1] for key in batch_map.keys() if key[1]})
            existing_map: dict[tuple[str, str], PoemModel] = {}
            author_batch_size = 800
            for author_batch in _chunks(authors, author_batch_size):
                rows = db.query(PoemModel).filter(PoemModel.author_simplified.in_(author_batch)).all()
                for row in rows:
                    for variant in [row.title_simplified, row.title_traditional]:
                        if variant:
                            existing_map[(variant, row.author_simplified)] = row

            for key, item in batch_map.items():
                row = None
                for variant in [item.get("title_simplified", ""), item.get("title_traditional", "")]:
                    row = existing_map.get((variant, item["author_simplified"]))
                    if row:
                        break
                if row:
                    row.title_simplified = item.get("title_simplified", row.title_simplified)
                    row.title_traditional = item.get("title_traditional", row.title_traditional)
                    row.author_simplified = item.get("author_simplified", row.author_simplified)
                    row.author_traditional = item.get("author_traditional", row.author_traditional)
                    row.dynasty = item.get("dynasty", "")
                    row.category = item.get("category", "")
                    row.content_simplified = item.get("content_simplified", "")
                    row.content_traditional = item.get("content_traditional", "")
                    row.tags = item.get("tags", "")
                    row.source = item.get("source", "")
                    row.source_url = item.get("source_url", "")
                    updated += 1
                else:
                    db.add(
                        PoemModel(
                            title_simplified=item["title_simplified"],
                            title_traditional=item["title_traditional"],
                            author_simplified=item["author_simplified"],
                            author_traditional=item["author_traditional"],
                            dynasty=item.get("dynasty", ""),
                            category=item.get("category", ""),
                            content_simplified=item["content_simplified"],
                            content_traditional=item["content_traditional"],
                            tags=item.get("tags", ""),
                            source=item.get("source", ""),
                            source_url=item.get("source_url", ""),
                        )
                    )
                    inserted += 1
            db.commit()
        return {"inserted": inserted, "updated": updated, "total": len(items), "deduplicated": deduplicated}


repo = SqlAlchemyRepository()
