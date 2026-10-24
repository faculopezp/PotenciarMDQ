-- Base liviana para el explorador interactivo de la web (réplica de la vieja consulta
-- interactiva de ANAC: filtros por tipo de vuelo, aerolínea, aeronave, mes, día y hora).
SELECT
  anio, mes, dia_semana, hora_local,
  es_comercial, segmento, clase_vuelo, clasificacion_vuelo, tipo_movimiento,
  aerolinea_nombre, aeronave_categoria,
  aeronave_familia_inferida AS aeronave_familia,   -- incluye 2019–2020 inferido por pasajeros
  origen_destino,
  count(*)                    AS movimientos,
  coalesce(sum(pasajeros), 0) AS pasajeros
FROM fct_movimiento
WHERE aeropuerto = getvariable('foco')
GROUP BY ALL
