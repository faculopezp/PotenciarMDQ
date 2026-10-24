-- Mapa de calor día de la semana × hora local: movimientos comerciales promedio por semana.
WITH semanas AS (
  SELECT anio, count(DISTINCT semana_iso) AS semanas FROM dim_fecha
  WHERE fecha BETWEEN (SELECT min(fecha) FROM fct_movimiento) AND (SELECT max(fecha) FROM fct_movimiento)
  GROUP BY anio
)
SELECT
  m.anio, m.dia_semana, m.dia_semana_nombre, m.hora_local,
  count(*)                                        AS movimientos,
  coalesce(sum(m.pasajeros), 0)                   AS pasajeros,
  round(count(*) / any_value(s.semanas), 2)       AS movimientos_por_semana
FROM fct_movimiento m
JOIN semanas s USING (anio)
WHERE m.aeropuerto = getvariable('foco') AND m.es_comercial AND m.hora_local IS NOT NULL
GROUP BY m.anio, m.dia_semana, m.dia_semana_nombre, m.hora_local
ORDER BY m.anio, m.dia_semana, m.hora_local
