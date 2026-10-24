"""Estandarización liviana: slug de columnas y CSV -> parquet (Yvera, OurAirports).

El esquema canónico de Yvera se fija cuando se vean las columnas reales (docs/04).
"""

from __future__ import annotations

import csv
import io
import logging
import re
from pathlib import Path

import duckdb

from potenciar_mdq.settings import PROCESSED, RAW
from potenciar_mdq.standardize.anac_movimientos import _ident, _latest_per_resource, _q, ensure_utf8
from potenciar_mdq.standardize.columns import slug

log = logging.getLogger(__name__)


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


_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_HEMI = re.compile(r"([NSEOW])\s*$", re.I)


def coordenada(texto: str | None, negativa_por_defecto: bool = True) -> float | None:
    """'-34.5594' / '-34,5594' / '34°33'32"S' / '34 33 32 S' -> grados decimales.

    Sin hemisferio explícito en DMS se asume S/O (todo el listado ANAC está en el hemisferio
    sur y al oeste de Greenwich).
    """
    if texto is None:
        return None
    t = str(texto).strip()
    if not t:
        return None
    try:
        return float(t.replace(",", "."))
    except ValueError:
        pass
    nums = [float(n.replace(",", ".")) for n in _NUM.findall(t)][:3]
    if not nums:
        return None
    val = sum(n / 60**i for i, n in enumerate(nums))
    hemi = _HEMI.search(t)
    neg = hemi.group(1).upper() in ("S", "W", "O") if hemi else negativa_por_defecto
    return -val if neg else val


def build_anac_aeropuertos(raw_dir: Path = RAW / "anac_aeropuertos", out: Path = PROCESSED) -> Path:
    """Lista oficial ANAC -> processed/anac_aeropuertos.parquet (código, OACI, IATA, lat, lon)."""
    files = sorted(p for p in raw_dir.rglob("*") if p.is_file())
    if not files:
        raise FileNotFoundError(f"No hay lista de aeropuertos ANAC en {raw_dir}")
    src = files[-1]
    raw = src.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    first = text.splitlines()[0]
    sep = max((";", ",", "\t"), key=first.count)
    filas = list(csv.DictReader(io.StringIO(text), delimiter=sep))
    if not filas:
        raise ValueError(f"{src.name}: vacío")
    cols = {slug(c): c for c in filas[0]}

    def col(*nombres: str) -> str | None:
        return next((cols[n] for n in nombres if n in cols), None)

    c_local, c_oaci, c_iata = (
        col("local", "codigo_local", "cod_local"),
        col("oaci", "icao"),
        col("iata"),
    )
    c_nombre, c_tipo = col("denominacion", "nombre"), col("tipo")
    c_lat, c_lon, c_coord = col("latitud", "lat"), col("longitud", "lon"), col("coordenadas")
    c_prov = col("provincia")
    if not c_local:
        raise ValueError(f"{src.name}: sin columna de código local ({list(cols)})")

    registros = []
    for f in filas:
        lat = coordenada(f.get(c_lat)) if c_lat else None
        lon = coordenada(f.get(c_lon)) if c_lon else None
        if (lat is None or lon is None) and c_coord and f.get(c_coord):
            partes = re.split(r"(?<=[NSEOW])\s*[,;]?\s*|\s*[,;]\s*", f[c_coord].strip(), maxsplit=1)
            if len(partes) == 2:
                lat, lon = coordenada(partes[0]), coordenada(partes[1])
        if lat is not None and not (-91 < lat < 0) or lon is not None and not (-180 < lon < 0):
            lat = lon = None  # fuera de Argentina/Antártida: dato roto
        codigo = (f.get(c_local) or "").strip().upper()
        if not codigo:
            continue
        registros.append(
            {
                "codigo": codigo,
                "oaci": (f.get(c_oaci) or "").strip().upper() or None if c_oaci else None,
                "iata": (f.get(c_iata) or "").strip().upper() or None if c_iata else None,
                "nombre": (f.get(c_nombre) or "").strip() or None if c_nombre else None,
                "tipo": (f.get(c_tipo) or "").strip() or None if c_tipo else None,
                "provincia": (f.get(c_prov) or "").strip() or None if c_prov else None,
                "lat": lat,
                "lon": lon,
                "archivo": src.name,
            }
        )
    dest = out / "anac_aeropuertos.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE a (codigo VARCHAR, oaci VARCHAR, iata VARCHAR, nombre VARCHAR, "
        "tipo VARCHAR, provincia VARCHAR, lat DOUBLE, lon DOUBLE, archivo VARCHAR)"
    )
    con.executemany(
        "INSERT INTO a VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [list(r.values()) for r in registros]
    )
    con.execute(
        f"COPY (SELECT * FROM a QUALIFY row_number() OVER (PARTITION BY codigo) = 1) "
        f"TO {_q(str(dest))} (FORMAT parquet)"
    )
    sin = sum(r["lat"] is None for r in registros)
    log.info("anac_aeropuertos: %d códigos, %d sin coordenadas", len(registros), sin)
    return dest
