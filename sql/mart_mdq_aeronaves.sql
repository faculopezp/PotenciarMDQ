-- Flota y tipo de aviación por año.
SELECT
  anio, es_comercial, clase_vuelo, aeronave_categoria, aeronave_familia,
  count(*)                    AS movimientos,
  coalesce(sum(pasajeros), 0) AS pasajeros
FROM fct_movimiento
WHERE aeropuerto = getvariable('foco')
GROUP BY ALL
ORDER BY anio, movimientos DESC
