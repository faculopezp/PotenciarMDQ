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
from potenciar_mdq.settings import BD, BD_EXPORT, DATA, PROCESSED, SQL, mdq

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
    "dim_perfil_familia",
    "dim_clima",
    "fct_municipal_mensual",
    "fct_mdq_vuelos_hist",
    "fct_bus_ruta_anual",
    "fct_bus_turismo",
    "fct_bus_nacional_diario",
    "dim_bus_localidad",
]

# Micros (Yvera "Conectividad terrestre interurbana"): recurso -> columnas, para crear la tabla
# vacía si falta (sql/bd/80_omnibus.sql corre igual).
BUS_STG = {
    "magnitudes_por_ruta": "indice_tiempo INT, par_origen_destino VARCHAR, viajes INT, "
                           "asientos INT, pasajeros INT",
    "magnitudes_por_ruta_dut": "indice_tiempo INT, par_origen_destino VARCHAR, viajes INT, "
                               "asientos INT, pasajeros INT",
    "viajes_asientos_pasajeros": "indice_tiempo DATE, viajes INT, asientos INT, pasajeros INT",
    "viajes_asientos_pasajeros_dut": "indice_tiempo DATE, viajes INT, asientos INT, "
                                     "pasajeros INT",
    "base_microdatos_dut": "indice_tiempo DATE, localidad_origen VARCHAR, "
                           "provincia_origen VARCHAR, localidad_destino VARCHAR, "
                           "provincia_destino VARCHAR, "
                           "ruta_clasificacion VARCHAR, clase_modalidad VARCHAR, asientos INT, "
                           "pasajeros INT",
}

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
    con.execute("SET VARIABLE patron_escuela = ?", [seg["patron_operador_escuela"]])
    perfil = cfg["perfil_aeronave"]
    con.execute(f"SET VARIABLE basico_categorias = {_lit(perfil['basico_categorias'])}")
    con.execute(f"SET VARIABLE basico_min_pax = {int(perfil['basico_min_pax'])}")
    con.execute(f"SET VARIABLE taxi_min_plazas = {int(perfil['taxi_min_plazas'])}")
    con.execute(f"SET VARIABLE taxi_modelos_piston = {_lit(perfil['taxi_modelos_piston_extra'])}")


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

    # Lista oficial ANAC (opcional): resuelve códigos locales que OurAirports no tiene.
    anac_ap = processed / "anac_aeropuertos.parquet"
    if anac_ap.exists():
        con.execute("CREATE TABLE anac_aeropuertos AS SELECT * FROM read_parquet(?)",
                    [str(anac_ap)])
    else:
        log.warning("Sin lista ANAC de aeropuertos: solo OurAirports")
        con.execute("CREATE TABLE anac_aeropuertos (codigo VARCHAR, oaci VARCHAR, iata VARCHAR, "
                    "nombre VARCHAR, tipo VARCHAR, provincia VARCHAR, lat DOUBLE, lon DOUBLE, "
                    "archivo VARCHAR)")

    # OpenSky (opcional): matrícula -> tipo ICAO, para validar modelos (reports/qa/muestras.md).
    tdb = processed / "tar1090.parquet"
    if tdb.exists():
        con.execute("CREATE TABLE ref_tar1090 AS SELECT * FROM read_parquet(?)", [str(tdb)])
    else:
        log.warning("Sin tar1090-db: no se completa el tipo por matrícula")
        con.execute("CREATE TABLE ref_tar1090 (hex VARCHAR, matricula VARCHAR, ident VARCHAR, "
                    "tipo_icao VARCHAR, flags VARCHAR, descripcion VARCHAR)")
    osky = processed / "opensky.parquet"
    if osky.exists():
        con.execute("CREATE TABLE ref_opensky AS SELECT * FROM read_parquet(?)", [str(osky)])
    else:
        con.execute("CREATE TABLE ref_opensky (registration VARCHAR, typecode VARCHAR, "
                    "manufacturername VARCHAR, model VARCHAR)")

    # MADHEL (opcional, esquema a descubrir): se carga tal cual para explorar en reports/qa.
    madhel = processed / "madhel.parquet"
    if madhel.exists():
        try:
            con.execute("CREATE TABLE ref_madhel AS SELECT * FROM read_parquet(?)", [str(madhel)])
        except Exception as exc:  # noqa: BLE001 - fuente exploratoria
            log.warning("MADHEL no se pudo cargar: %s", exc)

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

    # ANAC 2019 de una versión anterior del dataset (con aeronave; la vigente la trae vacía).
    # Exportada por el usuario en 2025: solo el foco. Ver sql/bd/25_recuperacion.sql, punto 7.
    previa = DATA / "reference" / "anac_2019_version_anterior.csv"
    con.execute("CREATE TABLE ref_anac_previa (fecha DATE, hora_utc TIME, aeropuerto VARCHAR, "
                "tipo_movimiento VARCHAR, origen_destino VARCHAR, aerolinea VARCHAR, "
                "aeronave VARCHAR, pasajeros INT)")
    if previa.exists():
        con.execute("""
            INSERT INTO ref_anac_previa
            SELECT strptime("Fecha", '%d/%m/%Y')::DATE, strptime("Hora", '%H:%M:%S')::TIME,
                   "Aeropuerto", lower("Tipo de Movimiento"), "Origen/Destino",
                   nullif(nullif(trim("Aerolinea Nombre"), 'N/A'), '0'),
                   nullif(nullif(trim("Aeronave"), 'N/A'), '0'), try_cast("Pasajeros" AS INT)
            FROM read_csv(?, all_varchar = true)""", [str(previa)])

    # Yvera "Base agregada de frecuencias aéreas" (vuelos, pasajeros y asientos por día, ruta,
    # aerolínea y clase; fuente SIAC/ANAC): solo las rutas del foco. Valida movimientos y da los
    # asientos de cada vuelo (sql/bd/25_recuperacion.sql, punto 8).
    oaci_foco = mdq()["foco"]["oaci"]
    con.execute("CREATE TABLE ref_yvera_frecuencias (fecha DATE, clasificacion_vuelo VARCHAR, "
                "clase_vuelo VARCHAR, aerolinea VARCHAR, origen_oaci VARCHAR, "
                "destino_oaci VARCHAR, pasajeros INT, asientos INT, vuelos INT)")
    for pq in sorted(processed.glob("yvera_*.parquet")):
        cols = {r[0] for r in con.execute("DESCRIBE SELECT * FROM read_parquet(?)",
                                          [str(pq)]).fetchall()}
        if {"origen_oaci", "destino_oaci", "asientos", "vuelos", "aerolinea"} <= cols:
            con.execute("""
                INSERT INTO ref_yvera_frecuencias
                SELECT CAST(indice_tiempo AS DATE), clasificacion_vuelo, clase_vuelo, aerolinea,
                       origen_oaci, destino_oaci, TRY_CAST(pasajeros AS INT),
                       TRY_CAST(asientos AS INT), TRY_CAST(vuelos AS INT)
                FROM read_parquet(?) WHERE origen_oaci = ? OR destino_oaci = ?""",
                [str(pq), oaci_foco, oaci_foco])
            break
    else:
        log.warning("Sin la base agregada de Yvera: no se validan rutas ni asientos por vuelo")

    # Certificados de ANAC (scripts/listados_anac.py): transporte aerocomercial (121/135) y
    # trabajo aéreo (CETA). Marcan qué operadores son taxi aéreo / trabajo aéreo certificados.
    ref = DATA / "reference"
    con.execute("CREATE TABLE ref_certificado_anac (nombre VARCHAR, certificado VARCHAR)")
    for archivo, campo, cert in (("anac_empresas_121_135.csv", "empresa", "121_135"),
                                 ("anac_ceta.csv", "titular", "ceta")):
        if (ref / archivo).exists():
            con.execute(f"INSERT INTO ref_certificado_anac SELECT \"{campo}\", ? "
                        "FROM read_csv(?, all_varchar = true)", [cert, str(ref / archivo)])

    # Consulta pública de Afectación de Aeronaves de ANAC (matrícula -> empresa explotadora, con
    # fecha de afectación); extracción manual, ver data/reference/anac_afectacion_*_log.txt.
    con.execute("CREATE TABLE ref_afectacion (tipo_entidad VARCHAR, entidad VARCHAR, "
                "matricula VARCHAR, marca VARCHAR, modelo VARCHAR, fecha_afectacion DATE, "
                "extraccion DATE)")
    afectaciones = sorted(ref.glob("anac_afectacion_????-??-??.csv"))
    if afectaciones:
        ultima = afectaciones[-1]
        con.execute("""
            INSERT INTO ref_afectacion
            SELECT tipo_entidad, entidad, upper(trim(matricula)), marca, modelo,
                   strptime(fecha_afectacion, '%d/%m/%Y')::DATE, ?::DATE
            FROM read_csv(?, all_varchar = true)""", [ultima.stem[-10:], str(ultima)])
        # Las entidades afectadas también son explotadores certificados.
        con.execute("""
            INSERT INTO ref_certificado_anac
            SELECT DISTINCT entidad, CASE WHEN tipo_entidad LIKE '%TRABAJO%' THEN 'ceta'
                                          ELSE '121_135' END
            FROM ref_afectacion""")

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
    dims.build_refs_recuperacion(con)

    for nombre, cols in BUS_STG.items():
        pq = processed / f"terrestre_{nombre}.parquet"
        if pq.exists():
            con.execute(f"CREATE TABLE stg_bus_{nombre} AS SELECT * FROM read_parquet(?)",
                        [str(pq)])
        else:
            log.warning("Sin %s (Yvera terrestre): la sección de micros queda incompleta", pq.name)
            con.execute(f"CREATE TABLE stg_bus_{nombre} ({cols})")

    for sql_file in sorted((SQL / "bd").glob("*.sql")):
        log.info("bd: %s", sql_file.name)
        con.execute(sql_file.read_text(encoding="utf-8"))

    con.execute("DROP TABLE stg_movimiento")
    con.execute("DROP TABLE mun_series")
    con.execute("DROP TABLE mun_vuelos_hist")
    con.execute("DROP TABLE ourairports")
    con.execute("DROP TABLE anac_aeropuertos")
    con.execute("DROP TABLE stg_bus_base_microdatos_dut")  # ya está en fct_bus_turismo (foco)

    if export:
        export.mkdir(parents=True, exist_ok=True)
        for t in TABLAS:
            con.execute(f"COPY {t} TO '{export / f'{t}.parquet'}' (FORMAT parquet)")
    con.close()
    return db_path
