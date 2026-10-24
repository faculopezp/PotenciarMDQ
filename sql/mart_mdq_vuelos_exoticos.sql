-- Vuelos a/desde destinos "exóticos": fuera del cono sur (el recorte del mapa) o al exterior.
-- Detalle vuelo por vuelo para la sección de destinos lejanos de la web.
SELECT
  m.fecha, m.hora_local, m.anio, m.tipo_movimiento, m.origen_destino AS codigo,
  ap.ciudad, ap.nombre, ap.pais, ap.lat, ap.lon, ap.distancia_mdq_km,
  m.segmento, m.aerolinea_nombre, coalesce(m.aeronave_modelo, m.aeronave_familia) AS aeronave,
  m.matricula, m.pasajeros
FROM fct_movimiento m
JOIN dim_aeropuerto ap ON ap.codigo = m.origen_destino
WHERE m.aeropuerto = getvariable('foco')
  AND ap.lat IS NOT NULL
  AND (ap.lat > -14 OR ap.lon < -76 OR ap.lon > -38 OR ap.pais NOT IN ('AR', 'UY', 'CL', 'PY', 'BR', 'FK'))
ORDER BY m.fecha DESC, m.hora_local DESC
