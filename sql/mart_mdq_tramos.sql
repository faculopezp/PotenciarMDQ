-- Duración de vuelo (pista a pista) de las rutas de MDQ.
SELECT
  anio, origen, destino, aeronave_familia,
  count(*)                              AS tramos,
  median(duracion_min)                  AS duracion_mediana_min,
  quantile_cont(duracion_min, 0.1)      AS p10_min,
  quantile_cont(duracion_min, 0.9)      AS p90_min,
  median(velocidad_bloque_kmh)          AS velocidad_mediana_kmh,
  any_value(distancia_km)               AS distancia_km
FROM fct_tramo
WHERE origen = getvariable('foco') OR destino = getvariable('foco')
GROUP BY ALL
HAVING count(*) >= 5
ORDER BY anio, tramos DESC
