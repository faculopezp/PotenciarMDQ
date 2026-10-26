-- Tren a Mar del Plata: pasajeros pagos por año y operador (en 2011–2015 corrieron dos a la vez).
SELECT anio, operador_nombre AS operador, sum(pax) AS pasajeros, count(DISTINCT mes) AS meses
FROM fct_tren_mensual
WHERE es_foco
GROUP BY ALL
ORDER BY anio, pasajeros DESC
