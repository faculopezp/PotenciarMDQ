-- Rotaciones (turnaround) en el aeropuerto foco y pares: aterrizaje -> siguiente despegue del
-- mismo avión. Con matrícula (2026+) es exacto; antes se aproxima con aerolínea + modelo
-- (FIFO), que en aeropuertos chicos funciona razonablemente (QA compara ambos métodos en 2026).
CREATE OR REPLACE TABLE fct_rotacion AS
WITH m AS (
  SELECT movimiento_id, ts_utc, ts_local, aeropuerto, origen_destino, tipo_movimiento,
         coalesce(aerolinea, '?') AS k_aerolinea, coalesce(aeronave, '?') AS k_aeronave,
         coalesce(matricula, '') AS k_matricula,
         aerolinea_nombre, aeronave, aeronave_familia, aeronave_categoria, matricula, pasajeros
  FROM fct_movimiento
  WHERE es_comercial AND ts_utc IS NOT NULL AND aeronave IS NOT NULL
    AND (aeropuerto = getvariable('foco') OR list_contains(getvariable('pares'), aeropuerto))
),
arr AS (SELECT * FROM m WHERE tipo_movimiento = 'aterrizaje'),
dep AS (SELECT * FROM m WHERE tipo_movimiento = 'despegue'),
par AS (
  SELECT
    a.aeropuerto,
    a.movimiento_id AS mov_aterrizaje_id, d.movimiento_id AS mov_despegue_id,
    a.ts_local AS llegada_local, d.ts_local AS salida_local,
    datediff('minute', a.ts_utc, d.ts_utc) AS tiempo_en_tierra_min,
    a.origen_destino AS viene_de, d.origen_destino AS va_a,
    a.aerolinea_nombre, a.aeronave, a.aeronave_familia, a.aeronave_categoria, a.matricula,
    a.pasajeros AS pax_llegada, d.pasajeros AS pax_salida,
    CASE WHEN a.k_matricula <> '' THEN 'matricula' ELSE 'modelo' END AS metodo_emparejamiento
  FROM arr a
  ASOF JOIN dep d
    ON d.aeropuerto = a.aeropuerto
   AND d.k_aerolinea = a.k_aerolinea AND d.k_aeronave = a.k_aeronave
   AND d.k_matricula = a.k_matricula
   AND d.ts_utc > a.ts_utc
)
SELECT
  *,
  CAST(llegada_local AS DATE) AS fecha,
  year(llegada_local)         AS anio,
  month(llegada_local)        AS mes,
  CASE
    WHEN tiempo_en_tierra_min <= 120 THEN 'rotacion'
    WHEN CAST(salida_local AS DATE) > CAST(llegada_local AS DATE)
         AND tiempo_en_tierra_min > 240 THEN 'pernocte'
    ELSE 'escala_larga'
  END AS tipo_rotacion
FROM par
WHERE tiempo_en_tierra_min BETWEEN 15 AND 36 * 60
QUALIFY row_number() OVER (PARTITION BY mov_despegue_id ORDER BY tiempo_en_tierra_min) = 1;
