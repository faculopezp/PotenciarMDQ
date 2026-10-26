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

-- 4. Aeronaves del Estado (config/estatales.yaml): operador por prefijo de la identificación
--    (formato de cada fuerza) y modelo por serie con identificación pública. La identificación se
--    compara sin guiones (T-94 = T94). Solo completa lo que ANAC deja vacío.
CREATE OR REPLACE TABLE ref_operador_estatal AS
WITH m AS (
  SELECT DISTINCT matricula, upper(regexp_replace(matricula, '[- ]', '', 'g')) AS ident
  FROM stg_movimiento
  WHERE matricula IS NOT NULL AND clase_vuelo <> 'vuelo_oficial_extranjero'
)
SELECT m.matricula, p.operador AS aerolinea, p.orden
FROM m JOIN ref_prefijo_estatal p ON regexp_matches(m.ident, p.patron)
QUALIFY row_number() OVER (PARTITION BY m.matricula ORDER BY p.orden) = 1;

CREATE OR REPLACE TABLE ref_aeronave_serie AS
SELECT DISTINCT s.matricula, r.aeronave, r.desde
FROM stg_movimiento s
JOIN ref_serie_estatal r ON upper(regexp_replace(s.matricula, '[- ]', '', 'g')) = r.matricula
WHERE s.matricula IS NOT NULL;

-- 5. El otro extremo del mismo vuelo SIN matrícula (2019–2025): el registro del aeropuerto de
--    origen/destino con aeropuertos cruzados, movimiento opuesto, entre 10 minutos y 10 horas, y
--    avión, operador y matrícula compatibles (iguales o uno de los dos vacío). Vale solo si hay un
--    único candidato de cada lado y el registro no está repetido. Validado contra los vuelos que
--    traen el dato en ambos extremos (reports/qa/auditoria.md, sección 2E).
CREATE OR REPLACE TABLE ref_vuelo_par AS
WITH m AS (
  SELECT s.fecha, s.hora_utc, s.aeropuerto, s.tipo_movimiento, s.origen_destino, s.aerolinea,
         s.aeronave, s.matricula, coalesce(al.aerolinea_clave, s.aerolinea) AS clave,
         CAST(s.fecha + s.hora_utc AS TIMESTAMP) AS ts,
         count(*) OVER (PARTITION BY s.fecha, s.hora_utc, s.aeropuerto, s.tipo_movimiento,
                        s.origen_destino, s.aerolinea, s.aeronave, s.matricula) AS repetidos
  FROM stg_movimiento s LEFT JOIN dim_aerolinea al ON al.aerolinea = s.aerolinea
  WHERE s.hora_utc IS NOT NULL AND s.origen_destino IS NOT NULL
    AND s.aeropuerto <> s.origen_destino
),
d AS (SELECT unnest([-1, 0, 1]) AS o),
-- x: registros a completar; y: candidatos en el otro aeropuerto.
k AS (
  SELECT x.fecha, x.hora_utc, x.aeropuerto, x.tipo_movimiento, x.origen_destino, x.aerolinea,
         x.aeronave, x.matricula, y.aerolinea AS aerolinea_par, y.aeronave AS aeronave_par,
         y.fecha AS y_fecha, y.hora_utc AS y_hora, y.aeropuerto AS y_ap, y.tipo_movimiento AS y_tm,
         y.origen_destino AS y_od, y.ts AS y_ts, y.clave AS y_clave, y.matricula AS y_mat,
         count(*) OVER (PARTITION BY x.fecha, x.hora_utc, x.aeropuerto, x.tipo_movimiento,
                        x.origen_destino, x.aerolinea, x.aeronave, x.matricula) AS candidatos
  FROM m x CROSS JOIN d
  JOIN m y ON y.fecha = x.fecha + d.o AND y.aeropuerto = x.origen_destino
          AND y.origen_destino = x.aeropuerto AND y.tipo_movimiento <> x.tipo_movimiento
  WHERE x.repetidos = 1 AND (x.aerolinea IS NULL OR x.aeronave IS NULL)
    AND (x.aeronave IS NULL OR y.aeronave IS NULL OR x.aeronave = y.aeronave)
    AND (x.aerolinea IS NULL OR y.aerolinea IS NULL OR x.clave = y.clave)
    AND (x.matricula IS NULL OR y.matricula IS NULL OR x.matricula = y.matricula)
    AND ((x.tipo_movimiento = 'aterrizaje' AND y.ts BETWEEN x.ts - INTERVAL 10 HOUR AND x.ts - INTERVAL 10 MINUTE)
      OR (x.tipo_movimiento = 'despegue' AND y.ts BETWEEN x.ts + INTERVAL 10 MINUTE AND x.ts + INTERVAL 10 HOUR))
),
u AS (SELECT * FROM k WHERE candidatos = 1),
-- El candidato tampoco puede tener otro registro compatible del lado de x.
v AS (
  SELECT u.*, count(*) OVER (PARTITION BY u.y_fecha, u.y_hora, u.y_ap, u.y_tm, u.y_od,
                             u.aerolinea_par, u.aeronave_par, u.y_mat) AS inversos
  FROM u CROSS JOIN d
  JOIN m z ON z.fecha = u.y_fecha + d.o AND z.aeropuerto = u.y_od AND z.origen_destino = u.y_ap
          AND z.tipo_movimiento <> u.y_tm
  WHERE (z.aeronave IS NULL OR u.aeronave_par IS NULL OR z.aeronave = u.aeronave_par)
    AND (z.aerolinea IS NULL OR u.aerolinea_par IS NULL OR z.clave = u.y_clave)
    AND (z.matricula IS NULL OR u.y_mat IS NULL OR z.matricula = u.y_mat)
    AND ((u.y_tm = 'aterrizaje' AND z.ts BETWEEN u.y_ts - INTERVAL 10 HOUR AND u.y_ts - INTERVAL 10 MINUTE)
      OR (u.y_tm = 'despegue' AND z.ts BETWEEN u.y_ts + INTERVAL 10 MINUTE AND u.y_ts + INTERVAL 10 HOUR))
)
SELECT DISTINCT fecha, hora_utc, aeropuerto, tipo_movimiento, origen_destino, aerolinea, aeronave,
       matricula,
       CASE WHEN aerolinea IS NULL THEN aerolinea_par END AS aerolinea_par,
       CASE WHEN aeronave IS NULL THEN aeronave_par END AS aeronave_par
FROM v
WHERE inversos = 1
  AND ((aerolinea IS NULL AND aerolinea_par IS NOT NULL) OR (aeronave IS NULL AND aeronave_par IS NOT NULL));

-- 6. Quién hace taxi aéreo: operadores y matrículas con algún vuelo no regular declarado. Lo usa el
--    segmento (sql/bd/30): un "privado" en jet o turbohélice ejecutivo se analiza como taxi aéreo
--    salvo que el operador o la matrícula se conozcan y nunca vuelen como no regular.
CREATE OR REPLACE TABLE ref_taxi_operador AS
SELECT DISTINCT aerolinea FROM stg_movimiento WHERE clase_vuelo = 'no_regular' AND aerolinea IS NOT NULL;

CREATE OR REPLACE TABLE ref_taxi_matricula AS
SELECT DISTINCT matricula FROM stg_movimiento WHERE clase_vuelo = 'no_regular' AND matricula IS NOT NULL;
