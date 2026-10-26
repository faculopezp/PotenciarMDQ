-- Micros de media y larga distancia: CNRT vía Yvera ("Conectividad terrestre interurbana").
-- Dos servicios:
--   regular  líneas con horario y boleto (servicio público de jurisdicción nacional).
--   turismo  servicios de turismo nacional (DUT): viajes contratados, excursiones, chárter.
-- Solo pares con Mar del Plata en un extremo. El archivo anual por ruta trae solo las rutas con al
-- menos un viaje semanal (un piso, no el total); la base DUT trae cada servicio con su fecha.

-- Mismo nombre escrito distinto según el archivo (con o sin tildes, abreviado o mal tipeado).
CREATE OR REPLACE MACRO bus_clave(x) AS
  CASE lower(strip_accents(trim(x)))
    WHEN 'caba' THEN 'ciudad autonoma de buenos aires'
    WHEN 'ciudad autonoma' THEN 'ciudad autonoma de buenos aires'
    WHEN 'cuidad autonoma' THEN 'ciudad autonoma de buenos aires'
    WHEN 'capital federal' THEN 'ciudad autonoma de buenos aires'
    ELSE lower(strip_accents(trim(x)))
  END;

CREATE OR REPLACE TABLE fct_bus_ruta_anual AS
WITH crudo AS (
  SELECT 'regular' AS servicio, TRY_CAST(indice_tiempo AS INT) AS anio,
         par_origen_destino AS par, viajes, asientos, pasajeros
  FROM stg_bus_magnitudes_por_ruta
  UNION ALL
  SELECT 'turismo', TRY_CAST(indice_tiempo AS INT), par_origen_destino, viajes, asientos, pasajeros
  FROM stg_bus_magnitudes_por_ruta_dut
),
partido AS (
  -- El otro extremo se saca quitando "Mar del Plata" del par: tolera guiones dentro del nombre.
  SELECT *,
    CASE WHEN regexp_matches(par, '^\s*mar del plata\s*-', 'i') THEN 'salida'
         WHEN regexp_matches(par, '-\s*mar del plata\s*$', 'i') THEN 'llegada' END AS sentido,
    trim(regexp_replace(regexp_replace(par, '^\s*mar del plata\s*-\s*', '', 'i'),
                        '\s*-\s*mar del plata\s*$', '', 'i')) AS extremo_crudo
  FROM crudo
)
SELECT servicio, anio, sentido, bus_clave(extremo_crudo) AS extremo_clave, extremo_crudo, par,
       TRY_CAST(viajes AS INT) AS viajes, TRY_CAST(asientos AS INT) AS asientos,
       TRY_CAST(pasajeros AS INT) AS pasajeros
FROM partido
WHERE sentido IS NOT NULL AND bus_clave(extremo_crudo) <> 'mar del plata';

-- Cada servicio de turismo (DUT) con Mar del Plata en un extremo.
CREATE OR REPLACE TABLE fct_bus_turismo AS
SELECT
  CAST(indice_tiempo AS DATE)                                   AS fecha,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN 'llegada' ELSE 'salida' END
                                                                AS sentido,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN localidad_origen
       ELSE localidad_destino END                               AS extremo_crudo,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN provincia_origen
       ELSE provincia_destino END                               AS extremo_provincia,
  ruta_clasificacion, clase_modalidad,
  TRY_CAST(asientos AS INT)                                     AS asientos,
  TRY_CAST(pasajeros AS INT)                                    AS pasajeros
FROM stg_bus_base_microdatos_dut
WHERE (bus_clave(localidad_destino) = 'mar del plata') <> (bus_clave(localidad_origen) = 'mar del plata');

-- Totales nacionales por día (todas las rutas): denominador de la participación de Mar del Plata.
CREATE OR REPLACE TABLE fct_bus_nacional_diario AS
SELECT 'regular' AS servicio, CAST(indice_tiempo AS DATE) AS fecha,
       TRY_CAST(viajes AS INT) AS viajes, TRY_CAST(asientos AS INT) AS asientos,
       TRY_CAST(pasajeros AS INT) AS pasajeros
FROM stg_bus_viajes_asientos_pasajeros
UNION ALL
SELECT 'turismo', CAST(indice_tiempo AS DATE), TRY_CAST(viajes AS INT),
       TRY_CAST(asientos AS INT), TRY_CAST(pasajeros AS INT)
FROM stg_bus_viajes_asientos_pasajeros_dut;

-- Nombre de cada localidad para mostrar (preferir la versión con tildes) y su provincia (solo la
-- trae la base DUT).
CREATE OR REPLACE TABLE dim_bus_localidad AS
WITH nombres AS (
  SELECT extremo_crudo AS nombre, NULL AS provincia FROM fct_bus_ruta_anual
  UNION ALL
  SELECT extremo_crudo, extremo_provincia FROM fct_bus_turismo
)
SELECT bus_clave(nombre)                                                     AS clave,
       replace(replace(max_by(nombre, (nombre <> strip_accents(nombre))::INT), ' De ', ' de '),
               ' Del ', ' del ')                                             AS nombre,
       replace(mode(provincia) FILTER (WHERE provincia IS NOT NULL), ' De ', ' de ') AS provincia
FROM nombres
GROUP BY 1;
