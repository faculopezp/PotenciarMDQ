-- Todos los orígenes/destinos de MDQ por año, segmento y ámbito (cabotaje / internacional),
-- incluida la aviación general. Los códigos sin coordenadas quedan con lat/lon NULL.
SELECT
  m.anio, m.origen_destino AS codigo, m.clasificacion_vuelo, m.segmento, m.es_linea,
  count(*)                     AS movimientos,
  coalesce(sum(m.pasajeros), 0) AS pasajeros,
  ap.nombre, ap.ciudad, ap.pais, ap.lat, ap.lon, ap.fuente_coord, ap.distancia_mdq_km
FROM fct_movimiento m
LEFT JOIN dim_aeropuerto ap ON ap.codigo = m.origen_destino
WHERE m.aeropuerto = getvariable('foco') AND m.origen_destino IS NOT NULL
GROUP BY ALL
ORDER BY anio, movimientos DESC
