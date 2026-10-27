-- Procedencia de los turistas (EMTUR): % de cada región por mes, y turistas estimados = % × total
-- de turistas del mes. Las regiones cambian de nombre entre planillas y se unifican en el parser;
-- "Exterior" no se publica todos los años.
WITH p AS (
  SELECT anio, mes, serie AS region, valor AS porcentaje
  FROM fct_municipal_mensual WHERE dataset = 'procedencia'
),
t AS (
  SELECT anio, mes, sum(valor) AS turistas
  FROM fct_municipal_mensual WHERE dataset = 'arribos_turistas' GROUP BY ALL
)
SELECT p.anio, p.mes, make_date(p.anio, p.mes, 1) AS periodo, p.region, p.porcentaje,
       round(p.porcentaje / 100 * t.turistas) AS turistas
FROM p LEFT JOIN t USING (anio, mes)
ORDER BY p.anio, p.mes, p.region
