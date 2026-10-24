-- Perfil anual de cada segmento: volumen, a quién sirve, cuándo y cómo opera.
WITH b AS (SELECT * FROM fct_movimiento WHERE aeropuerto = getvariable('foco')),
mensual AS (SELECT anio, segmento, mes, count(*) AS n FROM b GROUP BY ALL),
est AS (
  SELECT anio, segmento, round(max(n) / nullif(min(n), 0), 2) AS ratio_pico_valle, count(*) AS meses_activos
  FROM mensual GROUP BY ALL
),
rot AS (
  SELECT anio, segmento, median(tiempo_en_tierra_min) AS tiempo_en_tierra_mediano_min
  FROM fct_rotacion WHERE aeropuerto = getvariable('foco') AND tipo_rotacion <> 'pernocte'
  GROUP BY ALL
),
a AS (
  SELECT
    anio, segmento,
    count(*)                                                        AS movimientos,
    coalesce(sum(pasajeros), 0)                                     AS pasajeros,
    round(avg(pasajeros), 2)                                        AS pax_por_movimiento,
    count(DISTINCT aerolinea) FILTER (aerolinea IS NOT NULL)        AS operadores,
    count(DISTINCT matricula)                                       AS matriculas,
    count(DISTINCT origen_destino) FILTER (NOT es_vuelo_local)      AS origenes_destinos,
    round(count(*) FILTER (es_vuelo_local) / count(*), 4)           AS share_vuelos_locales,
    round(count(*) FILTER (es_fin_de_semana OR es_feriado) / count(*), 4) AS share_finde_feriado,
    round(count(*) FILTER (es_temporada_verano) / count(*), 4)      AS share_temporada_verano,
    round(count(*) FILTER (matricula_origen = 'extranjera') / nullif(count(matricula), 0), 4)
                                                                    AS share_matricula_extranjera,
    mode(hora_local)                                                AS hora_mas_frecuente,
    count(*) FILTER (aeronave IS NULL)                              AS movimientos_sin_aeronave
  FROM b GROUP BY anio, segmento
)
SELECT
  a.*,
  round(a.movimientos / sum(a.movimientos) OVER (PARTITION BY a.anio), 4) AS share_movimientos,
  e.ratio_pico_valle, e.meses_activos,
  r.tiempo_en_tierra_mediano_min
FROM a
LEFT JOIN est e USING (anio, segmento)
LEFT JOIN rot r USING (anio, segmento)
ORDER BY anio, movimientos DESC
