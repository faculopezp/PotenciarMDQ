-- Actividad por segmento y año con la mayor profundidad disponible:
-- 2015–2018 portal municipal (línea, charter, taxi aéreo, privado; sin oficiales ni escuela) y 2019+ ANAC.
-- OJO: el archivo municipal de vuelos es una muestra (~50 % de los movimientos comerciales según la
-- serie municipal de movimientos): usar para composición (%), no para totales. Ver `cobertura`.
WITH hist AS (
  SELECT anio, segmento, aeronave_familia, aeronave_categoria, count(*) AS movimientos,
         'Municipio de General Pueyrredon (muestra)' AS fuente
  FROM fct_mdq_vuelos_hist
  WHERE anio < (SELECT min(anio) FROM fct_movimiento)
    AND anio IN (SELECT anio FROM fct_mdq_vuelos_hist GROUP BY anio HAVING count(DISTINCT mes) = 12)
  GROUP BY ALL
),
cob AS (
  SELECT h.anio,
         round(sum(h.movimientos) FILTER (h.segmento IN ('linea_regular', 'charter_linea', 'taxi_aereo'))
               / nullif(any_value(m.movs), 0), 3) AS cobertura
  FROM hist h
  JOIN (SELECT anio, sum(valor) AS movs FROM fct_municipal_mensual
        WHERE dataset = 'movimientos' GROUP BY anio) m USING (anio)
  GROUP BY h.anio
),
anac AS (
  SELECT anio, segmento, aeronave_familia, aeronave_categoria, count(*) AS movimientos,
         'ANAC' AS fuente, 1.0 AS cobertura
  FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
  GROUP BY ALL
)
SELECT hist.*, cob.cobertura FROM hist LEFT JOIN cob USING (anio)
UNION ALL BY NAME
SELECT * FROM anac
ORDER BY anio, segmento, movimientos DESC
