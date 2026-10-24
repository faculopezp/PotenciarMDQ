-- Serie mensual larga 2001+: portal municipal hasta 2018 y ANAC desde 2019.
-- Validación en el empalme (2019): pasajeros municipales vs ANAC difieren ±4 % por mes.
-- Municipal "pasajeros por tramo" ≤ 2020 = ambos sentidos (comparable con ANAC); desde 2021 un
-- solo sentido (no se usa).
WITH mun AS (
  SELECT anio, mes,
         sum(valor) FILTER (dataset = 'pasajeros_tramo' AND unidad = 'pasajeros_ida_y_vuelta') AS pax_mun,
         sum(valor) FILTER (dataset = 'movimientos')                                         AS movs_mun
  FROM fct_municipal_mensual
  WHERE mes IS NOT NULL
  GROUP BY anio, mes
),
anac AS (
  SELECT anio, mes,
         sum(pasajeros) FILTER (es_linea)  AS pax_anac,
         count(*) FILTER (es_comercial)    AS movs_anac,
         bool_or(es_provisorio)            AS provisorio,
         count(DISTINCT fecha)             AS dias
  FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
  GROUP BY anio, mes
),
inicio_anac AS (SELECT min(anio) AS a FROM anac)
SELECT
  coalesce(a.anio, m.anio) AS anio,
  coalesce(a.mes, m.mes)   AS mes,
  make_date(coalesce(a.anio, m.anio), coalesce(a.mes, m.mes), 1) AS periodo,
  CASE WHEN a.anio IS NOT NULL THEN a.pax_anac ELSE m.pax_mun END   AS pasajeros,
  CASE WHEN a.anio IS NOT NULL THEN a.movs_anac ELSE m.movs_mun END AS movimientos_comerciales,
  CASE WHEN a.anio IS NOT NULL THEN 'ANAC' ELSE 'Municipio de General Pueyrredon' END AS fuente,
  m.pax_mun  AS pasajeros_municipal,
  m.movs_mun AS movimientos_municipal,
  coalesce(a.provisorio, false) AS tiene_provisorio
FROM anac a
FULL JOIN mun m USING (anio, mes)
WHERE coalesce(a.anio, m.anio) >= 2001
  AND (a.anio IS NOT NULL OR m.anio < (SELECT a FROM inicio_anac))
ORDER BY periodo
