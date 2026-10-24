-- Flota por año: familia, modelo estandarizado (config/aeronaves.yaml → modelos) y designador ICAO.
-- aeronave_familia_inferida completa 2019–2020 con las reglas de inferencia (aeronave_inferida).
SELECT
  anio, segmento, es_linea, aeronave_categoria, aeronave_familia, aeronave_familia_inferida,
  aeronave_inferida, coalesce(aeronave_modelo, aeronave_familia) AS aeronave_modelo,
  aeronave_modelo_inferido, aeronave_icao,
  count(*)                    AS movimientos,
  coalesce(sum(pasajeros), 0) AS pasajeros
FROM fct_movimiento
WHERE aeropuerto = getvariable('foco')
GROUP BY ALL
ORDER BY anio, movimientos DESC
