-- Turistas residentes con destino Mar del Plata por medio de transporte y año (EVyTH, expandido).
-- n = encuestados (casos sin expandir): con pocos casos la estimación es poco precisa.
WITH t AS (
  SELECT anio, medio, sum(pondera) AS turistas, count(*) AS n
  FROM fct_evyth_mdq WHERE tipo_visitante = 'turista'
  GROUP BY ALL
),
cob AS (
  SELECT anio, count(DISTINCT trimestre) AS trimestres, count(*) AS n_anio
  FROM fct_evyth_mdq WHERE tipo_visitante = 'turista' GROUP BY anio
)
SELECT t.anio, t.medio, round(t.turistas) AS turistas, t.n,
       round(t.turistas / sum(t.turistas) OVER (PARTITION BY t.anio), 4) AS share,
       r.trimestres, r.n_anio, r.trimestres = 4 AS anio_completo
FROM t JOIN cob r USING (anio)
ORDER BY t.anio, t.turistas DESC
