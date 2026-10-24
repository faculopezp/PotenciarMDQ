-- Avión vs turismo: turistas arribados a Mar del Plata (EMTURyC, todos los medios) y pasajeros aéreos.
-- llegados_aereos: ANAC (aterrizajes) desde 2019; antes ≈ pasajeros ida y vuelta / 2.
WITH t AS (
  SELECT anio, mes,
         sum(valor) FILTER (dataset = 'arribos_turistas')  AS turistas,
         sum(valor) FILTER (dataset = 'turistas_estables') AS turistas_estables,
         avg(valor) FILTER (dataset = 'estadia_promedio')  AS estadia_promedio_noches
  FROM fct_municipal_mensual WHERE mes IS NOT NULL GROUP BY anio, mes
),
lleg AS (
  SELECT anio, mes, sum(pasajeros) FILTER (tipo_movimiento = 'aterrizaje' AND es_linea) AS llegados
  FROM fct_movimiento WHERE aeropuerto = getvariable('foco') GROUP BY anio, mes
),
s AS (SELECT anio, mes, pasajeros, fuente FROM read_parquet(getvariable('marts_dir') || '/mart_mdq_serie_larga.parquet'))
SELECT
  t.anio, t.mes, make_date(t.anio, t.mes, 1) AS periodo,
  t.turistas, t.turistas_estables, t.estadia_promedio_noches,
  s.pasajeros AS pasajeros_aereos,
  coalesce(l.llegados, round(s.pasajeros / 2)) AS llegados_aereos,
  CASE WHEN l.llegados IS NOT NULL THEN 'ANAC' ELSE 'estimado (ida y vuelta / 2)' END AS fuente_llegados,
  round(coalesce(l.llegados, s.pasajeros / 2) / nullif(t.turistas, 0), 5) AS share_turistas_en_avion
FROM t
LEFT JOIN s USING (anio, mes)
LEFT JOIN lleg l USING (anio, mes)
WHERE t.turistas IS NOT NULL
ORDER BY periodo
