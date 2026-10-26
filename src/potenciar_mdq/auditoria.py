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
                     aerolinea_nombre AS nombre, segmento,
                     CASE WHEN aeronave_fuente = 'anac' THEN aeronave END AS aeronave,
                     CASE WHEN aeronave_fuente = 'anac_version_anterior' THEN aeronave_familia
                     END AS familia_previa
              FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND anio = 2019
            ),
            k AS (
              SELECT a.movimiento_id, a.aeronave, a.familia_previa, a.segmento, m.aeronave AS av_mun,
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
                      AND anio = 2019 AND aeronave_fuente IS DISTINCT FROM 'anac') AS anac_sin_aeronave,
                   count(DISTINCT movimiento_id) FILTER (c_anac = 1 AND c_mun = 1) AS cruces_1_a_1,
                   count(DISTINCT movimiento_id) FILTER (c_anac = 1 AND c_mun = 1 AND aeronave IS NULL
                     AND av_mun IS NOT NULL) AS aeronave_recuperable
            FROM cruce"""),
                "Aeronaves recuperables, por segmento y modelo municipal:", "", _table(con, """
            SELECT segmento, av_mun AS aeronave_municipal, count(*) AS movimientos
            FROM cruce WHERE c_anac = 1 AND c_mun = 1 AND aeronave IS NULL AND av_mun IS NOT NULL
            GROUP BY ALL ORDER BY 3 DESC LIMIT 15"""),
                "Validación cruzada: familia de la ANAC 2019 versión anterior contra el portal "
                "municipal en los mismos vuelos (1 a 1):", "", _table(con, """
            SELECT c.familia_previa, d.familia AS familia_municipal, count(*) AS vuelos
            FROM cruce c JOIN dim_aeronave d ON d.aeronave = c.av_mun
            WHERE c.c_anac = 1 AND c.c_mun = 1 AND c.familia_previa IS NOT NULL
            GROUP BY ALL ORDER BY 3 DESC LIMIT 12""")]

    # ── D bis: diagnóstico del cruce ANAC 2019 versión anterior ↔ vigente ──────────────────
    if _existe(con, "ref_anac_previa"):
        out += ["### ANAC 2019 versión anterior ↔ vigente: diagnóstico de claves", "",
                "Para cada registro de la versión anterior, el de la vigente más cercano en hora "
                "(mismo día, aeropuerto, movimiento y origen/destino): diferencia en minutos y si "
                "coinciden los pasajeros.", "", _table(con, """
            WITH v AS (
              SELECT movimiento_id, fecha, hora_utc, aeropuerto_original AS aeropuerto,
                     tipo_movimiento, origen_destino, pasajeros
              FROM fct_movimiento WHERE anio = 2019
                AND aeropuerto_original IN (SELECT DISTINCT aeropuerto FROM ref_anac_previa)
            ),
            k AS (
              SELECT p.*, round(date_diff('minute', p.fecha + p.hora_utc, v.fecha + v.hora_utc))
                       AS dif_min, v.pasajeros AS pax_vigente
              FROM ref_anac_previa p JOIN v
                ON v.fecha BETWEEN p.fecha - 1 AND p.fecha + 1 AND v.aeropuerto = p.aeropuerto
               AND v.tipo_movimiento = p.tipo_movimiento AND v.origen_destino = p.origen_destino
              QUALIFY row_number() OVER (PARTITION BY p.fecha, p.hora_utc, p.tipo_movimiento,
                                         p.origen_destino, p.aeronave, p.pasajeros
                                         ORDER BY abs(dif_min)) = 1
            )
            SELECT CASE WHEN dif_min = 0 THEN '0' WHEN abs(dif_min) <= 5 THEN '±5'
                        WHEN dif_min BETWEEN 175 AND 185 THEN '+180'
                        WHEN dif_min BETWEEN -185 AND -175 THEN '-180' ELSE 'otro' END AS dif_min,
                   count(*) AS registros, count(*) FILTER (pasajeros = pax_vigente) AS pax_iguales,
                   count(aeronave) AS con_aeronave
            FROM k GROUP BY 1 ORDER BY 2 DESC"""),
                "Registros de la versión anterior sin ningún candidato el mismo día: ", "",
                _table(con, """
            SELECT count(*) AS registros_version_anterior,
                   (SELECT count(*) FROM fct_movimiento WHERE anio = 2019
                      AND aeropuerto_original IN (SELECT DISTINCT aeropuerto FROM ref_anac_previa))
                     AS registros_vigente
            FROM ref_anac_previa""")]

    # ── E: el otro extremo sin matrícula, validado contra vuelos que traen el dato ──────────
    # Se toman vuelos del foco con operador y avión informados, se "esconde" uno de los dos y se
    # busca el otro extremo con las mismas reglas (sql/bd/25, punto 5; acá solo se exige candidato
    # único del lado del foco, más laxo que en la base).
    con.execute("""
        CREATE TEMP TABLE val_par AS
        WITH m AS (
          SELECT f.movimiento_id, f.aeropuerto, f.origen_destino, f.tipo_movimiento, f.ts_utc,
                 f.fecha, f.aerolinea_original AS op, f.matricula, f.segmento,
                 CASE WHEN f.aeronave_fuente = 'anac' THEN f.aeronave END AS av,
                 coalesce(al.aerolinea_clave, f.aerolinea_original) AS clave
          FROM fct_movimiento f LEFT JOIN dim_aerolinea al ON al.aerolinea = f.aerolinea_original
          WHERE f.ts_utc IS NOT NULL AND f.origen_destino IS NOT NULL
            AND f.aeropuerto <> f.origen_destino
        ),
        x AS (SELECT * FROM m WHERE aeropuerto = getvariable('foco') AND op IS NOT NULL
                AND av IS NOT NULL AND segmento <> 'linea_regular'),
        d AS (SELECT unnest([-1, 0, 1]) AS o),
        base AS (
          SELECT x.movimiento_id, x.op, x.av, x.clave, x.matricula, y.op AS op_y, y.av AS av_y,
                 y.clave AS clave_y, y.matricula AS mat_y, x.tipo_movimiento, x.ts_utc, y.ts_utc AS ts_y
          FROM x CROSS JOIN d
          JOIN m y ON y.fecha = x.fecha + d.o AND y.aeropuerto = x.origen_destino
                  AND y.origen_destino = x.aeropuerto AND y.tipo_movimiento <> x.tipo_movimiento
          WHERE (x.tipo_movimiento = 'aterrizaje' AND y.ts_utc BETWEEN x.ts_utc - INTERVAL 10 HOUR AND x.ts_utc - INTERVAL 10 MINUTE)
             OR (x.tipo_movimiento = 'despegue' AND y.ts_utc BETWEEN x.ts_utc + INTERVAL 10 MINUTE AND x.ts_utc + INTERVAL 10 HOUR)
        ),
        -- sin operador: se compara solo el avión; sin avión: solo el operador
        sin_op AS (
          SELECT 'operador' AS dato, movimiento_id, clave AS real, clave_y AS recuperado
          FROM base WHERE (av_y IS NULL OR av_y = av)
            AND (matricula IS NULL OR mat_y IS NULL OR matricula = mat_y)
          QUALIFY count(*) OVER (PARTITION BY movimiento_id) = 1
        ),
        sin_av AS (
          SELECT 'aeronave' AS dato, movimiento_id, av AS real, av_y AS recuperado
          FROM base WHERE (op_y IS NULL OR clave_y = clave)
            AND (matricula IS NULL OR mat_y IS NULL OR matricula = mat_y)
          QUALIFY count(*) OVER (PARTITION BY movimiento_id) = 1
        )
        SELECT * FROM sin_op UNION ALL SELECT * FROM sin_av""")
    out += ["## 2E. El otro extremo del mismo vuelo sin matrícula (2019–2025)", "",
            "Validación en el foco (vuelos no regulares con operador y avión informados; se esconde "
            "uno y se recupera del otro extremo):", "", _table(con, """
        SELECT dato, count(*) FILTER (recuperado IS NOT NULL) AS recuperados,
               count(*) FILTER (recuperado = real) AS coinciden,
               round(100.0 * count(*) FILTER (recuperado = real)
                     / nullif(count(*) FILTER (recuperado IS NOT NULL), 0), 1) AS pct_coinciden
        FROM val_par GROUP BY 1 ORDER BY 1""")]

    # ── F: aeronaves del Estado (config/estatales.yaml) ────────────────────────────────────
    out += ["## 2F. Aeronaves del Estado: operador por prefijo de la identificación (2026)", "",
            "Contrastación con los vuelos que traen operador en ANAC. Los desacuerdos son casi todos "
            "ANAC cargando \"Fuerza Aérea\" en aeronaves de otra fuerza (ej. 1-G-49 Huron de la "
            "Armada, PA-40 Dauphin de Prefectura, identificados en fuentes públicas).", "",
            _table(con, """
        WITH m AS (
          SELECT f.*, upper(regexp_replace(matricula, '[- ]', '', 'g')) AS ident
          FROM fct_movimiento f
          WHERE matricula IS NOT NULL AND clase_vuelo <> 'vuelo_oficial_extranjero'
        ),
        r AS (
          SELECT m.*, p.operador AS regla, p.valida, p.patron
          FROM m JOIN ref_prefijo_estatal p ON regexp_matches(m.ident, p.patron)
          QUALIFY row_number() OVER (PARTITION BY m.movimiento_id ORDER BY p.orden) = 1
        )
        SELECT patron, regla, count(*) AS movimientos,
          count(aerolinea_original) AS con_operador_anac,
          count(*) FILTER (regexp_matches(upper(strip_accents(aerolinea_original)), valida))
            AS coinciden,
          count(*) FILTER (aerolinea_original IS NULL) AS completados,
          count(*) FILTER (aerolinea_original IS NULL AND aeropuerto = getvariable('foco'))
            AS completados_foco
        FROM r GROUP BY ALL ORDER BY 3 DESC"""),
            "Modelo por serie con identificación pública (config/estatales.yaml → series):", "",
            _table(con, """
        SELECT upper(regexp_replace(matricula, '[- ]', '', 'g')) AS serie, aeronave_modelo,
               count(*) AS movimientos,
               count(*) FILTER (aeropuerto = getvariable('foco')) AS en_foco
        FROM fct_movimiento WHERE aeronave_fuente = 'serie_estatal'
        GROUP BY ALL ORDER BY 3 DESC""")]

    # ── Lo aplicado en la base y validación de la inferencia ───────────────────────────────
    out += ["## 4. Aplicado en la base (fct_movimiento)", "", _table(con, """
        SELECT CASE WHEN aeropuerto = getvariable('foco') THEN 'MDQ' ELSE 'resto del país' END AS ambito,
          count(*) FILTER (operador_fuente = 'matricula') AS operador_por_matricula,
          count(*) FILTER (operador_fuente = 'otro_extremo') AS operador_por_otro_extremo,
          count(*) FILTER (operador_fuente = 'prefijo_estatal') AS operador_por_prefijo_estatal,
          count(*) FILTER (operador_fuente = 'otro_extremo_sin_matricula')
            AS operador_otro_extremo_sin_matricula,
          count(*) FILTER (operador_fuente = 'anac_version_anterior') AS operador_anac_version_anterior,
          count(*) FILTER (aeronave_fuente = 'anac_version_anterior') AS aeronave_anac_version_anterior,
          count(*) FILTER (aeronave_fuente = 'municipal') AS aeronave_del_municipio,
          count(*) FILTER (aeronave_fuente = 'serie_estatal') AS aeronave_por_serie_estatal,
          count(*) FILTER (aeronave_fuente = 'otro_extremo_sin_matricula')
            AS aeronave_otro_extremo_sin_matricula
        FROM fct_movimiento GROUP BY 1 ORDER BY 1"""),
            "Privado en jet o turbohélice ejecutivo analizado como taxi aéreo. Evidencia en el foco: "
            "cuántos tienen operador o matrícula que también vuela como no regular.", "",
            _table(con, """
        SELECT anio, count(*) AS pasan_a_taxi,
          count(*) FILTER (aerolinea IS NOT NULL OR matricula IS NOT NULL) AS con_operador_o_matricula,
          count(*) FILTER (aerolinea IN (SELECT aerolinea FROM ref_taxi_operador)
                           OR matricula IN (SELECT matricula FROM ref_taxi_matricula))
            AS que_tambien_hacen_taxi
        FROM fct_movimiento
        WHERE aeropuerto = getvariable('foco') AND clase_vuelo LIKE 'vuelo_privado%'
          AND aeronave_categoria IN ('jet_ejecutivo', 'turbohelice_ejecutivo')
        GROUP BY 1 ORDER BY 1"""),
            "Asientos: cabina publicada (config/cabinas.yaml) contra el p95 de pasajeros observados:",
            "", _table(con, """
        SELECT f.aerolinea_nombre, f.aeronave_modelo, any_value(f.asientos_estimados) AS publicados,
               any_value(d.capacidad) AS p95_observado, count(*) AS movimientos_pais,
               count(*) FILTER (f.pasajeros > f.asientos_estimados) AS con_mas_pax_que_asientos
        FROM fct_movimiento f
        LEFT JOIN dim_capacidad d ON d.metodo = 'aerolinea_aeronave' AND d.aerolinea = f.aerolinea
                                 AND d.aeronave = f.aeronave
        WHERE f.fuente_asientos IN ('cabina_publicada', 'cabina_estandar')
        GROUP BY ALL ORDER BY 5 DESC"""),
            "Validación: qué habría dicho la inferencia por pasajeros en los vuelos 2019 del foco "
            "cuyo avión se recuperó (ANAC versión anterior o portal municipal):", "", _table(con, """
        WITH v AS (
          SELECT f.aeronave_familia AS real, r.familia AS inferida
          FROM fct_movimiento f JOIN ref_inferencia_aeronave r
            ON regexp_matches(upper(strip_accents(coalesce(f.aerolinea, ''))), r.operador)
           AND f.pasajeros BETWEEN r.pax_min AND r.pax_max AND f.anio <= r.anio_hasta
          WHERE f.aeronave_fuente IN ('municipal', 'anac_version_anterior')
            AND f.aeropuerto = getvariable('foco') AND f.anio = 2019
        )
        , c AS (SELECT inferida, real, count(*) AS vuelos FROM v GROUP BY inferida, real)
        SELECT *, round(100.0 * vuelos / sum(vuelos) OVER (PARTITION BY inferida), 1) AS pct
        FROM c ORDER BY inferida, vuelos DESC""")]

    # ── 5. Yvera (base agregada de frecuencias): validación y asientos por vuelo ──────────
    if _existe(con, "ref_yvera_frecuencias"):
        out += ["## 5. Yvera, base agregada de frecuencias (validación y asientos)", "",
                "Mismo origen (SIAC/ANAC): coincidir prueba consistencia de procesamiento, no "
                "exactitud de la carga. Vuelos y pasajeros por año contra los movimientos "
                "regulares y no regulares del foco:", "", _table(con, """
            WITH y AS (
              SELECT year(fecha) AS anio, sum(vuelos) AS vuelos_yvera,
                     sum(pasajeros) AS pasajeros_yvera, sum(asientos) AS asientos_yvera
              FROM ref_yvera_frecuencias GROUP BY 1
            ),
            f AS (
              SELECT anio, count(*) AS movimientos_anac, sum(pasajeros) AS pasajeros_anac,
                     sum(asientos_estimados) AS asientos_estimados
              FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
                AND clase_vuelo IN ('regular', 'no_regular') GROUP BY 1
            )
            SELECT anio, vuelos_yvera, movimientos_anac, pasajeros_yvera, pasajeros_anac,
                   asientos_yvera, asientos_estimados
            FROM y FULL JOIN f USING (anio) ORDER BY anio"""),
                "Asientos del vuelo exacto (Yvera, 1 a 1) contra la cabina publicada / p95 que "
                "se usaría sin Yvera:", "", _table(con, """
            SELECT f.aerolinea_nombre, f.aeronave_modelo, count(*) AS vuelos,
                   round(avg(r.asientos), 1) AS asientos_yvera,
                   round(avg(coalesce(cb.asientos, cg.asientos)), 1) AS cabina_config,
                   count(*) FILTER (r.asientos = coalesce(cb.asientos, cg.asientos))
                     AS coinciden_con_cabina
            FROM fct_movimiento f
            JOIN ref_asientos_vuelo r
              ON r.fecha = f.fecha AND r.hora_utc = f.hora_utc
             AND r.aeropuerto = f.aeropuerto_original AND r.tipo_movimiento = f.tipo_movimiento
             AND r.origen_destino = f.origen_destino AND r.pasajeros = f.pasajeros
            LEFT JOIN ref_cabina cb ON cb.operador IS NOT NULL AND cb.modelo = f.aeronave_modelo
             AND regexp_matches(upper(strip_accents(f.aerolinea_nombre)), cb.operador)
            LEFT JOIN ref_cabina cg ON cg.operador IS NULL AND cg.modelo = f.aeronave_modelo
            GROUP BY ALL ORDER BY 3 DESC LIMIT 20""")]

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
        FROM fct_movimiento WHERE aeropuerto = getvariable('foco') AND pasajeros IS NULL"""),
            "Muestra (foco, 2 por segmento): operador sin dato y sin matrícula:", "", _table(con, """
        SELECT segmento, fecha, hora_utc, tipo_movimiento, origen_destino, clase_vuelo,
               aeronave_modelo, pasajeros
        FROM fct_movimiento
        WHERE aeropuerto = getvariable('foco') AND aerolinea IS NULL AND matricula IS NULL
        QUALIFY row_number() OVER (PARTITION BY segmento ORDER BY hash(movimiento_id)) <= 2
        ORDER BY segmento, fecha"""),
            "Muestra (foco, 2 por segmento): aeronave sin dato y sin matrícula:", "", _table(con, """
        SELECT segmento, fecha, hora_utc, tipo_movimiento, origen_destino, clase_vuelo,
               aerolinea_nombre, pasajeros
        FROM fct_movimiento
        WHERE aeropuerto = getvariable('foco') AND aeronave IS NULL AND matricula IS NULL
        QUALIFY row_number() OVER (PARTITION BY segmento ORDER BY hash(movimiento_id)) <= 2
        ORDER BY segmento, fecha""")]

    con.close()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "auditoria.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    return dest
