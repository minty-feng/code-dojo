"""Parser for normalizing raw poems records."""

from __future__ import annotations

import json
from pathlib import Path

from opencc import OpenCC

T2S = OpenCC("t2s")
S2T = OpenCC("s2t")


def _normalize_content(content: str | list[str] | None) -> str:
    if content is None:
        return ""
    if isinstance(content, list):
        return "\n".join([line.strip() for line in content if str(line).strip()])
    return str(content).strip()


def _build_bilingual_content(raw_content: str) -> tuple[str, str]:
    """Build simplified and traditional content from raw text."""
    content_simplified = T2S.convert(raw_content)
    content_traditional = S2T.convert(raw_content)
    return content_simplified, content_traditional


def normalize_record(raw: dict, source: str, category: str, dynasty: str) -> dict | None:
    """Normalize one raw record to unified poem fields."""
    title_raw = str(raw.get("title", "")).strip()
    author = str(raw.get("author", "")).strip()
    content = _normalize_content(raw.get("content") or raw.get("paragraphs"))
    if not title_raw or not author or not content:
        return None
    title_simplified, title_traditional = _build_bilingual_content(title_raw)
    content_simplified, content_traditional = _build_bilingual_content(content)
    return {
        "title": title_simplified,
        "title_simplified": title_simplified,
        "title_traditional": title_traditional,
        "author": author,
        "dynasty": str(raw.get("dynasty", dynasty)).strip(),
        "category": str(raw.get("category", category)).strip(),
        "content_simplified": content_simplified,
        "content_traditional": content_traditional,
        "tags": ",".join(raw.get("tags", [])) if isinstance(raw.get("tags"), list) else str(raw.get("tags", "")),
        "source": source,
        "source_url": str(raw.get("source_url", "")),
    }


def parse_raw_file(file_path: Path, source: str, category: str, dynasty: str) -> list[dict]:
    """Parse one raw json file and return normalized poem list."""
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"raw file {file_path} is not JSON list")
    items: list[dict] = []
    for raw in payload:
        if not isinstance(raw, dict):
            continue
        item = normalize_record(raw, source=source, category=category, dynasty=dynasty)
        if item:
            items.append(item)
    return items

