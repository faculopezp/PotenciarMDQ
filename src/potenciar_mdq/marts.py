"""Ejecuta sql/mart_*.sql sobre la BD (data/potenciar_mdq.duckdb) y escribe data/marts/*.parquet."""

from __future__ import annotations

from pathlib import Path

from potenciar_mdq import bd
from potenciar_mdq.settings import BD, MARTS, SQL


def build(db_path: Path = BD, out: Path = MARTS) -> list[Path]:
    con = bd.connect(db_path, read_only=True)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for sql_file in sorted(SQL.glob("mart_*.sql")):
        dest = out / f"{sql_file.stem}.parquet"
        query = sql_file.read_text(encoding="utf-8").strip().rstrip(";")
        con.execute(f"COPY ({query}) TO '{dest}' (FORMAT parquet)")
        written.append(dest)
    con.close()
    return written
