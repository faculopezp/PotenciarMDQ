-- Micros con Mar del Plata en un extremo, por año y servicio (CNRT vía Yvera).
-- Pasajeros de las rutas con al menos un viaje semanal (piso, no total). La participación es sobre
-- el total nacional del mismo servicio y año; anio_completo = el archivo diario cubre el año entero.
WITH pais AS (
  SELECT servicio, year(fecha) AS anio, count(DISTINCT fecha) AS dias_con_datos,
         min(fecha) AS desde, max(fecha) AS hasta,
         sum(pasajeros) AS pasajeros_pais, sum(viajes) AS viajes_pais
  FROM fct_bus_nacional_diario
  GROUP BY ALL
),
mdq AS (
  SELECT servicio, anio,
         sum(pasajeros) FILTER (WHERE sentido = 'llegada') AS pasajeros_llegada,
         sum(pasajeros) FILTER (WHERE sentido = 'salida')  AS pasajeros_salida,
         sum(viajes)    FILTER (WHERE sentido = 'llegada') AS viajes_llegada,
         sum(viajes)    FILTER (WHERE sentido = 'salida')  AS viajes_salida,
         sum(asientos)  FILTER (WHERE sentido = 'llegada') AS asientos_llegada,
         sum(pasajeros) AS pasajeros,
         sum(asientos)  AS asientos,
         sum(viajes)    AS viajes,
         count(DISTINCT extremo_clave) AS extremos
  FROM fct_bus_ruta_anual
  GROUP BY ALL
)
SELECT m.servicio, m.anio,
       m.pasajeros_llegada, m.pasajeros_salida, m.viajes_llegada, m.viajes_salida,
       m.pasajeros, m.viajes, m.asientos, m.extremos,
       round(m.pasajeros / nullif(m.asientos, 0), 3)            AS ocupacion,
       round(m.pasajeros_llegada / nullif(m.asientos_llegada, 0), 3) AS ocupacion_llegada,
       round(m.pasajeros / nullif(m.viajes, 0), 1)              AS pasajeros_por_viaje,
       p.pasajeros_pais,
       round(m.pasajeros / nullif(p.pasajeros_pais, 0), 4)      AS share_pais,
       p.desde, p.hasta, p.dias_con_datos,
       coalesce(p.dias_con_datos >= 365, false)                 AS anio_completo
FROM mdq m
LEFT JOIN pais p USING (servicio, anio)
ORDER BY m.servicio, m.anio
