-- Micros: cada localidad conectada con Mar del Plata, por año y servicio (CNRT vía Yvera).
SELECT r.servicio, r.anio, l.nombre AS extremo, l.provincia,
       sum(r.pasajeros) FILTER (WHERE r.sentido = 'llegada') AS pasajeros_llegada,
       sum(r.pasajeros) FILTER (WHERE r.sentido = 'salida')  AS pasajeros_salida,
       sum(r.pasajeros)                                      AS pasajeros,
       sum(r.viajes)                                         AS viajes,
       sum(r.asientos)                                       AS asientos,
       round(sum(r.pasajeros) / nullif(sum(r.asientos), 0), 3) AS ocupacion
FROM fct_bus_ruta_anual r
JOIN dim_bus_localidad l ON l.clave = r.extremo_clave
GROUP BY ALL
ORDER BY r.servicio, r.anio, pasajeros DESC
