-- Fuentes municipales (datos.mardelplata.gob.ar) integradas a la BD.
CREATE OR REPLACE TABLE fct_municipal_mensual AS
SELECT * FROM mun_series;

-- Movimientos individuales en MDQ 2015–2019 (portal municipal; sin pasajeros, hora sin minutos).
-- Segmentos con la misma lógica que fct_movimiento (no trae vuelos oficiales ni escuela).
CREATE OR REPLACE TABLE fct_mdq_vuelos_hist AS
SELECT
  h.fecha, year(h.fecha) AS anio, month(h.fecha) AS mes, h.hora_local,
  h.clase_vuelo, h.tipo_movimiento,
  coalesce(ap.codigo, h.origen_destino_oaci)      AS origen_destino,
  h.aerolinea, h.aeronave,
  coalesce(an.familia, 'Sin dato')                AS aeronave_familia,
  coalesce(an.categoria, 'sin_dato')              AS aeronave_categoria,
  CASE
    WHEN h.clase_vuelo = 'regular' THEN 'linea_regular'
    WHEN h.clase_vuelo = 'no_regular'
     AND list_contains(getvariable('categorias_linea'), an.categoria) THEN 'charter_linea'
    WHEN h.clase_vuelo = 'no_regular' THEN 'taxi_aereo'
    WHEN h.clase_vuelo LIKE 'vuelo_privado%' THEN 'privado'
    ELSE 'otro'
  END                                             AS segmento,
  h.archivo
FROM mun_vuelos_hist h
LEFT JOIN dim_aeronave an ON an.aeronave = h.aeronave
LEFT JOIN (SELECT oaci, any_value(codigo ORDER BY length(codigo)) AS codigo
           FROM dim_aeropuerto GROUP BY oaci) ap
  ON ap.oaci = h.origen_destino_oaci;
