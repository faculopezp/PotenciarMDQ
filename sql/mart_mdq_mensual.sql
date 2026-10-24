-- Serie mensual MDQ: volumen, oferta estimada, flujo direccional y estacionalidad.
WITH m AS (
  SELECT
    anio, mes,
    count(*)                                                            AS movimientos,
    count(*) FILTER (es_comercial)                                      AS movimientos_comerciales,
    count(*) FILTER (NOT es_comercial)                                  AS movimientos_otros,
    coalesce(sum(pasajeros), 0)                                         AS pasajeros,
    coalesce(sum(pasajeros) FILTER (es_comercial), 0)                   AS pasajeros_comerciales,
    coalesce(sum(pasajeros) FILTER (tipo_movimiento = 'aterrizaje'), 0) AS pasajeros_llegados,
    coalesce(sum(pasajeros) FILTER (tipo_movimiento = 'despegue'), 0)   AS pasajeros_salidos,
    coalesce(sum(pasajeros) FILTER (clasificacion_vuelo = 'internacional'), 0) AS pasajeros_internacional,
    sum(asientos_estimados)                                             AS asientos_estimados,
    round(sum(pasajeros) FILTER (asientos_estimados IS NOT NULL)
          / nullif(sum(asientos_estimados) FILTER (pasajeros IS NOT NULL), 0), 3) AS lf_estimado,
    count(DISTINCT aerolinea_nombre) FILTER (es_comercial AND aerolinea IS NOT NULL) AS aerolineas_activas,
    count(DISTINCT origen_destino) FILTER (es_regular)                  AS destinos_regulares,
    bool_or(es_provisorio)                                              AS tiene_provisorio
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco')
  GROUP BY anio, mes
)
SELECT
  *,
  make_date(anio, mes, 1)                                               AS periodo,
  pasajeros_llegados - pasajeros_salidos                                AS balance_pasajeros,
  round(pasajeros_comerciales / nullif(movimientos_comerciales, 0), 1)  AS pax_por_mov_comercial,
  round(pasajeros / nullif(avg(pasajeros) OVER (PARTITION BY anio), 0), 3) AS indice_estacional,
  count(*) OVER (PARTITION BY anio)                                     AS meses_con_datos_anio,
  round(pasajeros / nullif(lag(pasajeros) OVER (PARTITION BY mes ORDER BY anio), 0) - 1, 4) AS var_interanual
FROM m
ORDER BY anio, mes
