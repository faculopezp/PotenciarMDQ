"""Rutas del proyecto y carga de configuración."""

from __future__ import annotations

from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
MARTS = DATA / "marts"
SQL = ROOT / "sql"
REPORTS = ROOT / "reports"
MANIFEST = RAW / "manifest.jsonl"
BD = DATA / "potenciar_mdq.duckdb"
BD_EXPORT = DATA / "bd"


@cache
def load_yaml(name: str) -> dict:
    with open(CONFIG / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def sources() -> dict:
    return load_yaml("sources.yaml")


def mdq() -> dict:
    return load_yaml("mdq.yaml")
