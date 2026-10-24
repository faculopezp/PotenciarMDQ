-- Operadores (taxis aéreos, escuelas, organismos) y de dónde vienen, fuera de la aviación de línea.
WITH b AS (
  SELECT m.*, ap.ciudad FROM fct_movimiento m
  LEFT JOIN dim_aeropuerto ap ON ap.codigo = m.origen_destino
  WHERE m.aeropuerto = getvariable('foco') AND NOT m.es_linea
),
u AS (
  SELECT 'operador' AS dimension, anio, segmento, aerolinea_nombre AS valor FROM b
  UNION ALL
  SELECT 'origen_destino', anio, segmento,
         CASE WHEN es_vuelo_local THEN 'Vuelo local (MDQ–MDQ)'
              ELSE coalesce(ciudad || ' (' || origen_destino || ')', origen_destino) END
  FROM b
),
c AS (
  SELECT dimension, anio, segmento, valor, count(*) AS movimientos
  FROM u GROUP BY dimension, anio, segmento, valor
)
SELECT * FROM c
QUALIFY row_number() OVER (PARTITION BY dimension, anio, segmento ORDER BY movimientos DESC) <= 10
ORDER BY dimension, anio, segmento, movimientos DESC
