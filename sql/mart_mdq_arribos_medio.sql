-- Turistas por medio de transporte (EMTUR, modelo municipal) por mes, junto a lo que se mide por
-- cada vía: avión (ANAC, pasajeros de línea que aterrizan), micro (CNRT, pasajeros de servicios
-- con destino Mar del Plata, regular + turismo) y tren (CNRT, pasajeros pagos del servicio; ida y
-- vuelta). Sirve para ver la temporada por vía y qué tan cerca está el modelo de los conteos.
WITH emtur AS (
  SELECT anio, mes,
         sum(valor) FILTER (WHERE serie = 'auto')    AS auto,
         sum(valor) FILTER (WHERE serie = 'omnibus') AS omnibus,
         sum(valor) FILTER (WHERE serie = 'tren')    AS tren,
         sum(valor) FILTER (WHERE serie = 'avion')   AS avion
  FROM fct_municipal_mensual WHERE dataset = 'arribos_medio'
  GROUP BY ALL
),
turistas AS (
  SELECT anio, mes, sum(valor) AS turistas
  FROM fct_municipal_mensual WHERE dataset = 'arribos_turistas' GROUP BY ALL
),
avion AS (
  SELECT anio, mes, sum(pasajeros) AS avion_anac
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') AND tipo_movimiento = 'aterrizaje' AND es_linea
  GROUP BY ALL
),
micro AS (
  SELECT year(fecha) AS anio, month(fecha) AS mes, sum(pasajeros) AS micro_cnrt
  FROM fct_bus_viaje WHERE sentido = 'llegada' GROUP BY ALL
),
tren AS (
  SELECT anio, mes, sum(pax) AS tren_cnrt_ida_vuelta
  FROM fct_tren_mensual WHERE es_foco GROUP BY ALL
)
SELECT e.anio, e.mes, make_date(e.anio, e.mes, 1) AS periodo,
       e.auto, e.omnibus, e.tren, e.avion,
       e.auto + e.omnibus + e.tren + e.avion          AS total_medios,
       t.turistas,
       a.avion_anac, m.micro_cnrt, r.tren_cnrt_ida_vuelta
FROM emtur e
LEFT JOIN turistas t USING (anio, mes)
LEFT JOIN avion a USING (anio, mes)
LEFT JOIN micro m USING (anio, mes)
LEFT JOIN tren r USING (anio, mes)
ORDER BY e.anio, e.mes
