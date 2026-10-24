-- "Avión típico" de cada segmento: top 3 familias por movimientos y top 3 por pasajeros, por año,
-- más el "avión básico" (familia más frecuente con perfil turbohélice 5+ pax, ver dim_perfil_familia).
-- En taxi aéreo difieren: la avioneta más frecuente casi no lleva pasajeros; el jet ejecutivo sí.
-- capacidad_observada_p95: percentil 95 de pasajeros de esa familia en ese segmento en todo el país
-- (proxy de cuántos pasajeros lleva "lleno"; para taxis aéreos y privados es pasajeros, no asientos).
WITH b AS (
  SELECT * FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') AND aeronave_familia NOT IN ('Sin dato', 'Otra')
),
fam AS (
  SELECT
    anio, segmento, aeronave_familia, any_value(aeronave_categoria) AS aeronave_categoria,
    count(*)                                  AS movimientos,
    coalesce(sum(pasajeros), 0)               AS pasajeros,
    round(avg(pasajeros), 2)                  AS pax_promedio,
    max(pasajeros)                            AS pax_maximo,
    mode(hora_local)                          AS hora_mas_frecuente,
    round(count(*) FILTER (es_vuelo_local) / count(*), 4) AS share_vuelos_locales,
    count(DISTINCT matricula)                 AS matriculas
  FROM b GROUP BY ALL
),
destinos AS (
  SELECT anio, segmento, aeronave_familia,
         string_agg(origen_destino, ', ' ORDER BY n DESC) AS principales_origenes_destinos
  FROM (
    SELECT *, row_number() OVER (PARTITION BY anio, segmento, aeronave_familia ORDER BY n DESC) AS r
    FROM (
      SELECT anio, segmento, aeronave_familia, origen_destino, count(*) AS n
      FROM b WHERE NOT es_vuelo_local AND origen_destino IS NOT NULL
      GROUP BY anio, segmento, aeronave_familia, origen_destino
    )
  ) WHERE r <= 3
  GROUP BY anio, segmento, aeronave_familia
),
cap AS (
  SELECT segmento, aeronave_familia, round(quantile_cont(pasajeros, 0.95)) AS capacidad_observada_p95,
         count(*) AS n_pais
  FROM fct_movimiento WHERE pasajeros > 0 GROUP BY ALL HAVING count(*) >= 30
),
rot AS (
  SELECT anio, segmento, aeronave_familia, median(tiempo_en_tierra_min) AS tiempo_en_tierra_mediano_min
  FROM fct_rotacion WHERE aeropuerto = getvariable('foco') AND tipo_rotacion <> 'pernocte'
  GROUP BY ALL
),
dur AS (
  SELECT anio, aeronave_familia, median(duracion_min) AS duracion_vuelo_mediana_min
  FROM fct_tramo WHERE origen = getvariable('foco') OR destino = getvariable('foco') GROUP BY ALL
)
SELECT
  f.*,
  p.perfil,
  row_number() OVER (PARTITION BY f.anio, f.segmento ORDER BY f.movimientos DESC) AS ranking,
  row_number() OVER (PARTITION BY f.anio, f.segmento, p.perfil ORDER BY f.movimientos DESC)
                                                                                     AS ranking_en_perfil,
  row_number() OVER (PARTITION BY f.anio, f.segmento ORDER BY f.pasajeros DESC, f.movimientos DESC)
                                                                                     AS ranking_por_pasajeros,
  round(f.movimientos / sum(f.movimientos) OVER (PARTITION BY f.anio, f.segmento), 4) AS share_en_segmento,
  c.capacidad_observada_p95,
  r.tiempo_en_tierra_mediano_min,
  d.duracion_vuelo_mediana_min,
  ds.principales_origenes_destinos
FROM fam f
LEFT JOIN cap c USING (segmento, aeronave_familia)
LEFT JOIN rot r USING (anio, segmento, aeronave_familia)
LEFT JOIN dur d USING (anio, aeronave_familia)
LEFT JOIN destinos ds USING (anio, segmento, aeronave_familia)
LEFT JOIN dim_perfil_familia p USING (aeronave_familia)
QUALIFY ranking <= 3 OR ranking_por_pasajeros <= 3
     OR (p.perfil = 'turbohelice_basico' AND ranking_en_perfil = 1)
ORDER BY f.anio, f.segmento, ranking
