-- KPIs anuales MDQ (ver docs/07_bd_y_metricas.md para definiciones).
WITH base AS (
  SELECT * FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
),
a AS (
  SELECT
    anio,
    count(*)                                                       AS movimientos,
    count(*) FILTER (es_comercial)                                 AS movimientos_comerciales,
    round(count(*) FILTER (NOT es_comercial) / count(*), 4)        AS share_movimientos_no_comerciales,
    round(count(*) FILTER (NOT es_linea) / count(*), 4)            AS share_movimientos_no_linea,
    count(*) FILTER (es_linea)                                     AS movimientos_linea,
    coalesce(sum(pasajeros), 0)                                    AS pasajeros,
    coalesce(sum(pasajeros) FILTER (es_comercial), 0)              AS pasajeros_comerciales,
    coalesce(sum(pasajeros) FILTER (clasificacion_vuelo = 'internacional'), 0) AS pasajeros_internacional,
    sum(asientos_estimados)                                        AS asientos_estimados,
    round(sum(pasajeros) FILTER (asientos_estimados IS NOT NULL)
          / nullif(sum(asientos_estimados) FILTER (pasajeros IS NOT NULL), 0), 3) AS lf_estimado,
    round(sum(rpk_est) FILTER (es_comercial))                      AS rpk_est,
    round(sum(ask_est))                                            AS ask_est,
    round(sum(rpk_est) FILTER (es_comercial)
          / nullif(sum(pasajeros) FILTER (es_comercial AND distancia_km IS NOT NULL), 0)) AS distancia_media_pax_km,
    count(DISTINCT aerolinea_nombre) FILTER (es_comercial AND aerolinea IS NOT NULL) AS aerolineas_activas,
    count(DISTINCT origen_destino) FILTER (es_regular)             AS destinos_regulares,
    count(DISTINCT matricula) FILTER (es_comercial)                AS matriculas_comerciales,
    count(DISTINCT mes)                                            AS meses_con_datos,
    bool_or(es_provisorio)                                         AS tiene_provisorio
  FROM base GROUP BY anio
),
mensual AS (
  SELECT anio, mes, sum(pasajeros) AS pax FROM base WHERE es_comercial GROUP BY anio, mes
),
estacional AS (
  SELECT anio,
         round(max(pax) / nullif(min(pax), 0), 2)                         AS ratio_pico_valle,
         round(stddev_pop(pax) / nullif(avg(pax), 0), 3)                  AS cv_mensual,
         arg_max(mes, pax)                                                AS mes_pico
  FROM mensual GROUP BY anio
),
verano AS (
  SELECT anio, round(sum(pasajeros) FILTER (es_temporada_verano) / nullif(sum(pasajeros), 0), 4)
           AS share_pax_temporada_verano
  FROM base WHERE es_comercial GROUP BY anio
),
pax_aer AS (
  SELECT anio, aerolinea_nombre, sum(pasajeros) AS pax FROM base
  WHERE es_linea AND aerolinea IS NOT NULL GROUP BY anio, aerolinea_nombre
),
hhi AS (
  SELECT anio, round(sum(pow(pax / tot, 2)) * 10000) AS hhi_aerolineas
  FROM (SELECT *, sum(pax) OVER (PARTITION BY anio) AS tot FROM pax_aer) GROUP BY anio
),
horas AS (
  SELECT anio, mes, fecha, hora_local, sum(pasajeros) AS pax
  FROM base WHERE es_comercial AND hora_local IS NOT NULL GROUP BY ALL
),
sbr AS (   -- Standard Busy Rate: 30.ª hora más cargada del año
  SELECT anio, max(pax) AS pax_hora_record, list_sort(list(pax), 'DESC')[30] AS pax_hora_sbr30
  FROM horas GROUP BY anio
),
tphp AS (  -- Typical Peak Hour Passengers (FAA): hora pico del día promedio del mes pico
  SELECT e.anio,
         round(max(h.pax_hora / day(last_day(make_date(e.anio, e.mes_pico, 1))))) AS pax_hora_tphp
  FROM estacional e
  JOIN (SELECT anio, mes, hora_local, sum(pax) AS pax_hora FROM horas GROUP BY ALL) h
    ON h.anio = e.anio AND h.mes = e.mes_pico
  GROUP BY e.anio
),
rot AS (
  SELECT anio,
         median(tiempo_en_tierra_min) FILTER (tipo_rotacion = 'rotacion') AS turnaround_mediano_min,
         count(*) FILTER (tipo_rotacion = 'pernocte')                     AS pernoctes
  FROM fct_rotacion WHERE aeropuerto = getvariable('foco') GROUP BY anio
)
SELECT
  a.*,
  round(a.pasajeros_comerciales / nullif(a.movimientos_comerciales, 0), 1) AS pax_por_mov_comercial,
  round(a.pasajeros_internacional / nullif(a.pasajeros, 0), 4)              AS share_internacional,
  round(a.pasajeros / nullif(lag(a.pasajeros) OVER (ORDER BY a.anio), 0) - 1, 4) AS var_interanual,
  h.hhi_aerolineas,
  e.ratio_pico_valle, e.cv_mensual, e.mes_pico,
  v.share_pax_temporada_verano,
  s.pax_hora_record, s.pax_hora_sbr30, t.pax_hora_tphp,
  r.turnaround_mediano_min, r.pernoctes
FROM a
LEFT JOIN hhi h USING (anio)
LEFT JOIN estacional e USING (anio)
LEFT JOIN verano v USING (anio)
LEFT JOIN sbr s USING (anio)
LEFT JOIN tphp t USING (anio)
LEFT JOIN rot r USING (anio)
ORDER BY anio
