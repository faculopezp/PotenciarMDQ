-- Tren a Mar del Plata por año, con el total de larga distancia del país para comparar.
-- meses = meses con dato del foco; meses_archivo = meses que trae la planilla ese año.
WITH pais AS (
  SELECT anio, count(DISTINCT mes) AS meses_archivo,
         sum(pax) FILTER (WHERE tipo_servicio = 'Larga Distancia') AS pasajeros_larga_distancia_pais
  FROM fct_tren_mensual GROUP BY anio
),
foco AS (
  SELECT anio, count(DISTINCT mes) AS meses, sum(pax) AS pasajeros,
         string_agg(DISTINCT operador, ' · ') AS operadores
  FROM fct_tren_mensual WHERE es_foco GROUP BY anio
)
SELECT p.anio, coalesce(f.pasajeros, 0) AS pasajeros, coalesce(f.meses, 0) AS meses,
       p.meses_archivo, f.operadores, p.pasajeros_larga_distancia_pais,
       round(f.pasajeros / nullif(p.pasajeros_larga_distancia_pais, 0), 4) AS share_larga_distancia,
       p.meses_archivo = 12 AS anio_completo
FROM pais p LEFT JOIN foco f USING (anio)
ORDER BY p.anio
