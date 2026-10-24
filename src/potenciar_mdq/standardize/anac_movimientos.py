"""ANAC "Aterrizajes y despegues": CSVs anuales heterogéneos -> processed/stg_movimiento.parquet.

Formatos reales observados (2023–2026):
- separador `;` (se auto-detecta), UTF-8, fin de línea CRLF, a veces comprimido .gz (espejos)
- Pasajeros/PAX con coma decimal ("199,00") en 2023–2025; enteros en 2026
- Hora "H:MM" o "HH:MM"; fecha "dd/mm/yyyy"
- "0" como "sin dato" en Aerolinea Nombre y Aeronave
"""

from __future__ import annotations

import gzip
import logging
import shutil
from pathlib import Path

import duckdb

from potenciar_mdq.settings import INTERIM, PROCESSED, RAW
from potenciar_mdq.standardize.columns import (
    ANAC_MOVIMIENTOS_ALIASES,
    ANAC_REQUIRED,
    SIN_DATO,
    VOCAB,
    SchemaError,
    map_columns,
)

log = logging.getLogger(__name__)

CANONICAL = [
    "fecha",
    "hora_utc",
    "clase_vuelo",
    "clasificacion_vuelo",
    "tipo_movimiento",
    "aeropuerto",
    "origen_destino",
    "aerolinea",
    "aeronave",
    "matricula",
    "pasajeros",
    "pax_nacional",
    "calidad_dato",
]

CSV_SUFFIXES = (".csv", ".csv.gz", ".txt")


def _open_text(path: Path, encoding: str):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding=encoding)
    return open(path, encoding=encoding)


def ensure_utf8(path: Path, interim_dir: Path = INTERIM) -> Path:
    """Ruta UTF-8 legible por DuckDB: la original si ya lo es, o una copia transcodificada."""
    try:
        with _open_text(path, "utf-8") as f:
            while f.read(1 << 20):
                pass
        return path
    except UnicodeDecodeError:
        name = path.name.removesuffix(".gz")
        out = interim_dir / "utf8" / f"{Path(name).stem}.utf8.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
            with _open_text(path, "latin-1") as src, open(out, "w", encoding="utf-8") as dst:
                shutil.copyfileobj(src, dst)
        return out


