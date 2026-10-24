-- MDQ vs aeropuertos pares (config/mdq.yaml).
WITH base AS (
  SELECT * FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') OR list_contains(getvariable('pares'), aeropuerto)
),
a AS (
  SELECT
    aeropuerto, anio,
    count(*) FILTER (es_comercial)                                  AS movimientos_comerciales,
    coalesce(sum(pasajeros) FILTER (es_comercial), 0)               AS pasajeros_comerciales,
    round(count(*) FILTER (NOT es_comercial) / count(*), 4)         AS share_movimientos_no_comerciales,
    round(sum(pasajeros) FILTER (asientos_estimados IS NOT NULL)
          / nullif(sum(asientos_estimados) FILTER (pasajeros IS NOT NULL), 0), 3) AS lf_estimado,
    count(DISTINCT origen_destino) FILTER (es_regular)              AS destinos_regulares,
    count(DISTINCT aerolinea_nombre) FILTER (es_comercial AND aerolinea IS NOT NULL) AS aerolineas_activas,
    round(sum(pasajeros) FILTER (es_comercial AND es_temporada_verano)
          / nullif(sum(pasajeros) FILTER (es_comercial), 0), 4)     AS share_pax_temporada_verano,
    count(DISTINCT mes)                                             AS meses_con_datos
  FROM base GROUP BY aeropuerto, anio
),
mensual AS (
  SELECT aeropuerto, anio, mes, sum(pasajeros) AS pax FROM base WHERE es_comercial GROUP BY ALL
),
est AS (
  SELECT aeropuerto, anio, round(max(pax) / nullif(min(pax), 0), 2) AS ratio_pico_valle
  FROM mensual GROUP BY ALL
),
rot AS (
  SELECT aeropuerto, anio, median(tiempo_en_tierra_min) AS turnaround_mediano_min
  FROM fct_rotacion WHERE tipo_rotacion = 'rotacion' GROUP BY ALL
)
SELECT
  a.*,
  a.aeropuerto = getvariable('foco') AS es_foco,
  ap.ciudad,
  e.ratio_pico_valle,
  r.turnaround_mediano_min
FROM a
LEFT JOIN est e USING (aeropuerto, anio)
LEFT JOIN rot r USING (aeropuerto, anio)
LEFT JOIN dim_aeropuerto ap ON ap.codigo = a.aeropuerto
ORDER BY anio, pasajeros_comerciales DESC
