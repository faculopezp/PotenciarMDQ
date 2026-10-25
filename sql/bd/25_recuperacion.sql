-- Recuperación de datos faltantes con cruces exactos (sin suponer). Ver reports/qa/auditoria.md.
-- Clave de un registro de stg_movimiento: fecha, hora_utc, aeropuerto, tipo, origen/destino, operador.

-- 1. Operador por matrícula, unánime: la matrícula voló con un único operador en todos los
--    registros que lo informan (y son al menos 2).
CREATE OR REPLACE TABLE ref_operador_matricula AS
SELECT matricula, any_value(aerolinea) AS aerolinea
FROM stg_movimiento
WHERE matricula IS NOT NULL AND aerolinea IS NOT NULL
GROUP BY matricula
HAVING count(DISTINCT aerolinea) = 1 AND count(*) >= 2;

-- 2. Operador por el otro extremo del mismo vuelo: mismo avión (matrícula), aeropuertos cruzados,
--    movimiento opuesto, entre 10 minutos y 10 horas; solo si hay un único candidato.
CREATE OR REPLACE TABLE ref_operador_par AS
WITH m AS (
  SELECT fecha, hora_utc, aeropuerto, tipo_movimiento, origen_destino, matricula, aerolinea,
         CAST(fecha + hora_utc AS TIMESTAMP) AS ts
  FROM stg_movimiento
  WHERE matricula IS NOT NULL AND hora_utc IS NOT NULL AND origen_destino IS NOT NULL
    AND aeropuerto <> origen_destino
),
k AS (
  SELECT a.fecha, a.hora_utc, a.aeropuerto, a.tipo_movimiento, a.origen_destino, a.matricula,
         b.aerolinea, count(*) OVER (PARTITION BY a.fecha, a.hora_utc, a.aeropuerto,
                                     a.tipo_movimiento, a.origen_destino, a.matricula) AS candidatos
  FROM m a JOIN m b
    ON b.matricula = a.matricula AND b.aeropuerto = a.origen_destino
   AND b.origen_destino = a.aeropuerto AND b.tipo_movimiento <> a.tipo_movimiento
   AND ((a.tipo_movimiento = 'aterrizaje' AND b.ts BETWEEN a.ts - INTERVAL 10 HOUR AND a.ts - INTERVAL 10 MINUTE)
     OR (a.tipo_movimiento = 'despegue' AND b.ts BETWEEN a.ts + INTERVAL 10 MINUTE AND a.ts + INTERVAL 10 HOUR))
  WHERE a.aerolinea IS NULL
)
SELECT * EXCLUDE (candidatos) FROM k WHERE candidatos = 1 AND aerolinea IS NOT NULL;

-- 3. Aeronave del portal municipal (vuelos 2015–2019) para el foco: mismo día y hora local,
--    movimiento, origen/destino y aerolínea; un solo candidato de cada lado (1 a 1).
CREATE OR REPLACE TABLE ref_aeronave_municipal AS
WITH a AS (
  SELECT s.fecha, s.hora_utc, s.aeropuerto, s.tipo_movimiento, s.origen_destino, s.aerolinea,
         CAST(s.fecha + s.hora_utc + to_hours(getvariable('utc_offset')) AS DATE) AS fecha_l,
         hour(s.fecha + s.hora_utc + to_hours(getvariable('utc_offset'))) AS hora_l,
         al.aerolinea_nombre AS nombre
  FROM stg_movimiento s LEFT JOIN dim_aerolinea al ON al.aerolinea = s.aerolinea
  WHERE s.aeropuerto = getvariable('foco') AND s.aeronave IS NULL AND s.hora_utc IS NOT NULL
),
m AS (
  SELECT h.fecha, h.hora_local, h.tipo_movimiento, h.aeronave,
         coalesce(ap.codigo, h.origen_destino_oaci) AS od,
         coalesce(al.aerolinea_nombre, h.aerolinea) AS nombre,
         row_number() OVER () AS id_mun
  FROM mun_vuelos_hist h
  LEFT JOIN dim_aerolinea al ON al.aerolinea = h.aerolinea
  LEFT JOIN (SELECT oaci, any_value(codigo ORDER BY length(codigo)) AS codigo
             FROM dim_aeropuerto WHERE oaci IS NOT NULL GROUP BY oaci) ap
    ON ap.oaci = h.origen_destino_oaci
  WHERE h.aeronave IS NOT NULL
),
k AS (
  SELECT a.*, m.aeronave AS aeronave_mun, m.id_mun,
         count(*) OVER (PARTITION BY a.fecha, a.hora_utc, a.aeropuerto, a.tipo_movimiento,
                                     a.origen_destino, a.aerolinea) AS c_anac,
         count(*) OVER (PARTITION BY m.id_mun) AS c_mun
  FROM a JOIN m
    ON m.fecha = a.fecha_l AND m.hora_local = a.hora_l AND m.tipo_movimiento = a.tipo_movimiento
   AND m.od = a.origen_destino AND m.nombre = a.nombre
)
SELECT fecha, hora_utc, aeropuerto, tipo_movimiento, origen_destino, aerolinea,
       aeronave_mun AS aeronave
FROM k WHERE c_anac = 1 AND c_mun = 1;