def _q(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def _ident(col: str) -> str:
    return '"' + col.replace('"', '""') + '"'


def _slug_sql(expr: str) -> str:
    return (
        f"nullif(trim(regexp_replace(lower(strip_accents(trim({expr}))), '[^a-z0-9]+', '_', 'g'),"
        f" '_'), '')"
    )


def _vocab_sql(expr: str, canon: str) -> str:
    cases = " ".join(f"WHEN {_q(k)} THEN {_q(v)}" for k, v in VOCAB[canon].items())
    s = _slug_sql(expr)
    # Fuera de vocabulario: se conserva el slug para que QA lo reporte.
    return f"CASE {s} {cases} ELSE {s} END"


def _number_sql(c: str) -> str:
    """'1.234,00' / '199,00' / '155' -> BIGINT. Vacío o basura -> NULL."""
    t = f"trim({c})"
    norm = f"CASE WHEN {t} LIKE '%,%' THEN replace(replace({t}, '.', ''), ',', '.') ELSE {t} END"
    return f"CAST(round(try_cast(nullif({norm}, '') AS DOUBLE)) AS BIGINT)"


def _text_sql(c: str) -> str:
    sin_dato = ", ".join(_q(v) for v in SIN_DATO)
    t = f"upper(trim({c}))"
    return f"CASE WHEN {t} IN ({sin_dato}) THEN NULL ELSE {t} END"


def _expr(canon: str, src: str | None) -> str:
    if src is None:
        typ = "BIGINT" if canon in ("pasajeros", "pax_nacional") else "VARCHAR"
        return f"CAST(NULL AS {typ}) AS {canon}"
    c = _ident(src)
    match canon:
        case "fecha":
            fmts = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y", "%Y/%m/%d"]
            tries = ", ".join(f"try_strptime(trim({c}), {_q(f)})" for f in fmts)
            return f"CAST(coalesce({tries}) AS DATE) AS fecha"
        case "hora_utc":
            return (
                f"CAST(coalesce(try_strptime(trim({c}), '%H:%M:%S'),"
                f" try_strptime(trim({c}), '%H:%M')) AS TIME) AS hora_utc"
            )
        case "pasajeros" | "pax_nacional":
            return f"{_number_sql(c)} AS {canon}"
        case "clasificacion_vuelo" | "tipo_movimiento" | "calidad_dato":
            return f"{_vocab_sql(c, canon)} AS {canon}"
        case "clase_vuelo":
            return f"{_slug_sql(c)} AS clase_vuelo"
        case _:
            return f"{_text_sql(c)} AS {canon}"


def _read_csv_sql(path: Path) -> str:
    # Sniffer de DuckDB para el separador: 2023+ usa ';', años previos sin verificar.
    return f"read_csv({_q(str(path))}, all_varchar=true, header=true, sample_size=-1)"


def select_sql(path: Path, columns: list[str], source_name: str | None = None) -> str:
    mapping = map_columns(columns, ANAC_MOVIMIENTOS_ALIASES)
    inverse = {canon: src for src, canon in mapping.items()}
    missing = [c for c in ANAC_REQUIRED if c not in inverse]
    if missing:
        raise SchemaError(f"{path.name}: faltan columnas requeridas {missing}")
    exprs = ",\n  ".join(_expr(c, inverse.get(c)) for c in CANONICAL)
    return (
        f"SELECT\n  {exprs},\n  {_q(source_name or path.name)} AS source_file\n"
        f"FROM {_read_csv_sql(path)}"
    )


def _detect_columns(con: duckdb.DuckDBPyConnection, path: Path) -> list[str]:
    cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM {_read_csv_sql(path)}").fetchall()]
    if len(cols) == 1 and "," in cols[0]:
        raise SchemaError(f"{path.name}: no se detectó el separador ({cols[0][:80]})")
    return cols


def _latest_per_resource(files: list[Path]) -> list[Path]:
    """raw/<source>/<resource_id>/<YYYYMMDD>_<archivo>: quedarse con la descarga más nueva."""
    latest: dict[Path, Path] = {}
    for p in files:
        prev = latest.get(p.parent)
        if prev is None or p.name > prev.name:
            latest[p.parent] = p
    return sorted(latest.values())


def find_csvs(raw_dir: Path) -> list[Path]:
    files = _latest_per_resource(
        [p for p in raw_dir.rglob("*") if p.name.lower().endswith(CSV_SUFFIXES)]
    )
    oficiales = [p for p in files if not p.parent.name.startswith("espejo_")]
    if oficiales and len(oficiales) < len(files):
        log.warning("Hay archivos oficiales: se ignora el espejo para no duplicar años")
        return oficiales
    return files


def build(
    raw_dir: Path = RAW / "anac_movimientos", out: Path = PROCESSED, interim_dir: Path = INTERIM
) -> Path:
    files = find_csvs(raw_dir)
    if not files:
        raise FileNotFoundError(f"No hay CSV en {raw_dir}. Correr `make ingest` primero.")
    con = duckdb.connect()
    selects = []
    for p in files:
        utf8 = ensure_utf8(p, interim_dir)
        cols = _detect_columns(con, utf8)
        log.info("%s: %d columnas", p.name, len(cols))
        selects.append(select_sql(utf8, cols, p.name))

    out.mkdir(parents=True, exist_ok=True)
    dest = out / "stg_movimiento.parquet"
    union = "\nUNION ALL BY NAME\n".join(selects)
    con.execute(
        f"COPY (SELECT * FROM ({union}) ORDER BY fecha, hora_utc) "
        f"TO {_q(str(dest))} (FORMAT parquet)"
    )
    return dest
