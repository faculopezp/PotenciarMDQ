"""Ejecuta sql/mart_*.sql sobre la BD (data/potenciar_mdq.duckdb) y escribe data/marts/*.parquet."""

from __future__ import annotations

from pathlib import Path

from potenciar_mdq import bd
from potenciar_mdq.settings import BD, MARTS, SQL


def build(db_path: Path = BD, out: Path = MARTS) -> list[Path]:
    con = bd.connect(db_path, read_only=True)
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"SET VARIABLE marts_dir = '{out}'")
    written = []
    # mart_mdq_turismo lee la serie larga ya escrita: se ordena para que vaya después.
    archivos = sorted(SQL.glob("mart_*.sql"), key=lambda p: (p.stem == "mart_mdq_turismo", p.stem))
    for sql_file in archivos:
        dest = out / f"{sql_file.stem}.parquet"
        query = sql_file.read_text(encoding="utf-8").strip().rstrip(";")
        con.execute(f"COPY ({query}) TO '{dest}' (FORMAT parquet)")
        written.append(dest)
    con.close()
    return written
