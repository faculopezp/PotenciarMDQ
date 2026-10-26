-- Cobertura de cada dato en el foco, por año y alcance (línea / resto / todos): qué parte de los
-- movimientos tiene operador, aeronave y asientos, después de la recuperación
-- (sql/bd/25_recuperacion.sql). La web lo muestra al pie de cada gráfico que depende de esos datos.
WITH b AS (
  SELECT anio, CASE WHEN es_linea THEN 'linea' ELSE 'resto' END AS alcance,
         aerolinea, aerolinea_original, aeronave, aeronave_inferida, aeronave_familia_inferida,
         asientos_estimados, pasajeros
  FROM fct_movimiento WHERE aeropuerto = getvariable('foco')
),
t AS (
  SELECT anio, alcance, * EXCLUDE (anio, alcance) FROM b
  UNION ALL
  SELECT anio, 'todos', * EXCLUDE (anio, alcance) FROM b
)
SELECT
  anio, alcance, count(*) AS movimientos,
  round(count(aerolinea_original) / count(*), 4)                                AS pct_operador_anac,
  round(count(aerolinea) / count(*), 4)                                         AS pct_operador,
  round(count(*) FILTER (aeronave IS NOT NULL AND NOT aeronave_inferida) / count(*), 4)
                                                                                AS pct_aeronave,
  round(count(*) FILTER (aeronave_familia_inferida <> 'Sin dato') / count(*), 4) AS pct_aeronave_con_inferida,
  round(count(asientos_estimados) / count(*), 4)                                AS pct_asientos,
  round(count(pasajeros) / count(*), 4)                                         AS pct_pasajeros
FROM t
GROUP BY anio, alcance
ORDER BY anio, alcance
