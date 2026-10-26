-- Turistas residentes con destino Mar del Plata por región de residencia y año (EVyTH).
WITH t AS (
  SELECT anio, region_origen, sum(pondera) AS turistas, count(*) AS n
  FROM fct_evyth_mdq WHERE tipo_visitante = 'turista'
  GROUP BY ALL
)
SELECT anio, region_origen, round(turistas) AS turistas, n,
       round(turistas / sum(turistas) OVER (PARTITION BY anio), 4) AS share
FROM t
ORDER BY anio, turistas DESC
