-- Aeropuertos: OurAirports indexado por el código que usa ANAC.
-- ANAC usa el código local (FAA Argentina, ej. MDP, AER) para aeropuertos nacionales y OACI para
-- extranjeros. OurAirports guarda ese código local en `local_code` (verificado para MDP/AER/BCA...).
CREATE OR REPLACE TABLE dim_aeropuerto AS
WITH k AS (
  SELECT local_code AS codigo, 1 AS prioridad, * FROM ourairports
  WHERE iso_country = 'AR' AND local_code IS NOT NULL
  UNION ALL BY NAME
  SELECT ident AS codigo, 2 AS prioridad, * FROM ourairports
),
u AS (
  SELECT * FROM k
  QUALIFY row_number() OVER (
    PARTITION BY codigo
    ORDER BY prioridad,
             CASE type WHEN 'large_airport' THEN 1 WHEN 'medium_airport' THEN 2 ELSE 3 END
  ) = 1
),
foco AS (SELECT latitude_deg AS lat, longitude_deg AS lon FROM u WHERE codigo = getvariable('foco'))
SELECT
  u.codigo,
  u.ident                   AS oaci,
  u.iata_code               AS iata,
  u.name                    AS nombre,
  u.municipality            AS ciudad,
  u.iso_country             AS pais,
  u.iso_region              AS region,
  u.latitude_deg            AS lat,
  u.longitude_deg           AS lon,
  u.type                    AS tipo,
  u.codigo = getvariable('foco')                    AS es_foco,
  list_contains(getvariable('pares'), u.codigo)     AS es_par,
  round(haversine_km(foco.lat, foco.lon, u.latitude_deg, u.longitude_deg)) AS distancia_mdq_km
FROM u, foco;
