-- Tren a Mar del Plata: pasajeros pagos por mes (todos los servicios que llegan a la ciudad).
SELECT anio, mes, periodo,
       sum(pax)                                   AS pasajeros,
       string_agg(DISTINCT operador, ' · ')       AS operadores,
       string_agg(DISTINCT servicio, ' · ')       AS servicios
FROM fct_tren_mensual
WHERE es_foco
GROUP BY ALL
ORDER BY periodo
