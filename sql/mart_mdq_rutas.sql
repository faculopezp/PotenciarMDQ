-- Red de rutas desde/hacia MDQ por año, con coordenadas para el mapa (estilo tablero Yvera).
WITH r AS (
  SELECT
    anio, origen_destino AS codigo, any_value(clasificacion_vuelo) AS clasificacion_vuelo,
    count(*)                                         AS movimientos,
    count(*) FILTER (tipo_movimiento = 'despegue')   AS salidas,
    count(*) FILTER (tipo_movimiento = 'aterrizaje') AS llegadas,
    coalesce(sum(pasajeros), 0)                      AS pasajeros,
    round(sum(pasajeros) FILTER (asientos_estimados IS NOT NULL)
          / nullif(sum(asientos_estimados) FILTER (pasajeros IS NOT NULL), 0), 3) AS lf_estimado,
    string_agg(DISTINCT aerolinea_nombre, ', ' ORDER BY aerolinea_nombre) FILTER (aerolinea IS NOT NULL)
                                                     AS aerolineas,
    count(DISTINCT fecha) FILTER (tipo_movimiento = 'despegue') AS dias_con_salida,
    any_value(distancia_km)                          AS distancia_km
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') AND es_regular
  GROUP BY anio, origen_destino
),
dur AS (
  SELECT anio, destino AS codigo, median(duracion_min) AS duracion_mediana_min
  FROM fct_tramo WHERE origen = getvariable('foco') GROUP BY ALL
),
dias AS (
  SELECT anio, count(DISTINCT fecha) AS dias FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') GROUP BY anio
)
SELECT
  r.*,
  round(r.salidas / (d.dias / 7.0), 1) AS salidas_semanales_promedio,
  dur.duracion_mediana_min,
  ap.nombre, ap.ciudad, ap.pais, ap.lat, ap.lon,
  foco.lat AS foco_lat, foco.lon AS foco_lon
FROM r
JOIN dias d USING (anio)
LEFT JOIN dur USING (anio, codigo)
LEFT JOIN dim_aeropuerto ap ON ap.codigo = r.codigo
LEFT JOIN dim_aeropuerto foco ON foco.codigo = getvariable('foco')
ORDER BY anio, pasajeros DESC
