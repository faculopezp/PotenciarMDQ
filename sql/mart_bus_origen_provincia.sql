-- Micros que llegan a Mar del Plata, por provincia de origen, año y servicio (bases por viaje).
SELECT servicio, year(fecha) AS anio,
       coalesce(replace(l.provincia, ' De ', ' de '), 'Sin dato') AS provincia,
       count(*) AS viajes, sum(pasajeros) AS pasajeros
FROM fct_bus_viaje v
LEFT JOIN dim_bus_localidad l ON l.clave = bus_clave(v.extremo_crudo)
WHERE sentido = 'llegada'
GROUP BY ALL
ORDER BY servicio, anio, pasajeros DESC
