-- Hecho principal: 1 fila = 1 aterrizaje o despegue, enriquecido con calendario, aerolínea,
-- aeronave, distancia y métricas estimadas. Ver docs/07_bd_y_metricas.md.
CREATE OR REPLACE TABLE fct_movimiento AS
WITH s AS (
  SELECT
    s.* EXCLUDE (aeropuerto),
    s.aeropuerto                                   AS aeropuerto_original,
    coalesce(c.a, s.aeropuerto)                    AS aeropuerto,
    CAST(s.fecha + s.hora_utc AS TIMESTAMP)        AS ts_utc
  FROM stg_movimiento s
  LEFT JOIN correcciones c
    ON s.aeropuerto = c.de AND list_contains(c.clases, s.clase_vuelo)
),
e AS (
  SELECT
    *,
    ts_utc + to_hours(getvariable('utc_offset'))                       AS ts_local,
    coalesce(CAST(ts_utc + to_hours(getvariable('utc_offset')) AS DATE), fecha) AS fecha_local,
    list_contains(getvariable('comerciales'), clase_vuelo)             AS es_comercial
  FROM s
),
j AS (
  SELECT
    e.*,
    al.aerolinea_nombre, al.aerolinea_tipo,
    an.fabricante, an.familia, an.categoria,
    round(haversine_km(a1.lat, a1.lon, a2.lat, a2.lon))                AS distancia_km,
    coalesce(ca.capacidad, cn.capacidad)                               AS capacidad,
    CASE WHEN ca.capacidad IS NOT NULL THEN 'p95_aerolinea_aeronave'
         WHEN cn.capacidad IS NOT NULL THEN 'p95_aeronave' END         AS fuente_capacidad
  FROM e
  LEFT JOIN dim_aerolinea al ON al.aerolinea = e.aerolinea
  LEFT JOIN dim_aeronave an  ON an.aeronave = e.aeronave
  LEFT JOIN dim_aeropuerto a1 ON a1.codigo = e.aeropuerto
  LEFT JOIN dim_aeropuerto a2 ON a2.codigo = e.origen_destino
  LEFT JOIN dim_capacidad ca ON ca.metodo = 'aerolinea_aeronave'
                            AND ca.aerolinea = e.aerolinea AND ca.aeronave = e.aeronave
  LEFT JOIN dim_capacidad cn ON cn.metodo = 'aeronave' AND cn.aeronave = e.aeronave
)
SELECT
  row_number() OVER (ORDER BY j.ts_utc, j.aeropuerto, j.tipo_movimiento, j.origen_destino)
                                                   AS movimiento_id,
  -- tiempo
  j.fecha                                          AS fecha_utc,
  j.hora_utc,
  j.ts_utc,
  j.ts_local,
  j.fecha_local                                    AS fecha,
  year(j.fecha_local)                              AS anio,
  month(j.fecha_local)                             AS mes,
  hour(j.ts_local)                                 AS hora_local,
  CASE WHEN j.ts_local IS NULL THEN NULL
       WHEN hour(j.ts_local) < 6  THEN 'madrugada'
       WHEN hour(j.ts_local) < 12 THEN 'mañana'
       WHEN hour(j.ts_local) < 19 THEN 'tarde'
       ELSE 'noche' END                            AS franja_horaria,
  f.dia_semana, f.dia_semana_nombre, f.es_fin_de_semana, f.es_feriado, f.es_finde_largo,
  f.es_temporada_verano, f.verano_anio,
  -- tipo de vuelo
  j.clase_vuelo,
  j.es_comercial,
  j.clase_vuelo = 'regular'                        AS es_regular,
  j.clasificacion_vuelo,
  j.tipo_movimiento,
  -- lugar
  j.aeropuerto,
  j.aeropuerto_original,
  j.aeropuerto IS DISTINCT FROM j.aeropuerto_original AS aeropuerto_corregido,
  j.origen_destino,
  j.distancia_km,
  -- operador y aeronave
  j.aerolinea,
  coalesce(j.aerolinea_nombre, 'Sin dato')         AS aerolinea_nombre,
  coalesce(j.aerolinea_tipo, 'sin_dato')           AS aerolinea_tipo,
  j.aeronave,
  j.fabricante                                     AS aeronave_fabricante,
  coalesce(j.familia, 'Sin dato')                  AS aeronave_familia,
  coalesce(j.categoria, 'sin_dato')                AS aeronave_categoria,
  j.matricula,
  CASE WHEN j.matricula IS NULL THEN NULL
       WHEN regexp_matches(j.matricula, '^L[VQ]-') THEN 'argentina'
       ELSE 'extranjera' END                       AS matricula_origen,
  -- demanda y oferta
  j.pasajeros,
  j.pax_nacional,
  CASE WHEN j.es_comercial THEN j.capacidad END    AS asientos_estimados,
  CASE WHEN j.es_comercial THEN j.fuente_capacidad END AS fuente_asientos,
  CASE WHEN j.es_comercial
       THEN round(j.pasajeros / nullif(j.capacidad, 0), 3) END AS lf_estimado,
  j.pasajeros * j.distancia_km                     AS rpk_est,
  CASE WHEN j.es_comercial THEN j.capacidad * j.distancia_km END AS ask_est,
  -- calidad
  j.calidad_dato,
  j.calidad_dato = 'provisorio'                    AS es_provisorio,
  j.source_file
FROM j
LEFT JOIN dim_fecha f ON f.fecha = j.fecha_local
-- Los vuelos de las primeras horas UTC del primer día caen el día anterior en hora local: se
-- descartan para no crear un año con un par de filas (ej. 31/12/2018).
WHERE j.fecha_local >= (SELECT min(fecha) FROM stg_movimiento);
