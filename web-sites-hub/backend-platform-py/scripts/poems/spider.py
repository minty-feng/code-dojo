"""Spider for fetching raw poems data."""

from __future__ import annotations

import json
import logging
from glob import glob
from datetime import datetime
from pathlib import Path

import requests
import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "sources.yaml"
DEFAULT_RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "poems"
LOGGER = logging.getLogger(__name__)


def load_sources(config_path: Path) -> list[dict]:
    """Load source list from yaml config."""
    content = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    sources = content.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    return sources


def fetch_source(source: dict, timeout_seconds: int = 15) -> list[dict]:
    """Fetch one source URL and return decoded JSON array."""
    source_name = source.get("name", "unknown")
    source_url = source.get("url", "")
    LOGGER.info("fetch_start source=%s url=%s timeout_seconds=%s", source_name, source_url, timeout_seconds)
    response = requests.get(source["url"], timeout=timeout_seconds)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError(f"source {source['name']} did not return JSON list")
    LOGGER.info("fetch_done source=%s records=%s", source_name, len(payload))
    return payload


def _load_local_payload(local_path: Path) -> list[dict]:
    payload = json.loads(local_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"local source {local_path} did not return JSON list")
    return payload


def _resolve_local_files(source: dict) -> list[Path]:
    local_files: list[Path] = []
    local_path = source.get("local_path")
    local_glob = source.get("local_glob")
    if local_path:
        path = Path(local_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"local_path not found: {path}")
        local_files.append(path)
    if local_glob:
        matches = sorted(glob(local_glob, recursive=True))
        local_files.extend([Path(match).resolve() for match in matches if Path(match).is_file()])
    return local_files


def save_raw_payload(source_name: str, payload: list[dict], output_dir: Path) -> Path:
    """Save raw payload to timestamped file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    output_path = output_dir / f"{source_name}__{timestamp}.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def run_spider(config_path: Path = DEFAULT_CONFIG_PATH, output_dir: Path = DEFAULT_RAW_DIR) -> list[Path]:
    """Fetch all enabled sources and save raw json files."""
    output_files: list[Path] = []
    failed_sources: list[str] = []
    for source in load_sources(config_path):
        if not source.get("enabled", True):
            continue
        source_name = source.get("name", "unknown")
        try:
            if source.get("local_path") or source.get("local_glob"):
                local_files = _resolve_local_files(source)
                if not local_files:
                    raise FileNotFoundError(f"no local files matched for source={source_name}")
                LOGGER.info("local_source_detected source=%s files=%s", source_name, len(local_files))
                for local_file in local_files:
                    payload = _load_local_payload(local_file)
                    output_file = save_raw_payload(source_name, payload, output_dir)
                    LOGGER.info("raw_saved source=%s from_local=%s path=%s", source_name, local_file, output_file)
                    output_files.append(output_file)
            else:
                payload = fetch_source(source)
                output_file = save_raw_payload(source_name, payload, output_dir)
                LOGGER.info("raw_saved source=%s path=%s", source_name, output_file)
                output_files.append(output_file)
        except requests.RequestException as exc:
            LOGGER.error("fetch_failed source=%s reason=%s", source_name, exc)
            failed_sources.append(source_name)
        except FileNotFoundError as exc:
            LOGGER.error("local_source_failed source=%s reason=%s", source_name, exc)
            failed_sources.append(source_name)
        except ValueError as exc:
            LOGGER.error("parse_failed source=%s reason=%s", source_name, exc)
            failed_sources.append(source_name)
    if failed_sources:
        LOGGER.warning("spider_partial_success succeeded=%s failed=%s", len(output_files), len(failed_sources))
    if not output_files:
        raise RuntimeError("no raw files fetched; check network or sources.yaml")
    return output_files

