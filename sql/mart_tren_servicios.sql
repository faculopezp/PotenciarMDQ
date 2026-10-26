-- Servicios de larga distancia del país por año: dónde se ubica el de Mar del Plata.
SELECT anio, servicio, any_value(operador) AS operador, bool_or(es_foco) AS es_foco,
       sum(pax) AS pasajeros, count(DISTINCT mes) AS meses
FROM fct_tren_mensual
WHERE tipo_servicio = 'Larga Distancia'
GROUP BY anio, servicio
ORDER BY anio, pasajeros DESC
