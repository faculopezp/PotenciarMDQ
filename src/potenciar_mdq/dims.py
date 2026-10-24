"""Dimensiones de la BD que necesitan Python (regex de config, calendario de feriados)."""

from __future__ import annotations

import re
import unicodedata
from datetime import date, timedelta

import duckdb
import holidays

from potenciar_mdq.settings import load_yaml, mdq


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().upper().strip()


def classify_aeronave(name: str, cfg: dict) -> tuple[str, str, str]:
    """'BO-737-8Q8' -> ('Boeing', 'Boeing 737', 'jet_fuselaje_angosto')."""
    up = name.upper().strip()
    prefix = up.split("-", 1)[0]
    if prefix in cfg["fabricantes"]:
        fabricante = cfg["fabricantes"][prefix]
    elif " " in up:  # formato "EMBRAER E-190" del portal municipal
        fabricante = up.split()[0].title()
    else:
        fabricante = prefix
    for rule in cfg["categorias"]:
        if re.search(rule["patron"], up):
            familia = next(
                (fam for rx, fam in rule.get("familia_regex", {}).items() if re.search(rx, up)),
                f"{fabricante} (otro)",
            )
            return fabricante, familia, rule["categoria"]
    return fabricante, cfg["default"]["familia"], cfg["default"]["categoria"]


def modelo_aeronave(name: str, cfg: dict, familia: str) -> tuple[str, str | None, bool]:
    """'BO-B737-8SH' -> ('Boeing 737-800', 'B738', False). Sin regla: (familia, None, False)."""
    up = name.upper().strip()
    for m in cfg.get("modelos", []):
        if re.search(m["patron"], up):
            return m["modelo"], (m.get("icao") or None), bool(m.get("biplaza", False))
    return familia, None, False


def classify_aerolinea(name: str, rules: list[dict]) -> tuple[str, str]:
    n = _norm(name)
    for r in rules:
        if re.search(r["patron"], n):
            return (r["nombre"] or name.title()), r["tipo"]
    return name.title(), "otra"


def build_dim_aeronave(con: duckdb.DuckDBPyConnection) -> None:
    cfg = load_yaml("aeronaves.yaml")
    extra = (" UNION SELECT DISTINCT aeronave FROM mun_vuelos_hist WHERE aeronave IS NOT NULL"
             if _existe(con, "mun_vuelos_hist") else "")
    names = [r[0] for r in con.execute(
        "SELECT DISTINCT aeronave FROM stg_movimiento WHERE aeronave IS NOT NULL" + extra
    ).fetchall()]
    rows = []
    for n in names:
        fabricante, familia, categoria = classify_aeronave(n, cfg)
        rows.append((n, fabricante, familia, categoria, *modelo_aeronave(n, cfg, familia)))
    con.execute(
        "CREATE OR REPLACE TABLE dim_aeronave "
        "(aeronave VARCHAR PRIMARY KEY, fabricante VARCHAR, familia VARCHAR, categoria VARCHAR, "
        "modelo VARCHAR, icao_tipo VARCHAR, es_biplaza BOOLEAN)"
    )
    if rows:
        con.executemany("INSERT INTO dim_aeronave VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    inferencia = cfg.get("inferencia", [])
    con.execute(
        "CREATE OR REPLACE TABLE ref_inferencia_aeronave (orden INT, operador VARCHAR, "
        "pax_min DOUBLE, pax_max DOUBLE, familia VARCHAR, categoria VARCHAR)"
    )
    if inferencia:
        con.executemany(
            "INSERT INTO ref_inferencia_aeronave VALUES (?, ?, ?, ?, ?, ?)",
            [(i, r["operador"], r["pax_min"], r["pax_max"], r["familia"], r["categoria"])
             for i, r in enumerate(inferencia)],
        )


def _existe(con: duckdb.DuckDBPyConnection, tabla: str) -> bool:
    return bool(con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [tabla]
    ).fetchall()[0][0])


def build_dim_aerolinea(con: duckdb.DuckDBPyConnection) -> None:
    rules = load_yaml("aerolineas.yaml")["aerolineas"]
    names = [r[0] for r in con.execute(
        "SELECT DISTINCT aerolinea FROM stg_movimiento WHERE aerolinea IS NOT NULL"
    ).fetchall()]
    rows = [(n, *classify_aerolinea(n, rules)) for n in names]
    con.execute(
        "CREATE OR REPLACE TABLE dim_aerolinea "
        "(aerolinea VARCHAR PRIMARY KEY, aerolinea_nombre VARCHAR, aerolinea_tipo VARCHAR)"
    )
    if rows:
        con.executemany("INSERT INTO dim_aerolinea VALUES (?, ?, ?)", rows)


def build_dim_fecha(con: duckdb.DuckDBPyConnection, desde: date, hasta: date) -> None:
    """Calendario con feriados nacionales (paquete `holidays`, incluye feriados puente)."""
    verano = set(mdq()["meses_verano"])
    feriados = holidays.country_holidays("AR", years=range(desde.year, hasta.year + 1))
    rows = []
    d = desde
    while d <= hasta:
        rows.append((d, feriados.get(d)))
        d += timedelta(days=1)
    con.execute("CREATE OR REPLACE TEMP TABLE _f (fecha DATE, feriado VARCHAR)")
    con.executemany("INSERT INTO _f VALUES (?, ?)", rows)
    meses = ", ".join(str(m) for m in sorted(verano))
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_fecha AS
        WITH b AS (
          SELECT fecha, feriado,
                 isodow(fecha) IN (6, 7) OR feriado IS NOT NULL AS es_no_laborable
          FROM _f
        ),
        bloques AS (   -- racha de días no laborables consecutivos (finde largo = racha >= 3)
          SELECT *, sum(CASE WHEN es_no_laborable THEN 0 ELSE 1 END) OVER (ORDER BY fecha) AS grp
          FROM b
        )
        SELECT
          fecha,
          year(fecha) AS anio, month(fecha) AS mes, day(fecha) AS dia,
          quarter(fecha) AS trimestre, weekofyear(fecha) AS semana_iso,
          isodow(fecha) AS dia_semana,
          ['lun','mar','mié','jue','vie','sáb','dom'][isodow(fecha)] AS dia_semana_nombre,
          isodow(fecha) IN (6, 7) AS es_fin_de_semana,
          feriado IS NOT NULL AS es_feriado,
          feriado AS feriado_nombre,
          es_no_laborable,
          es_no_laborable AND count(*) FILTER (es_no_laborable) OVER (PARTITION BY grp) >= 3
            AS es_finde_largo,
          month(fecha) IN ({meses}) AS es_temporada_verano,
          CASE WHEN month(fecha) IN ({meses})
               THEN year(fecha) + CASE WHEN month(fecha) >= 7 THEN 1 ELSE 0 END END
            AS verano_anio,
          month(fecha) = 7 AS es_julio   -- proxy de vacaciones de invierno (fechas varían por año)
        FROM bloques
        ORDER BY fecha
    """)
