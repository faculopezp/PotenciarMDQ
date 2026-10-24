-- Visitantes por fin de semana largo (EMTURyC) por año y feriado.
SELECT anio, serie AS feriado, valor AS visitantes
FROM fct_municipal_mensual
WHERE dataset = 'findes_largos'
ORDER BY anio, visitantes DESC
