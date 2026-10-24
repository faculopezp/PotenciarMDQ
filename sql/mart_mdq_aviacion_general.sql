-- Actividad no comercial (privados, escuela, oficiales, trabajo aéreo) por mes.
SELECT
  anio, mes, make_date(anio, mes, 1) AS periodo, clase_vuelo, aeronave_categoria,
  count(*) AS movimientos
FROM fct_movimiento
WHERE aeropuerto = getvariable('foco') AND NOT es_comercial
GROUP BY ALL
ORDER BY anio, mes, movimientos DESC
