"""Word cloud loader for poems module."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

class PoemsWordCloudConstant:
    """Load fixed word cloud words from json files."""

    CATEGORY_ORDER = ["ci", "shi", "poets", "ci_pai"]
    CATEGORY_FILES = {
        "ci": "ci-keywords.json",
        "shi": "shi-keywords.json",
        "poets": "poets-names.json",
        "ci_pai": "ci-pai-names.json",
    }

    DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "wordcloud"
    DEFAULT_COLORS = ["#2f7df6", "#7a63ff", "#00a6d8", "#2aa36b", "#d7881d", "#c95757"]

    @classmethod
    @lru_cache(maxsize=1)
    def load_all(cls) -> dict[str, dict[str, str | list[list[int | str]]]]:
        """Load and cache all category json files."""
        data: dict[str, dict[str, str | list[list[int | str]]]] = {}
        for key in cls.CATEGORY_ORDER:
            file_name = cls.CATEGORY_FILES.get(key, f"{key}.json")
            file_path = cls.DATA_DIR / file_name
            with file_path.open("r", encoding="utf-8") as fp:
                payload = json.load(fp)
            category_name = str(payload.get("name", "")).strip()
            if not category_name:
                category_name = key
           
            items = payload.get("items", []) if isinstance(payload, dict) else payload
            if not isinstance(items, list):
                items = []
            data[key] = {
                "name": category_name,
                "words": cls._normalize_items(items),
            }
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

