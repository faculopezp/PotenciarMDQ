-- Pulso diario (estilo EUROCONTROL): pasajeros y vuelos comerciales por día, media móvil 7 días y
-- comparación con el mismo día de la semana del año anterior (t - 364 días).
WITH d AS (
  SELECT
    fecha,
    count(*)                                                            AS movimientos_comerciales,
    coalesce(sum(pasajeros), 0)                                         AS pasajeros,
    coalesce(sum(pasajeros) FILTER (tipo_movimiento = 'aterrizaje'), 0) AS pasajeros_llegados,
    coalesce(sum(pasajeros) FILTER (tipo_movimiento = 'despegue'), 0)   AS pasajeros_salidos
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') AND es_comercial
  GROUP BY fecha
),
c AS (
  SELECT f.fecha, f.anio, f.mes, f.dia_semana, f.dia_semana_nombre, f.es_feriado, f.feriado_nombre,
         f.es_finde_largo, f.verano_anio,
         coalesce(d.movimientos_comerciales, 0) AS movimientos_comerciales,
         coalesce(d.pasajeros, 0)               AS pasajeros,
         coalesce(d.pasajeros_llegados, 0)      AS pasajeros_llegados,
         coalesce(d.pasajeros_salidos, 0)       AS pasajeros_salidos
  FROM dim_fecha f
  LEFT JOIN d USING (fecha)
  WHERE f.fecha BETWEEN (SELECT min(fecha) FROM d) AND (SELECT max(fecha) FROM d)
),
ma AS (
  SELECT *,
    pasajeros_llegados - pasajeros_salidos AS balance_pasajeros,
    round(avg(pasajeros) OVER w, 1)               AS pasajeros_ma7,
    round(avg(movimientos_comerciales) OVER w, 2) AS movimientos_ma7
  FROM c
  WINDOW w AS (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
)
SELECT
  a.*,
  b.pasajeros_ma7                                                  AS pasajeros_ma7_anio_anterior,
  round(a.pasajeros_ma7 / nullif(b.pasajeros_ma7, 0) - 1, 4)       AS var_ma7_interanual
FROM ma a
LEFT JOIN ma b ON b.fecha = a.fecha - INTERVAL 364 DAY
ORDER BY a.fecha
