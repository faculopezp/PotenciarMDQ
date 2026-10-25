"""Auditoría de datos faltantes -> reports/qa/auditoria.md.

Para cada campo: cuánto falta (país y foco, por año) y qué se puede recuperar con un cruce exacto
entre registros, sin suponer nada:

  A. Operador por matrícula: otros vuelos del mismo avión con un único operador informado.
  B. Aeronave por matrícula: otros vuelos del mismo avión con un único modelo informado.
  C. El otro extremo del mismo vuelo (desde 2026, por matrícula): el despegue en el origen y el
     aterrizaje en MDQ son dos registros del mismo vuelo; si uno trae el dato y el otro no.
  D. Portal municipal 2015–2019 ↔ ANAC 2019: mismo día, hora, movimiento, origen/destino y
     aerolínea, con un solo candidato de cada lado (1 a 1).

"Unánime" = todos los registros con dato coinciden (y hay al menos 2). Se informa también la
versión con >= 80 % de consistencia para comparar.
"""

from __future__ import annotations

from pathlib import Path

from potenciar_mdq import bd
from potenciar_mdq.quality import _table
from potenciar_mdq.settings import BD, REPORTS


def _existe(con, tabla: str) -> bool:
    return bool(con.execute(
        "SELECT count(*) FROM duckdb_tables() WHERE table_name = ?", [tabla]).fetchall()[0][0])


