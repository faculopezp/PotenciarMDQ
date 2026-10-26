-- Micros de turismo (DUT) con Mar del Plata en un extremo, por mes: cada fila de la base es un
-- servicio. Meses de la base sin datos del foco quedan en cero (no faltantes).
WITH meses AS (
  SELECT DISTINCT date_trunc('month', fecha) AS mes FROM fct_bus_nacional_diario
  WHERE servicio = 'turismo'
),
mdq AS (
  SELECT date_trunc('month', fecha) AS mes,
         count(*) FILTER (WHERE sentido = 'llegada')          AS viajes_llegada,
         count(*) FILTER (WHERE sentido = 'salida')           AS viajes_salida,
         sum(pasajeros) FILTER (WHERE sentido = 'llegada')    AS pasajeros_llegada,
         sum(pasajeros) FILTER (WHERE sentido = 'salida')     AS pasajeros_salida,
         sum(asientos)                                        AS asientos,
         sum(pasajeros)                                       AS pasajeros
  FROM fct_bus_turismo
  GROUP BY 1
)
SELECT 'turismo' AS servicio, year(m.mes) AS anio, month(m.mes) AS mes,
       coalesce(d.viajes_llegada, 0)    AS viajes_llegada,
       coalesce(d.viajes_salida, 0)     AS viajes_salida,
       coalesce(d.pasajeros_llegada, 0) AS pasajeros_llegada,
       coalesce(d.pasajeros_salida, 0)  AS pasajeros_salida,
       round(d.pasajeros / nullif(d.asientos, 0), 3) AS ocupacion
FROM meses m
LEFT JOIN mdq d USING (mes)
ORDER BY m.mes
