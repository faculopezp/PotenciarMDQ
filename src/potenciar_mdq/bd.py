"""Construye "nuestra BD" (data/potenciar_mdq.duckdb) desde processed/; exporta a data/bd/.

Orden: macros -> dim_fecha / dim_aerolinea / dim_aeronave (Python) -> dim_aeropuerto, dim_capacidad,
fct_movimiento, fct_tramo, fct_rotacion (sql/bd/*.sql).
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

import duckdb

from potenciar_mdq import dims
from potenciar_mdq.settings import BD, BD_EXPORT, PROCESSED, SQL, mdq

log = logging.getLogger(__name__)

TABLAS = [
    "dim_fecha",
    "dim_aeropuerto",
    "dim_aerolinea",
    "dim_aeronave",
    "dim_capacidad",
    "fct_movimiento",
    "fct_tramo",
    "fct_rotacion",
    "dim_clima",
    "fct_municipal_mensual",
    "fct_mdq_vuelos_hist",
]

OURAIRPORTS_COLS = (
    "ident VARCHAR, type VARCHAR, name VARCHAR, latitude_deg DOUBLE, longitude_deg DOUBLE, "
    "iso_country VARCHAR, iso_region VARCHAR, municipality VARCHAR, gps_code VARCHAR, "
    "iata_code VARCHAR, local_code VARCHAR"
)


def _lit(values: list[str]) -> str:
    return "[" + ", ".join("'" + v.replace("'", "''") + "'" for v in values) + "]"


def set_variables(con: duckdb.DuckDBPyConnection) -> None:
    cfg = mdq()
    con.execute(f"SET VARIABLE foco = '{cfg['foco']['codigo_anac']}'")
    con.execute(f"SET VARIABLE pares = {_lit([p['codigo_anac'] for p in cfg['pares']])}")
    con.execute(f"SET VARIABLE comerciales = {_lit(cfg['clases_comerciales'])}")
    con.execute(f"SET VARIABLE utc_offset = {int(cfg['utc_offset_horas'])}")
    seg = cfg["segmentos"]
    con.execute(f"SET VARIABLE categorias_linea = {_lit(seg['categorias_aeronave_linea'])}")
    con.execute(f"SET VARIABLE operadores_linea = {_lit(seg['tipos_operador_linea'])}")


def connect(path: Path = BD, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(str(path), read_only=read_only)
    set_variables(con)
    return con


def build(processed: Path = PROCESSED, db_path: Path = BD, export: Path | None = BD_EXPORT) -> Path:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    con = connect(db_path)

    con.execute(
        "CREATE TABLE stg_movimiento AS SELECT * FROM read_parquet(?)",
        [str(processed / "stg_movimiento.parquet")],
    )
    oa = processed / "dim_aeropuerto.parquet"
    if oa.exists():
        con.execute("CREATE TABLE ourairports AS SELECT * FROM read_parquet(?)", [str(oa)])
    else:
        log.warning("Sin OurAirports (%s): distancias y coordenadas quedan NULL", oa)
        con.execute(f"CREATE TABLE ourairports ({OURAIRPORTS_COLS})")

    # Portal municipal (opcional): series mensuales 2001+ y vuelos individuales 2015–2019.
    for tabla, archivo, ddl in [
        ("mun_series", "mun_series.parquet",
         "dataset VARCHAR, serie VARCHAR, anio INT, mes INT, valor DOUBLE, unidad VARCHAR, "
         "archivo VARCHAR"),
        ("mun_vuelos_hist", "mun_vuelos_hist.parquet",
         "fecha DATE, hora_local INT, clase_vuelo VARCHAR, tipo_movimiento VARCHAR, "
         "origen_destino_oaci VARCHAR, aerolinea VARCHAR, aeronave VARCHAR, archivo VARCHAR"),
    ]:
        if (processed / archivo).exists():
            con.execute(f"CREATE TABLE {tabla} AS SELECT * FROM read_parquet(?)",
                        [str(processed / archivo)])
        else:
            log.warning("Sin %s: la serie larga queda solo con ANAC", archivo)
            con.execute(f"CREATE TABLE {tabla} ({ddl})")

    clima = processed / "clima_diario.parquet"
    if clima.exists():
        con.execute("CREATE TABLE dim_clima AS SELECT * FROM read_parquet(?)", [str(clima)])
    else:
        con.execute(
            "CREATE TABLE dim_clima (fecha DATE, codigo_tiempo INT, precipitacion_mm DOUBLE, "
            "viento_max_kmh DOUBLE, rafaga_max_kmh DOUBLE, temp_max_c DOUBLE)"
        )

    cfg = mdq()
    con.execute(
        "CREATE TABLE correcciones (de VARCHAR, a VARCHAR, clases VARCHAR[], motivo VARCHAR)"
    )
    for c in cfg.get("correcciones_aeropuerto", []):
        con.execute(
            "INSERT INTO correcciones VALUES (?, ?, ?, ?)",
            [c["de"], c["a"], c["clases"], c["motivo"]],
        )

    [(lo, hi)] = con.execute("SELECT min(fecha), max(fecha) FROM stg_movimiento").fetchall()
    dims.build_dim_fecha(con, date(lo.year, 1, 1), date(hi.year, 12, 31))
    dims.build_dim_aerolinea(con)
    dims.build_dim_aeronave(con)

    for sql_file in sorted((SQL / "bd").glob("*.sql")):
        log.info("bd: %s", sql_file.name)
        con.execute(sql_file.read_text(encoding="utf-8"))

    con.execute("DROP TABLE stg_movimiento")
    con.execute("DROP TABLE mun_series")
    con.execute("DROP TABLE mun_vuelos_hist")
    con.execute("DROP TABLE ourairports")

    if export:
        export.mkdir(parents=True, exist_ok=True)
        for t in TABLAS:
            con.execute(f"COPY {t} TO '{export / f'{t}.parquet'}' (FORMAT parquet)")
    con.close()
    return db_path
