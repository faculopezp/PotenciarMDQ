"""Estandarización liviana: slug de columnas y CSV -> parquet (Yvera, OurAirports).

El esquema canónico de Yvera se fija cuando se vean las columnas reales (docs/04).
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from potenciar_mdq.settings import PROCESSED, RAW
from potenciar_mdq.standardize.anac_movimientos import _ident, _latest_per_resource, _q, ensure_utf8
from potenciar_mdq.standardize.columns import slug


def csv_to_parquet(src: Path, dest: Path) -> Path:
    con = duckdb.connect()
    utf8 = ensure_utf8(src)
    rel = f"read_csv({_q(str(utf8))}, header=true, sample_size=-1)"
    cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM {rel}").fetchall()]
    renamed = ", ".join(f"{_ident(c)} AS {_ident(slug(c))}" for c in cols)
    dest.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY (SELECT {renamed} FROM {rel}) TO {_q(str(dest))} (FORMAT parquet)")
    return dest


def build_yvera(raw_dir: Path = RAW / "yvera_conectividad") -> list[Path]:
    files = [p for p in raw_dir.rglob("*") if p.suffix.lower() == ".csv"]
    out = []
    for p in _latest_per_resource(files):
        name = slug(p.stem.split("_", 1)[-1])  # quita el prefijo de fecha
        out.append(csv_to_parquet(p, PROCESSED / f"yvera_{name}.parquet"))
    return out


def build_dim_aeropuerto(raw_dir: Path = RAW / "ourairports") -> Path:
    files = sorted(raw_dir.glob("*airports.csv"))
    if not files:
        raise FileNotFoundError(f"No hay airports.csv en {raw_dir}")
    return csv_to_parquet(files[-1], PROCESSED / "dim_aeropuerto.parquet")


def build_clima(raw_dir: Path = RAW / "clima_mdq") -> Path:
    """Open-Meteo (JSON diario) -> processed/clima_diario.parquet."""
    files = sorted(raw_dir.glob("*"))
    if not files:
        raise FileNotFoundError(f"No hay datos de clima en {raw_dir}")
    src = files[-1]
    dest = PROCESSED / "clima_diario.parquet"
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
          SELECT CAST(unnest(daily.time) AS DATE)           AS fecha,
                 unnest(daily.weather_code)::INT            AS codigo_tiempo,
                 unnest(daily.precipitation_sum)            AS precipitacion_mm,
                 unnest(daily.wind_speed_10m_max)           AS viento_max_kmh,
                 unnest(daily.wind_gusts_10m_max)           AS rafaga_max_kmh,
                 unnest(daily.temperature_2m_max)           AS temp_max_c
          FROM read_json({_q(str(src))})
        ) TO {_q(str(dest))} (FORMAT parquet)
        """
    )
    return dest
