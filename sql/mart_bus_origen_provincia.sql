-- Micros de turismo (DUT) que llegan a Mar del Plata, por provincia de origen y año.
SELECT year(fecha) AS anio, coalesce(extremo_provincia, 'Sin dato') AS provincia,
       count(*) AS viajes, sum(pasajeros) AS pasajeros
FROM fct_bus_turismo
WHERE sentido = 'llegada'
GROUP BY ALL
ORDER BY anio, pasajeros DESC
