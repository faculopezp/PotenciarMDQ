-- Aeropuertos indexados por el código que usa ANAC en el CSV de movimientos.
-- ANAC usa el código local (MDP, AER, y numéricos para aeródromos/helipuertos sin designador)
-- para Argentina y el OACI para el exterior. Orden de resolución (gana la primera que matchea):
--   1. OurAirports, Argentina, local_code   (nombres y ciudades más prolijos)
--   2. Lista oficial ANAC de aeródromos     (cubre helipuertos, pistas chicas y códigos numéricos)
--   3. OurAirports, Antártida, local_code   (bases argentinas: MBI Marambio, etc.)
--   4. OurAirports ident / gps_code de 4 letras (exterior; gps_code resuelve OACI nuevos, ej. SPJC
--      Lima, cuyo ident en OurAirports sigue siendo SPIM)
-- Validación cruzada ANAC vs OurAirports: reports/qa (distancia entre ambas coordenadas).
CREATE OR REPLACE TABLE dim_aeropuerto AS
WITH oa AS (
  SELECT ident, iata_code, name, municipality, iso_country, iso_region,
         latitude_deg, longitude_deg, type, local_code, gps_code,
         CASE type WHEN 'large_airport' THEN 1 WHEN 'medium_airport' THEN 2 ELSE 3 END AS rango
  FROM ourairports
),
k AS (
  SELECT local_code AS codigo, 1 AS prioridad, 'ourairports_local' AS fuente_coord, * FROM oa
  WHERE iso_country = 'AR' AND local_code IS NOT NULL
  UNION ALL BY NAME
  SELECT codigo, 2 AS prioridad, 'anac' AS fuente_coord,
         oaci AS ident, iata AS iata_code, nombre AS name,
         NULL AS municipality, CASE WHEN lat < -60 THEN 'AQ' ELSE 'AR' END AS iso_country,
         provincia AS iso_region, lat AS latitude_deg, lon AS longitude_deg, tipo AS type,
         codigo AS local_code, oaci AS gps_code, 3 AS rango
  FROM anac_aeropuertos WHERE lat IS NOT NULL
  UNION ALL BY NAME
  SELECT local_code AS codigo, 3 AS prioridad, 'ourairports_local' AS fuente_coord, * FROM oa
  WHERE iso_country = 'AQ' AND local_code IS NOT NULL
  UNION ALL BY NAME
  SELECT ident AS codigo, 4 AS prioridad, 'ourairports_oaci' AS fuente_coord, * FROM oa
  WHERE regexp_matches(ident, '^[A-Z]{4}$')
  UNION ALL BY NAME
  SELECT gps_code AS codigo, 5 AS prioridad, 'ourairports_oaci' AS fuente_coord, * FROM oa
  WHERE regexp_matches(gps_code, '^[A-Z]{4}$') AND gps_code <> ident
  UNION ALL BY NAME
  -- Códigos numéricos = Lugares Aptos Denunciados (LAD, art. 25 Código Aeronáutico): superficies
  -- aptas registradas por denuncia, no aeródromos. Sin coordenadas públicas (no están en la lista
  -- de aeródromos ni en MADHEL). ANAC los marca como "internacional", pero están en Argentina.
  SELECT DISTINCT origen_destino AS codigo, 6 AS prioridad, 'lad_sin_coordenadas' AS fuente_coord,
         NULL AS ident, NULL AS iata_code, 'Lugar apto denunciado ' || origen_destino AS name,
         NULL AS municipality, 'AR' AS iso_country, NULL AS iso_region,
         NULL::DOUBLE AS latitude_deg, NULL::DOUBLE AS longitude_deg,
         'lugar_apto_denunciado' AS type, NULL AS local_code, NULL AS gps_code, 9 AS rango
  FROM stg_movimiento WHERE regexp_matches(origen_destino, '^[0-9]+$')
),
u AS (
  SELECT * FROM k
  QUALIFY row_number() OVER (PARTITION BY codigo ORDER BY prioridad, rango) = 1
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
  u.fuente_coord,
  u.codigo = getvariable('foco')                    AS es_foco,
  list_contains(getvariable('pares'), u.codigo)     AS es_par,
  round(haversine_km(foco.lat, foco.lon, u.latitude_deg, u.longitude_deg)) AS distancia_mdq_km
FROM u, foco;

-- Validación cruzada: mismo código en la lista ANAC y en OurAirports (Argentina) -> distancia.
CREATE OR REPLACE TABLE ref_aeropuerto_cruce AS
SELECT a.codigo, a.nombre AS nombre_anac, o.name AS nombre_ourairports,
       a.lat AS lat_anac, a.lon AS lon_anac, o.latitude_deg AS lat_oa, o.longitude_deg AS lon_oa,
       round(haversine_km(a.lat, a.lon, o.latitude_deg, o.longitude_deg), 1) AS distancia_km
FROM anac_aeropuertos a
JOIN ourairports o ON o.local_code = a.codigo AND o.iso_country IN ('AR', 'AQ')
WHERE a.lat IS NOT NULL;
