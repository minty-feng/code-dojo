"""Run spider -> parser -> importer pipeline for poems data."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys

import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.poems.importer import import_poems
from scripts.poems.parser import parse_raw_file
from scripts.poems.spider import DEFAULT_CONFIG_PATH, DEFAULT_RAW_DIR, run_spider
from app.core.database import init_db

LOG_DIR = ROOT_DIR / "data" / "logs"
LOG_FILE = LOG_DIR / "poems_pipeline.log"
LOGGER = logging.getLogger("poems_pipeline")


def _setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler], force=True)


def _load_source_map(config_path: Path) -> dict[str, dict]:
    content = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    sources = content.get("sources", [])
    mapping: dict[str, dict] = {}
    for source in sources:
        name = source.get("name")
        if name:
            mapping[name] = source
    return mapping


def main() -> None:
    _setup_logging()
    # Ensure schema/migrations are applied before importing poems.
    init_db()
    parser = argparse.ArgumentParser(description="Run poems crawl and import pipeline.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to sources yaml file.")
    parser.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR), help="Directory to save/read raw files.")
    parser.add_argument("--skip-crawl", action="store_true", help="Skip spider stage and import latest raw files.")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, do not write database.")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    raw_dir = Path(args.raw_dir).resolve()
    LOGGER.info(
        "pipeline_start config=%s raw_dir=%s skip_crawl=%s dry_run=%s",
        config_path,
        raw_dir,
        args.skip_crawl,
        args.dry_run,
    )
    source_map = _load_source_map(config_path)

    raw_files: list[Path]
    if args.skip_crawl:
        raw_files = sorted(raw_dir.glob("*.json"))
        LOGGER.info("skip_crawl_enabled raw_files=%s", len(raw_files))
    else:
        raw_files = run_spider(config_path=config_path, output_dir=raw_dir)
        LOGGER.info("crawl_done raw_files=%s", len(raw_files))

    parsed_items: list[dict] = []
    for file_path in raw_files:
        if "__" in file_path.name:
            source_name = file_path.name.split("__")[0]
        else:
            source_name = file_path.name.split("-")[0]
        source_cfg = source_map.get(source_name, {})
        parsed = parse_raw_file(
            file_path=file_path,
            source=source_name,
            category=source_cfg.get("category", ""),
            dynasty=source_cfg.get("dynasty", ""),
        )
        parsed_items.extend(parsed)
        LOGGER.info("parse_done file=%s records=%s", file_path.name, len(parsed))

    result = import_poems(parsed_items, dry_run=args.dry_run)
    LOGGER.info(
        "pipeline_done total=%s inserted=%s updated=%s deduplicated=%s dry_run=%s",
        result["total"],
        result["inserted"],
        result["updated"],
        result.get("deduplicated", 0),
        result["dry_run"],
    )
    print(
        f"poems pipeline finished: total={result['total']} inserted={result['inserted']} "
        f"updated={result['updated']} deduplicated={result.get('deduplicated', 0)} "
        f"dry_run={result['dry_run']} log_file={LOG_FILE}"
    )


if __name__ == "__main__":
    main()

