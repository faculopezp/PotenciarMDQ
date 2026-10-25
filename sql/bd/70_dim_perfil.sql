-- Perfil de cada familia de aeronave: jet ejecutivo, turbohélice (el "avión básico" del taxi
-- aéreo es el turbohélice más frecuente), pistón, helicóptero, avión de línea. La división del
-- pistón por plazas se hace por movimiento en mart_mdq_perfil_aeronave. Capacidad = p95 de pasajeros de la
-- familia en vuelos que no son de línea, en todo el país (mínimo 30 vuelos con pasajeros).
CREATE OR REPLACE TABLE dim_perfil_familia AS
WITH fam AS (
  SELECT aeronave_familia, mode(aeronave_categoria) AS aeronave_categoria, count(*) AS movimientos
  FROM fct_movimiento GROUP BY 1
),
cap AS (
  SELECT aeronave_familia, round(quantile_cont(pasajeros, 0.95)) AS capacidad_ga_p95,
         count(*) AS vuelos_con_pax
  FROM fct_movimiento WHERE NOT es_linea AND pasajeros > 0
  GROUP BY 1 HAVING count(*) >= 30
)
SELECT
  f.aeronave_familia, f.aeronave_categoria, c.capacidad_ga_p95, c.vuelos_con_pax,
  CASE
    WHEN f.aeronave_categoria = 'jet_ejecutivo' THEN 'jet_ejecutivo'
    WHEN f.aeronave_categoria = 'turbohelice_ejecutivo' THEN 'turbohelice'
    WHEN f.aeronave_categoria = 'aviacion_general_piston' THEN 'piston'
    WHEN f.aeronave_categoria = 'helicoptero' THEN 'helicoptero'
    WHEN list_contains(getvariable('categorias_linea'), f.aeronave_categoria) THEN 'avion_de_linea'
    ELSE 'sin_dato'
  END AS perfil
FROM fam f LEFT JOIN cap c USING (aeronave_familia);
