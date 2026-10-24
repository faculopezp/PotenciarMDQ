"""Chequeos de calidad sobre la BD -> reports/qa/anac_movimientos.md."""

from __future__ import annotations

from pathlib import Path

import duckdb

from potenciar_mdq import bd
from potenciar_mdq.settings import BD, CONFIG, REPORTS
from potenciar_mdq.standardize.columns import VOCAB


def _table(con: duckdb.DuckDBPyConnection, sql: str) -> str:
    rel = con.sql(sql)
    cols = rel.columns
    rows = rel.fetchall()
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols)
    body = "\n".join("| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in rows)
    return f"{head}\n{body}\n"


def run(db_path: Path = BD, out_dir: Path = REPORTS / "qa") -> Path:
    con = bd.connect(db_path, read_only=True)
    con.execute("CREATE TEMP VIEW f AS SELECT * FROM fct_movimiento")
    out = ["# QA — BD PotenciarMDQ", ""]

    out += ["## Filas y nulos por archivo", "", _table(con, """
        SELECT source_file, count(*) AS filas,
               round(100.0 * count(*) FILTER (fecha IS NULL) / count(*), 2) AS pct_fecha_null,
               round(100.0 * count(*) FILTER (hora_utc IS NULL) / count(*), 2) AS pct_hora_null,
               round(100.0 * count(*) FILTER (pasajeros IS NULL) / count(*), 2) AS pct_pax_null,
               round(100.0 * count(*) FILTER (aeronave IS NULL) / count(*), 2) AS pct_aeronave_null,
               round(100.0 * count(*) FILTER (matricula IS NOT NULL) / count(*), 2) AS pct_con_matricula,
               round(100.0 * count(*) FILTER (es_provisorio) / count(*), 2) AS pct_provisorio,
               min(fecha) AS desde, max(fecha) AS hasta
        FROM f GROUP BY 1 ORDER BY 1""")]

    for col, vocab in VOCAB.items():
        allowed = ", ".join(f"'{v}'" for v in set(vocab.values()))
        out += [f"## Valores fuera de vocabulario: `{col}`", "", _table(con, f"""
            SELECT {col} AS valor, count(*) AS filas FROM f
            WHERE {col} IS NOT NULL AND {col} NOT IN ({allowed})
            GROUP BY 1 ORDER BY 2 DESC LIMIT 20""")]

    out += ["## Clases de vuelo (ajustar `clases_comerciales` en config/mdq.yaml)", "",
            _table(con, "SELECT clase_vuelo, es_comercial, count(*) AS filas FROM f "
                        "GROUP BY ALL ORDER BY 3 DESC")]

    out += ["## Duplicados exactos", "", _table(con, """
        SELECT count(*) - count(DISTINCT (ts_utc, aeropuerto, tipo_movimiento, origen_destino,
               aerolinea, aeronave, matricula, pasajeros)) AS filas_duplicadas FROM f""")]

    out += ["## Correcciones de aeropuerto aplicadas", "", _table(con, """
        SELECT aeropuerto_original, aeropuerto, count(*) AS filas FROM f
        WHERE aeropuerto_corregido GROUP BY ALL""")]

    out += ["## Cobertura de enriquecimiento (vuelos comerciales)", "", _table(con, """
        SELECT
          round(100.0 * count(*) FILTER (aeronave_categoria = 'otro') / count(*), 2) AS pct_aeronave_otro,
          round(100.0 * count(*) FILTER (aerolinea_tipo = 'otra') / count(*), 2) AS pct_aerolinea_sin_regla,
          round(100.0 * count(*) FILTER (distancia_km IS NULL) / count(*), 2) AS pct_sin_distancia,
          round(100.0 * count(*) FILTER (asientos_estimados IS NULL) / count(*), 2) AS pct_sin_asientos
        FROM f WHERE es_comercial""")]

    out += ["## Aeronaves sin clasificar (top 25 → ampliar config/aeronaves.yaml)", "", _table(con, """
        SELECT aeronave, count(*) AS movimientos FROM f WHERE aeronave_categoria = 'otro'
        GROUP BY 1 ORDER BY 2 DESC LIMIT 25""")]

    out += ["## Códigos sin coordenadas (top 20 → revisar dim_aeropuerto)", "", _table(con, """
        SELECT origen_destino, count(*) AS movimientos FROM f
        WHERE distancia_km IS NULL AND origen_destino IS NOT NULL
        GROUP BY 1 ORDER BY 2 DESC LIMIT 20""")]

    out += ["## Tramos reconstruidos (cabotaje comercial)", "", _table(con, """
        SELECT
          (SELECT count(*) FROM fct_tramo) AS tramos,
          (SELECT count(*) FROM f WHERE es_comercial AND clasificacion_vuelo = 'cabotaje'
             AND tipo_movimiento = 'despegue') AS despegues_cabotaje,
          round(100.0 * (SELECT count(*) FROM fct_tramo) / nullif((SELECT count(*) FROM f
             WHERE es_comercial AND clasificacion_vuelo = 'cabotaje'
             AND tipo_movimiento = 'despegue'), 0), 1) AS pct_emparejado""")]

    out += ["## Rotaciones: método por matrícula vs por modelo", "", _table(con, """
        SELECT aeropuerto, metodo_emparejamiento, tipo_rotacion, count(*) AS n,
               median(tiempo_en_tierra_min) AS mediana_min
        FROM fct_rotacion GROUP BY ALL ORDER BY 1, 2, 3""")]

    out += ["## Meses sin movimientos en el foco", "", _table(con, """
        WITH rango AS (
          SELECT range AS m FROM range(
            (SELECT date_trunc('month', min(fecha)) FROM f),
            (SELECT date_trunc('month', max(fecha)) FROM f) + INTERVAL 1 MONTH,
            INTERVAL 1 MONTH)
        )
        SELECT strftime(m, '%Y-%m') AS mes_faltante FROM rango
        WHERE m NOT IN (SELECT DISTINCT date_trunc('month', fecha) FROM f
                        WHERE aeropuerto = getvariable('foco'))
        ORDER BY 1""")]

    out += ["## Outliers: load factor estimado > 1,1 en el foco", "", _table(con, """
        SELECT fecha, aeronave, aerolinea_nombre, pasajeros, asientos_estimados, lf_estimado
        FROM f WHERE aeropuerto = getvariable('foco') AND lf_estimado > 1.1
        ORDER BY lf_estimado DESC LIMIT 20""")]

    out += ["## Reconciliación vs fuente oficial (config/reconciliacion.csv)", "", _table(con, f"""
        WITH r AS (SELECT * FROM read_csv('{CONFIG / "reconciliacion.csv"}', header=true,
                   columns={{'anio':'INT','mes':'INT','aeropuerto_anac':'VARCHAR',
                   'pasajeros_oficial':'BIGINT','movimientos_oficial':'BIGINT',
                   'fuente_url':'VARCHAR','nota':'VARCHAR'}})),
             d AS (SELECT year(fecha_utc) AS anio, month(fecha_utc) AS mes, aeropuerto,
                          sum(pasajeros) AS pax, count(*) AS movs
                   FROM f GROUP BY ALL)
        SELECT r.anio, r.mes, r.aeropuerto_anac, r.pasajeros_oficial, d.pax AS pasajeros_datos,
               round(100.0 * (d.pax - r.pasajeros_oficial) / nullif(r.pasajeros_oficial, 0), 2)
                 AS dif_pax_pct,
               r.movimientos_oficial, d.movs AS movimientos_datos,
               round(100.0 * (d.movs - r.movimientos_oficial) / nullif(r.movimientos_oficial, 0), 2)
                 AS dif_movs_pct
        FROM r LEFT JOIN d ON d.anio = r.anio AND d.mes = r.mes AND d.aeropuerto = r.aeropuerto_anac
        ORDER BY 1, 2""")]

    con.close()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "anac_movimientos.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    return dest
