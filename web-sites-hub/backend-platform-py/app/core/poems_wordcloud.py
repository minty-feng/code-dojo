"""Word cloud loader for poems module."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

class PoemsWordCloudConstant:
    """Load fixed word cloud words from json files."""

    CATEGORY_ORDER = ["ci", "tang", "song_people", "ci_pai"]

    CATEGORY_META = {
        "ci": {"name": "宋词高频词"},
        "tang": {"name": "唐诗高频词"},
        "song_people": {"name": "宋诗人名云"},
        "ci_pai": {"name": "词牌名词云"},
    }
    DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "wordcloud"
    DEFAULT_COLORS = ["#2f7df6", "#7a63ff", "#00a6d8", "#2aa36b", "#d7881d", "#c95757"]

    @classmethod
    @lru_cache(maxsize=1)
    def load_all(cls) -> dict[str, list[list[int | str]]]:
        """Load all category json files without python expansion."""
        data: dict[str, list[list[int | str]]] = {}
        for key in cls.CATEGORY_ORDER:
            file_path = cls.DATA_DIR / f"{key}.json"
            with file_path.open("r", encoding="utf-8") as fp:
                payload = json.load(fp)
            items = payload.get("items", [])
            data[key] = cls._normalize_items(items)
        return data

    @classmethod
    def _normalize_items(cls, items: list[dict]) -> list[list[int | str]]:
        """Normalize json rows and keep original item count."""
        rows: list[list[int | str]] = []
        for idx, item in enumerate(items):
            rows.append(
                [
                    str(item.get("name", "")).strip() or f"词条{idx + 1}",
                    int(item.get("score", 10)),
                    str(item.get("color") or cls.DEFAULT_COLORS[idx % len(cls.DEFAULT_COLORS)]),
                ]
            )
        return rows