def run(db_path: Path = BD, out_dir: Path = REPORTS / "qa") -> Path:
    con = bd.connect(db_path, read_only=True)
    out = ["# Auditoría de datos faltantes", "",
           "Qué falta, qué se puede recuperar con cruces exactos y qué haría falta para el resto.", ""]

    # ── Completitud ─────────────────────────────────────────────────────────────────────────
    completitud = """
        SELECT anio, count(*) AS movimientos,
          round(100.0 * count(*) FILTER (aerolinea_original IS NULL) / count(*), 1) AS pct_sin_operador,
          round(100.0 * count(*) FILTER (aeronave IS NULL) / count(*), 1) AS pct_sin_aeronave,
          round(100.0 * count(*) FILTER (matricula IS NULL) / count(*), 1) AS pct_sin_matricula,
          round(100.0 * count(*) FILTER (pasajeros IS NULL) / count(*), 1) AS pct_sin_pasajeros,
          round(100.0 * count(*) FILTER (hora_utc IS NULL) / count(*), 1) AS pct_sin_hora,
          round(100.0 * count(*) FILTER (origen_destino IS NULL) / count(*), 1) AS pct_sin_od,
          round(100.0 * count(*) FILTER (regexp_matches(origen_destino, '^[0-9]+$')) / count(*), 1)
            AS pct_od_lad
        FROM fct_movimiento {w} GROUP BY anio ORDER BY anio"""
    out += ["## 1. Completitud por año", "", "País:", "", _table(con, completitud.format(w="")),
            "Foco (MDQ):", "",
            _table(con, completitud.format(w="WHERE aeropuerto = getvariable('foco')")),
            "Foco 2021+, por segmento:", "", _table(con, """
        SELECT segmento, count(*) AS movimientos,
          round(100.0 * count(*) FILTER (aerolinea_original IS NULL) / count(*), 1) AS pct_sin_operador,
          round(100.0 * count(*) FILTER (aeronave IS NULL) / count(*), 1) AS pct_sin_aeronave,
          round(100.0 * count(*) FILTER (pasajeros IS NULL) / count(*), 1) AS pct_sin_pasajeros
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND anio >= 2021
        GROUP BY 1 ORDER BY 2 DESC""")]

    # ── A y B: por matrícula ────────────────────────────────────────────────────────────────
    con.execute("""
        CREATE TEMP TABLE por_mat AS
        SELECT matricula,
          count(DISTINCT aerolinea_original) AS operadores, count(aerolinea_original) AS con_operador,
          max(aerolinea_original) AS operador_unico,
          count(DISTINCT aeronave) AS modelos, count(aeronave) AS con_aeronave,
          max(aeronave) AS aeronave_unica
        FROM fct_movimiento WHERE matricula IS NOT NULL GROUP BY 1""")
    for nombre, campo, n, cnt, unico in [
        ("A. Operador por matrícula", "aerolinea_original", "operadores", "con_operador", "operador_unico"),
        ("B. Aeronave por matrícula", "aeronave", "modelos", "con_aeronave", "aeronave_unica"),
    ]:
        out += [f"## 2{nombre[0]}. {nombre[3:]}", "", _table(con, f"""
            SELECT CASE WHEN f.aeropuerto = getvariable('foco') THEN 'MDQ' ELSE 'resto del país' END AS ambito,
              count(*) AS faltan_con_matricula,
              count(*) FILTER (p.{n} = 1 AND p.{cnt} >= 2) AS recuperables_unanime,
              count(*) FILTER (p.{n} >= 1) AS matricula_con_algun_dato
            FROM fct_movimiento f JOIN por_mat p USING (matricula)
            WHERE f.{campo} IS NULL GROUP BY 1 ORDER BY 1"""),
            "Foco, por segmento:", "", _table(con, f"""
            SELECT f.segmento, count(*) AS faltan_con_matricula,
              count(*) FILTER (p.{n} = 1 AND p.{cnt} >= 2) AS recuperables_unanime
            FROM fct_movimiento f JOIN por_mat p USING (matricula)
            WHERE f.{campo} IS NULL AND f.aeropuerto = getvariable('foco')
            GROUP BY 1 ORDER BY 2 DESC"""),
            "Qué se recupera (foco, top 12):", "", _table(con, f"""
            SELECT p.{unico} AS valor_recuperado, count(*) AS movimientos
            FROM fct_movimiento f JOIN por_mat p USING (matricula)
            WHERE f.{campo} IS NULL AND f.aeropuerto = getvariable('foco')
              AND p.{n} = 1 AND p.{cnt} >= 2
            GROUP BY 1 ORDER BY 2 DESC LIMIT 12""")]
    out += ["Comparación con la regla vigente (operador con >= 80 % de consistencia):", "",
            _table(con, """
        SELECT count(*) FILTER (operador_inferido) AS operador_inferido_80,
               count(*) FILTER (operador_inferido AND aeropuerto = getvariable('foco')) AS en_foco
        FROM fct_movimiento""")]
    if _existe(con, "ref_opensky"):
        out += ["Aeronave faltante con matrícula presente en OpenSky (registro externo):", "",
                _table(con, """
            SELECT count(*) AS faltan_con_matricula,
                   count(o.typecode) FILTER (o.typecode <> '') AS con_tipo_en_opensky,
                   count(o.typecode) FILTER (o.typecode <> '' AND f.aeropuerto = getvariable('foco'))
                     AS en_foco
            FROM fct_movimiento f LEFT JOIN ref_opensky o ON o.registration = f.matricula
            WHERE f.aeronave IS NULL AND f.matricula IS NOT NULL""")]

    # ── C: el otro extremo del mismo vuelo ──────────────────────────────────────────────────
    con.execute("""
        CREATE TEMP TABLE pares AS
        WITH m AS (
          SELECT movimiento_id, matricula, aeropuerto, origen_destino, tipo_movimiento, ts_utc,
                 aerolinea_original, aeronave, pasajeros
          FROM fct_movimiento
          WHERE matricula IS NOT NULL AND ts_utc IS NOT NULL AND origen_destino IS NOT NULL
            AND aeropuerto <> origen_destino
        )
        SELECT a.movimiento_id, a.aeropuerto,
               b.aerolinea_original AS op_otro, b.aeronave AS av_otro, b.pasajeros AS pax_otro,
               a.aerolinea_original, a.aeronave, a.pasajeros,
               count(*) OVER (PARTITION BY a.movimiento_id) AS candidatos
        FROM m a JOIN m b
          ON b.matricula = a.matricula AND b.aeropuerto = a.origen_destino
         AND b.origen_destino = a.aeropuerto AND b.tipo_movimiento <> a.tipo_movimiento
         AND ((a.tipo_movimiento = 'aterrizaje' AND b.ts_utc BETWEEN a.ts_utc - INTERVAL 10 HOUR AND a.ts_utc - INTERVAL 10 MINUTE)
           OR (a.tipo_movimiento = 'despegue' AND b.ts_utc BETWEEN a.ts_utc + INTERVAL 10 MINUTE AND a.ts_utc + INTERVAL 10 HOUR))""")
    out += ["## 2C. El otro extremo del mismo vuelo (por matrícula, un solo candidato)", "",
            _table(con, """
        SELECT CASE WHEN aeropuerto = getvariable('foco') THEN 'MDQ' ELSE 'resto del país' END AS ambito,
          count(DISTINCT movimiento_id) AS movimientos_con_par_unico,
          count(*) FILTER (aerolinea_original IS NULL AND op_otro IS NOT NULL) AS operador_recuperable,
          count(*) FILTER (aeronave IS NULL AND av_otro IS NOT NULL) AS aeronave_recuperable,
          count(*) FILTER (pasajeros IS NULL AND pax_otro IS NOT NULL) AS pasajeros_recuperables,
          count(*) FILTER (aeronave IS NOT NULL AND av_otro IS NOT NULL AND aeronave <> av_otro)
            AS aeronave_distinta_en_cada_extremo
        FROM pares WHERE candidatos = 1 GROUP BY 1 ORDER BY 1""")]

    # ── D: portal municipal 2015–2019 ↔ ANAC 2019 ───────────────────────────────────────────
    if _existe(con, "fct_mdq_vuelos_hist"):
        con.execute("""
            CREATE TEMP TABLE mun AS
            SELECT h.*, coalesce(al.aerolinea_nombre, h.aerolinea) AS nombre
            FROM fct_mdq_vuelos_hist h LEFT JOIN dim_aerolinea al ON al.aerolinea = h.aerolinea
            WHERE h.anio = 2019""")
        con.execute("""
            CREATE TEMP TABLE cruce AS
            WITH a AS (
              SELECT movimiento_id, fecha, hora_local, tipo_movimiento, origen_destino,
                     aerolinea_nombre AS nombre, aeronave, segmento
              FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND anio = 2019
            ),
            k AS (
              SELECT a.movimiento_id, a.aeronave, a.segmento, m.aeronave AS av_mun,
                     count(*) OVER (PARTITION BY a.movimiento_id) AS c_anac,
                     count(*) OVER (PARTITION BY m.fecha, m.hora_local, m.tipo_movimiento,
                                                 m.origen_destino, m.nombre, m.aeronave) AS c_mun
              FROM a JOIN mun m
                ON m.fecha = a.fecha AND m.hora_local = a.hora_local
               AND m.tipo_movimiento = a.tipo_movimiento AND m.origen_destino = a.origen_destino
               AND m.nombre = a.nombre
            )
            SELECT * FROM k""")
        out += ["## 2D. Portal municipal 2015–2019 ↔ ANAC 2019 (foco)", "",
                "Claves: fecha, hora local, aterrizaje/despegue, origen/destino y aerolínea.", "",
                _table(con, """
            SELECT (SELECT count(*) FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
                      AND anio = 2019) AS movimientos_anac_2019,
                   (SELECT count(*) FROM mun) AS registros_municipales_2019,
                   (SELECT count(*) FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
                      AND anio = 2019 AND aeronave IS NULL) AS anac_sin_aeronave,
                   count(DISTINCT movimiento_id) FILTER (c_anac = 1 AND c_mun = 1) AS cruces_1_a_1,
                   count(DISTINCT movimiento_id) FILTER (c_anac = 1 AND c_mun = 1 AND aeronave IS NULL
                     AND av_mun IS NOT NULL) AS aeronave_recuperable
            FROM cruce"""),
                "Aeronaves recuperables, por segmento y modelo municipal:", "", _table(con, """
            SELECT segmento, av_mun AS aeronave_municipal, count(*) AS movimientos
            FROM cruce WHERE c_anac = 1 AND c_mun = 1 AND aeronave IS NULL AND av_mun IS NOT NULL
            GROUP BY ALL ORDER BY 3 DESC LIMIT 15""")]

    # ── Lo que no se puede recuperar con lo que hay ────────────────────────────────────────
    out += ["## 3. Sin cruce posible con las fuentes actuales", "", _table(con, """
        SELECT 'Aeronave sin matrícula (2019–2025)' AS caso, count(*) AS movimientos_foco
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND aeronave IS NULL AND matricula IS NULL
        UNION ALL
        SELECT 'Operador sin matrícula (2019–2025)', count(*)
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND aerolinea_original IS NULL
          AND matricula IS NULL
        UNION ALL
        SELECT 'Origen/destino en lugar apto denunciado (sin coordenadas)', count(*)
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
          AND regexp_matches(origen_destino, '^[0-9]+$')
        UNION ALL
        SELECT 'Pasajeros sin dato', count(*)
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND pasajeros IS NULL""")]

    con.close()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "auditoria.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    return dest
