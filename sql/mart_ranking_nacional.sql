-- Ranking de aeropuertos argentinos por pasajeros de línea (estilo lapanquecita), MDQ resaltado.
WITH a AS (
  SELECT m.anio, m.aeropuerto AS codigo,
         coalesce(sum(m.pasajeros) FILTER (m.es_linea), 0) AS pasajeros_linea,
         count(*) FILTER (m.es_linea)                      AS movimientos_linea,
         count(*)                                          AS movimientos_totales,
         count(DISTINCT m.mes)                             AS meses_con_datos
  FROM fct_movimiento m
  JOIN dim_aeropuerto ap ON ap.codigo = m.aeropuerto AND ap.pais = 'AR'
  GROUP BY m.anio, m.aeropuerto
)
SELECT
  a.*, ap.ciudad, ap.nombre,
  a.codigo = getvariable('foco') AS es_foco,
  list_contains(getvariable('pares'), a.codigo) AS es_par,
  rank() OVER (PARTITION BY a.anio ORDER BY a.pasajeros_linea DESC)   AS ranking_pasajeros,
  rank() OVER (PARTITION BY a.anio ORDER BY a.movimientos_totales DESC) AS ranking_movimientos
FROM a
JOIN dim_aeropuerto ap USING (codigo)
WHERE a.pasajeros_linea > 0
ORDER BY a.anio, ranking_pasajeros
