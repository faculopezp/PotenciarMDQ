"""Muestras para validar a mano -> reports/qa/muestras.md.

Filas concretas (no solo conteos) de los casos dudosos: vuelos oficiales sin modelo, vuelos de
línea 2019–2020 sin aeronave, inferencias aplicadas, taxis reclasificados y la validación de
modelos contra OpenSky por matrícula. Muestras deterministas (orden por hash) para que no
cambien entre corridas si no cambian los datos.
"""

from __future__ import annotations

from pathlib import Path

from potenciar_mdq import bd
from potenciar_mdq.quality import _table
from potenciar_mdq.settings import BD, REPORTS

COLS = """fecha, hora_local, clase_vuelo, clasificacion_vuelo, tipo_movimiento, origen_destino,
          aerolinea_nombre, aeronave, matricula, pasajeros"""


def run(db_path: Path = BD, out_dir: Path = REPORTS / "qa") -> Path:
    con = bd.connect(db_path, read_only=True)
    con.execute("CREATE TEMP VIEW m AS SELECT * FROM fct_movimiento "
                "WHERE aeropuerto = getvariable('foco')")
    out = ["# Muestras para validar — MDQ", ""]

    out += ["## 1. Vuelos oficiales y militares sin modelo de avión (2021+)", "",
            "Perfil del faltante:", "", _table(con, """
        SELECT count(*) AS movimientos,
               count(*) FILTER (aerolinea IS NULL) AS sin_operador,
               count(*) FILTER (es_vuelo_local) AS vuelos_locales,
               count(*) FILTER (pasajeros > 0) AS con_pasajeros,
               count(*) FILTER (matricula IS NOT NULL) AS con_matricula
        FROM m WHERE segmento = 'oficial' AND aeronave IS NULL AND anio >= 2021"""),
        "Orígenes/destinos más frecuentes:", "", _table(con, """
        SELECT origen_destino, count(*) AS movimientos FROM m
        WHERE segmento = 'oficial' AND aeronave IS NULL AND anio >= 2021
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10"""),
        "Operadores informados:", "", _table(con, """
        SELECT aerolinea_nombre, count(*) AS movimientos FROM m
        WHERE segmento = 'oficial' AND aeronave IS NULL AND anio >= 2021
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10"""),
        "Muestra (20 filas):", "", _table(con, f"""
        SELECT {COLS} FROM m WHERE segmento = 'oficial' AND aeronave IS NULL AND anio >= 2021
        ORDER BY hash(movimiento_id) LIMIT 20""")]

    out += ["## 2. Vuelos de línea 2019–2020 sin aeronave, 20 a 96 pasajeros", "",
            "Por operador y familia inferida:", "", _table(con, """
        SELECT anio, aerolinea_nombre, aeronave_familia_inferida, count(*) AS movimientos,
               round(avg(pasajeros), 1) AS pax_promedio, max(pasajeros) AS pax_max
        FROM m WHERE es_linea AND aeronave IS NULL AND anio IN (2019, 2020)
          AND pasajeros BETWEEN 20 AND 96
        GROUP BY ALL ORDER BY anio, movimientos DESC"""),
        "Muestra (20 filas):", "", _table(con, f"""
        SELECT {COLS}, aeronave_familia_inferida FROM m
        WHERE es_linea AND aeronave IS NULL AND anio IN (2019, 2020) AND pasajeros BETWEEN 20 AND 96
        ORDER BY hash(movimiento_id) LIMIT 20""")]

    out += ["## 3. Inferencias aplicadas (config/aeronaves.yaml → inferencia)", "", _table(con, """
        SELECT anio, aerolinea_nombre, aeronave_familia_inferida, count(*) AS movimientos,
               min(pasajeros) AS pax_min, max(pasajeros) AS pax_max
        FROM m WHERE aeronave_inferida GROUP BY ALL ORDER BY anio, movimientos DESC""")]

    out += ["## 3b. Backtest de las reglas (línea 2021+ en el foco, avión conocido)", "",
            "Se aplica cada regla como si no se supiera el avión y se compara con el real.", "",
            _table(con, """
        WITH b AS (
          SELECT m.aeronave_familia AS familia_real, m.aeronave_modelo AS modelo_real, r.*
          FROM m JOIN ref_inferencia_aeronave r
            ON regexp_matches(upper(strip_accents(coalesce(m.aerolinea, ''))), r.operador)
           AND m.pasajeros BETWEEN r.pax_min AND r.pax_max AND m.anio <= r.anio_hasta
          WHERE m.es_linea AND m.aeronave IS NOT NULL AND m.anio >= 2021
        )
        SELECT orden, operador, pax_min, pax_max, modelo AS modelo_inferido, count(*) AS vuelos,
               round(100.0 * count(*) FILTER (familia_real = familia) / count(*), 1)
                 AS pct_acierto_familia,
               round(100.0 * count(*) FILTER (list_contains(modelos_validos, modelo_real))
                     / count(*), 1) AS pct_acierto_modelo
        FROM b GROUP BY ALL ORDER BY orden""")]

    out += ["## 4. Taxi aéreo a pistón con menos de taxi_min_plazas → analizado como privado", "",
            _table(con, """
        SELECT anio, aeronave_modelo, aeronave_plazas, count(*) AS movimientos,
               round(avg(pasajeros), 2) AS pax_promedio, max(pasajeros) AS pax_max
        FROM m WHERE segmento_reclasificado
        GROUP BY ALL ORDER BY anio, movimientos DESC""")]

    out += ["## 5. Modelos estandarizados: denominaciones ANAC por modelo (foco)", "",
            _table(con, """
        SELECT aeronave_modelo, aeronave_icao, count(DISTINCT aeronave) AS denominaciones,
               string_agg(DISTINCT aeronave, ' · ') AS como_figura_en_anac, count(*) AS movimientos
        FROM m WHERE aeronave IS NOT NULL GROUP BY ALL ORDER BY movimientos DESC LIMIT 40""")]

    out += ["## 6. Validación contra OpenSky (matrícula → tipo ICAO, todo el país)", "",
            "Coincidencia del designador ICAO asignado por las reglas con el de OpenSky:", "",
            _table(con, """
        WITH v AS (
          SELECT DISTINCT f.matricula, f.aeronave, f.aeronave_modelo, f.aeronave_icao,
                 upper(o.typecode) AS icao_opensky, o.model AS modelo_opensky
          FROM fct_movimiento f JOIN ref_opensky o ON o.registration = f.matricula
          WHERE f.aeronave_icao IS NOT NULL AND o.typecode IS NOT NULL AND o.typecode <> ''
        )
        SELECT count(*) AS matriculas,
               count(*) FILTER (aeronave_icao = icao_opensky) AS coinciden,
               round(100.0 * count(*) FILTER (aeronave_icao = icao_opensky)
                     / nullif(count(*), 0), 1) AS pct_coinciden
        FROM v"""),
            "Discrepancias (revisar regla o dato de OpenSky):", "", _table(con, """
        WITH v AS (
          SELECT DISTINCT f.matricula, f.aeronave, f.aeronave_modelo, f.aeronave_icao,
                 upper(o.typecode) AS icao_opensky, o.model AS modelo_opensky
          FROM fct_movimiento f JOIN ref_opensky o ON o.registration = f.matricula
          WHERE f.aeronave_icao IS NOT NULL AND o.typecode IS NOT NULL AND o.typecode <> ''
        )
        SELECT aeronave, aeronave_modelo, aeronave_icao, icao_opensky, modelo_opensky,
               count(*) AS matriculas, min(matricula) AS ejemplo
        FROM v WHERE aeronave_icao <> icao_opensky
        GROUP BY ALL ORDER BY matriculas DESC LIMIT 30"""),
            "Tipos ICAO sugeridos por OpenSky para modelos sin designador:", "", _table(con, """
        SELECT f.aeronave_modelo, upper(o.typecode) AS icao_opensky,
               count(DISTINCT f.matricula) AS matriculas
        FROM fct_movimiento f JOIN ref_opensky o ON o.registration = f.matricula
        WHERE f.aeronave_icao IS NULL AND f.aeronave_modelo IS NOT NULL AND o.typecode <> ''
        GROUP BY ALL ORDER BY 3 DESC LIMIT 30""")]

    try:  # esquema de MADHEL todavía no verificado: un error no corta el reporte
        existe = con.execute(
            "SELECT count(*) FROM duckdb_tables() WHERE table_name = 'ref_madhel'")
        if existe.fetchall()[0][0]:
            out += ["## 7. MADHEL (datos.anac.gob.ar/madhel/api/v2/airports/)", "",
                    "Registros: "
                    f"{con.execute('SELECT count(*) FROM ref_madhel').fetchall()[0][0]}", "",
                    "Columnas:", "", _table(con, "SELECT column_name, column_type FROM "
                                                 "(DESCRIBE ref_madhel)"),
                    "Primeras filas:", "",
                    _table(con, "SELECT COLUMNS(*)::VARCHAR FROM ref_madhel LIMIT 3"),
                    "Códigos numéricos del CSV de movimientos encontrados en MADHEL:", "",
                    _table(con, """
                WITH n AS (
                  SELECT origen_destino AS codigo, count(*) AS movimientos FROM fct_movimiento
                  WHERE regexp_matches(origen_destino, '^[0-9]+$') GROUP BY 1
                )
                SELECT n.codigo, n.movimientos, t.human_readable_identifier AS registro_madhel
                FROM n JOIN ref_madhel t
                  ON t.local_identifier = n.codigo
              OR regexp_matches(t.human_readable_identifier, '[(/ ]' || n.codigo || '[)/ ]')
                ORDER BY n.movimientos DESC LIMIT 25""")]
    except Exception as exc:  # noqa: BLE001
        out += ["## 7. MADHEL", "", f"Error explorando MADHEL: `{type(exc).__name__}: {exc}`"]

    con.close()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "muestras.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    return dest
