-- Tramos (vuelos origen -> destino) reconstruidos uniendo el despegue en A con el aterrizaje
-- en B. ANAC no publica ID de vuelo: se empareja por aerolínea + aeronave (+ matrícula si existe,
-- desde 2026) tomando el primer aterrizaje posterior (ASOF JOIN). Solo cabotaje (los
-- internacionales tienen un solo extremo en el dataset).
CREATE OR REPLACE TABLE fct_tramo AS
WITH m AS (
  SELECT movimiento_id, ts_utc, ts_local, aeropuerto, origen_destino, tipo_movimiento,
         coalesce(aerolinea, '?') AS k_aerolinea, coalesce(aeronave, '?') AS k_aeronave,
         coalesce(matricula, '') AS k_matricula,
         aerolinea_nombre, aeronave, aeronave_familia, matricula, pasajeros, distancia_km
  FROM fct_movimiento
  WHERE es_comercial AND clasificacion_vuelo = 'cabotaje'
    AND ts_utc IS NOT NULL AND origen_destino IS NOT NULL
    AND aeropuerto <> origen_destino
),
dep AS (SELECT *, aeropuerto AS origen, origen_destino AS destino FROM m WHERE tipo_movimiento = 'despegue'),
arr AS (SELECT *, origen_destino AS origen, aeropuerto AS destino FROM m WHERE tipo_movimiento = 'aterrizaje'),
par AS (
  SELECT
    d.movimiento_id AS mov_despegue_id, a.movimiento_id AS mov_aterrizaje_id,
    d.origen, d.destino, d.ts_utc AS salida_utc, a.ts_utc AS llegada_utc, d.ts_local AS salida_local,
    datediff('minute', d.ts_utc, a.ts_utc) AS duracion_min,
    d.aerolinea_nombre, d.aeronave, d.aeronave_familia, d.matricula,
    d.pasajeros AS pax_despegue, a.pasajeros AS pax_aterrizaje, d.distancia_km,
    CASE WHEN d.k_matricula <> '' THEN 'matricula' ELSE 'modelo' END AS metodo_emparejamiento
  FROM dep d
  ASOF JOIN arr a
    ON a.origen = d.origen AND a.destino = d.destino
   AND a.k_aerolinea = d.k_aerolinea AND a.k_aeronave = d.k_aeronave
   AND a.k_matricula = d.k_matricula
   AND a.ts_utc > d.ts_utc
)
SELECT
  row_number() OVER (ORDER BY salida_utc, origen) AS tramo_id,
  *,
  CAST(salida_local AS DATE)                       AS fecha,
  year(salida_local)                               AS anio,
  month(salida_local)                              AS mes,
  round(distancia_km / nullif(duracion_min / 60.0, 0)) AS velocidad_bloque_kmh,
  pax_despegue - pax_aterrizaje                    AS pax_diferencia
FROM par
WHERE duracion_min BETWEEN 15 AND 600
QUALIFY row_number() OVER (PARTITION BY mov_aterrizaje_id ORDER BY duracion_min) = 1;
