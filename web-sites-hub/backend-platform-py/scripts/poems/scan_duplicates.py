"""Scan duplicated poem unique keys in database.

Usage:
  ./.venv/bin/python scripts/poems/scan_duplicates.py --limit 200
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.repositories.sqlalchemy_repo import repo


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan duplicate poem unique keys.")
    parser.add_argument("--limit", type=int, default=200, help="Max duplicate groups to print.")
    args = parser.parse_args()

    rows = repo.scan_duplicate_poem_keys(limit=max(1, args.limit))
    if not rows:
        print("duplicate_groups=0")
        return

    print(f"duplicate_groups={len(rows)}")
    for idx, row in enumerate(rows, start=1):
        title = row["title_simplified"]
        author = row["author_simplified"]
        count = row["count"]
        ids = row["ids"]
        print(f"{idx:04d}. count={count} title={title} author={author} ids={ids}")


if __name__ == "__main__":
    main()

