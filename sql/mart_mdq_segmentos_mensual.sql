-- Actividad por segmento y mes (toda la aviación, no solo la de línea).
SELECT
  anio, mes, make_date(anio, mes, 1) AS periodo, segmento,
  count(*)                                  AS movimientos,
  coalesce(sum(pasajeros), 0)               AS pasajeros,
  count(*) FILTER (es_vuelo_local)          AS movimientos_locales
FROM fct_movimiento
WHERE aeropuerto = getvariable('foco')
GROUP BY anio, mes, segmento
ORDER BY anio, mes, segmento
