-- Micros con Mar del Plata en un extremo, por mes y servicio, desde las bases por viaje (cada fila
-- es un servicio). Meses que el total país cubre sin viajes del foco quedan en cero.
WITH meses AS (
  SELECT DISTINCT servicio, date_trunc('month', fecha) AS mes FROM fct_bus_nacional_diario
),
mdq AS (
  SELECT servicio, date_trunc('month', fecha) AS mes,
         count(*) FILTER (WHERE sentido = 'llegada')          AS viajes_llegada,
         count(*) FILTER (WHERE sentido = 'salida')           AS viajes_salida,
         sum(pasajeros) FILTER (WHERE sentido = 'llegada')    AS pasajeros_llegada,
         sum(pasajeros) FILTER (WHERE sentido = 'salida')     AS pasajeros_salida
  FROM fct_bus_viaje
  GROUP BY ALL
),
cubiertos AS (SELECT DISTINCT servicio FROM fct_bus_viaje)
SELECT m.servicio, year(m.mes) AS anio, month(m.mes) AS mes,
       coalesce(d.viajes_llegada, 0)    AS viajes_llegada,
       coalesce(d.viajes_salida, 0)     AS viajes_salida,
       coalesce(d.pasajeros_llegada, 0) AS pasajeros_llegada,
       coalesce(d.pasajeros_salida, 0)  AS pasajeros_salida
FROM meses m
SEMI JOIN cubiertos c ON c.servicio = m.servicio
LEFT JOIN mdq d USING (servicio, mes)
-- Solo meses dentro del rango de la base de ese servicio.
WHERE m.mes BETWEEN (SELECT date_trunc('month', min(fecha)) FROM fct_bus_viaje v WHERE v.servicio = m.servicio)
                AND (SELECT date_trunc('month', max(fecha)) FROM fct_bus_viaje v WHERE v.servicio = m.servicio)
ORDER BY m.servicio, m.mes
