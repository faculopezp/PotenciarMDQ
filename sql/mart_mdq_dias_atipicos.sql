-- Días atípicos (gráfico de control): pasajeros de línea vs lo esperado para ese día de la semana
-- en las 3 semanas anteriores y posteriores (mediana). z robusto con la desviación absoluta mediana.
-- Se cruza con el clima diario (Open-Meteo) cuando está disponible.
WITH d AS (
  SELECT f.fecha, f.anio, f.mes, f.dia_semana, f.es_feriado, f.feriado_nombre, f.es_finde_largo,
         coalesce(sum(m.pasajeros), 0) AS pasajeros,
         count(m.movimiento_id)        AS movimientos
  FROM dim_fecha f
  LEFT JOIN fct_movimiento m
    ON m.fecha = f.fecha AND m.aeropuerto = getvariable('foco') AND m.es_linea
  WHERE f.fecha BETWEEN (SELECT min(fecha) FROM fct_movimiento) AND (SELECT max(fecha) FROM fct_movimiento)
  GROUP BY ALL
),
e AS (
  SELECT *,
    median(pasajeros) OVER (PARTITION BY dia_semana ORDER BY fecha
                            ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING) AS esperado,
    median(movimientos) OVER (PARTITION BY dia_semana ORDER BY fecha
                              ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING) AS movimientos_esperados
  FROM d
),
r AS (
  SELECT *, pasajeros - esperado AS desvio FROM e
),
s AS (
  SELECT anio, 1.4826 * median(abs(desvio)) AS escala FROM r GROUP BY anio
)
SELECT
  r.*,
  round(r.desvio / nullif(r.esperado, 0), 4)                AS desvio_pct,
  round(r.desvio / nullif(s.escala, 0), 2)                  AS z,
  abs(r.desvio / nullif(s.escala, 0)) >= 3                  AS es_atipico,
  c.codigo_tiempo, c.precipitacion_mm, c.viento_max_kmh, c.rafaga_max_kmh,
  CASE
    WHEN c.codigo_tiempo IN (95, 96, 99)                    THEN 'tormenta'
    WHEN c.codigo_tiempo IN (45, 48)                        THEN 'niebla'
    WHEN c.rafaga_max_kmh >= 70                             THEN 'viento fuerte'
    WHEN c.precipitacion_mm >= 20                           THEN 'lluvia fuerte'
    WHEN c.codigo_tiempo IS NULL                            THEN NULL
    ELSE 'normal'
  END                                                       AS condicion
FROM r
JOIN s USING (anio)
LEFT JOIN dim_clima c USING (fecha)
ORDER BY r.fecha
