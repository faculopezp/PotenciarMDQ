-- Temporada de verano (dic + ene + feb; diciembre cuenta para el verano siguiente) por destino.
-- Para comparar temporadas estilo "oferta de verano" de Aviacionline.
SELECT
  m.verano_anio,
  m.origen_destino                                AS codigo,
  ap.ciudad,
  count(*)                                        AS movimientos,
  count(*) FILTER (m.tipo_movimiento = 'despegue') AS salidas,
  coalesce(sum(m.pasajeros), 0)                   AS pasajeros,
  sum(m.asientos_estimados)                       AS asientos_estimados,
  count(DISTINCT m.fecha)                         AS dias_con_datos
FROM fct_movimiento m
LEFT JOIN dim_aeropuerto ap ON ap.codigo = m.origen_destino
WHERE m.aeropuerto = getvariable('foco') AND m.es_comercial AND m.verano_anio IS NOT NULL
GROUP BY m.verano_anio, m.origen_destino, ap.ciudad
ORDER BY m.verano_anio, pasajeros DESC
