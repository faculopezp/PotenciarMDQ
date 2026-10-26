-- Micros con Mar del Plata en un extremo, por año y servicio (CNRT vía Yvera).
-- fuente: base por viaje (todas las rutas) o, en los años que esa base no cubre, el archivo anual
-- (solo rutas con al menos un viaje semanal: piso). La participación es sobre el total nacional del
-- mismo servicio y año; anio_completo = el rango del archivo diario cubre el año entero (en 2020
-- hubo días sin viajes por la pandemia: no se cuentan días, se mira el rango).
WITH rango AS (
  SELECT servicio, min(fecha) AS primero, max(fecha) AS ultimo
  FROM fct_bus_nacional_diario GROUP BY 1
),
pais AS (
  SELECT servicio, year(fecha) AS anio, count(DISTINCT fecha) AS dias_con_datos,
         min(fecha) AS desde, max(fecha) AS hasta,
         sum(pasajeros) AS pasajeros_pais, sum(viajes) AS viajes_pais
  FROM fct_bus_nacional_diario
  GROUP BY ALL
),
mdq AS (
  SELECT servicio, anio,
         sum(pasajeros) FILTER (WHERE sentido = 'llegada') AS pasajeros_llegada,
         sum(pasajeros) FILTER (WHERE sentido = 'salida')  AS pasajeros_salida,
         sum(viajes)    FILTER (WHERE sentido = 'llegada') AS viajes_llegada,
         sum(viajes)    FILTER (WHERE sentido = 'salida')  AS viajes_salida,
         sum(asientos)  FILTER (WHERE sentido = 'llegada') AS asientos_llegada,
         sum(pasajeros) AS pasajeros,
         sum(asientos)  AS asientos,
         sum(viajes)    AS viajes,
         count(DISTINCT extremo_clave) AS extremos,
         any_value(fuente) AS fuente,
         -- Rutas donde la fuente registra más pasajeros que asientos (ver reports/qa/omnibus.md).
         round(sum(pasajeros) FILTER (WHERE pasajeros > asientos) / sum(pasajeros), 3)
           AS share_pax_rutas_sobre_asientos
  FROM fct_bus_ruta_anual
  GROUP BY ALL
)
SELECT m.servicio, m.anio,
       m.pasajeros_llegada, m.pasajeros_salida, m.viajes_llegada, m.viajes_salida,
       m.pasajeros, m.viajes, m.asientos, m.extremos, m.fuente,
       coalesce(m.share_pax_rutas_sobre_asientos, 0) AS share_pax_rutas_sobre_asientos,
       round(m.pasajeros / nullif(m.asientos, 0), 3)            AS ocupacion,
       round(m.pasajeros_llegada / nullif(m.asientos_llegada, 0), 3) AS ocupacion_llegada,
       round(m.pasajeros / nullif(m.viajes, 0), 1)              AS pasajeros_por_viaje,
       p.pasajeros_pais,
       round(m.pasajeros / nullif(p.pasajeros_pais, 0), 4)      AS share_pais,
       p.desde, p.hasta, p.dias_con_datos,
       coalesce(r.primero <= make_date(m.anio, 1, 1) AND r.ultimo >= make_date(m.anio, 12, 31), false)
                                                                AS anio_completo
FROM mdq m
LEFT JOIN pais p USING (servicio, anio)
LEFT JOIN rango r USING (servicio)
ORDER BY m.servicio, m.anio
