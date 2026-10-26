-- Micros de media y larga distancia: CNRT vía Yvera ("Conectividad terrestre interurbana").
-- Dos servicios:
--   regular  líneas con horario y boleto (servicio público de jurisdicción nacional).
--   turismo  servicios de turismo nacional (DUT): viajes contratados, excursiones, chárter.
-- Solo pares con Mar del Plata en un extremo. Dos tipos de archivo:
--   bases por viaje (una fila por servicio, con fecha): la fuente principal donde cubren el año.
--   anual por ruta (solo rutas con al menos un viaje semanal): completa los años sin base.

-- Mismo nombre escrito distinto según el archivo (con o sin tildes, abreviado o mal tipeado).
CREATE OR REPLACE MACRO bus_clave(x) AS
  CASE lower(strip_accents(trim(x)))
    WHEN 'caba' THEN 'ciudad autonoma de buenos aires'
    WHEN 'ciudad autonoma' THEN 'ciudad autonoma de buenos aires'
    WHEN 'cuidad autonoma' THEN 'ciudad autonoma de buenos aires'
    WHEN 'capital federal' THEN 'ciudad autonoma de buenos aires'
    ELSE lower(strip_accents(trim(x)))
  END;

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

-- Cada viaje con Mar del Plata en un extremo (regular y turismo).
CREATE OR REPLACE TABLE fct_bus_viaje AS
WITH crudo AS (
  SELECT 'regular' AS servicio, indice_tiempo, localidad_origen, provincia_origen,
         localidad_destino, provincia_destino, ruta_clasificacion, descripcion AS modalidad,
         asientos, pasajeros
  FROM stg_bus_base_microdatos
  UNION ALL
  SELECT 'turismo', indice_tiempo, localidad_origen, provincia_origen, localidad_destino,
         provincia_destino, ruta_clasificacion, clase_modalidad, asientos, pasajeros
  FROM stg_bus_base_microdatos_dut
)
SELECT
  servicio,
  CAST(indice_tiempo AS DATE)                                       AS fecha,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN 'llegada' ELSE 'salida' END
                                                                    AS sentido,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN localidad_origen
       ELSE localidad_destino END                                   AS extremo_crudo,
  CASE WHEN bus_clave(localidad_destino) = 'mar del plata' THEN provincia_origen
       ELSE provincia_destino END                                   AS extremo_provincia,
  ruta_clasificacion, modalidad,
  TRY_CAST(asientos AS INT)                                         AS asientos,
  TRY_CAST(pasajeros AS INT)                                        AS pasajeros
FROM crudo
WHERE (bus_clave(localidad_destino) = 'mar del plata') <> (bus_clave(localidad_origen) = 'mar del plata');

-- Archivo anual por ruta, tal como se publica (validación y años sin base por viaje).
CREATE OR REPLACE TABLE fct_bus_ruta_anual_publicada AS
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

-- Por ruta y año: la base por viaje donde cubre los mismos meses que el total país de ese
-- servicio y año; si no, el archivo anual.
CREATE OR REPLACE TABLE fct_bus_ruta_anual AS
WITH meses_pais AS (
  SELECT servicio, year(fecha) AS anio, count(DISTINCT month(fecha)) AS meses
  FROM fct_bus_nacional_diario GROUP BY ALL
),
meses_base AS (
  SELECT servicio, year(fecha) AS anio, count(DISTINCT month(fecha)) AS meses
  FROM fct_bus_viaje GROUP BY ALL
),
con_base AS (
  SELECT b.servicio, b.anio
  FROM meses_base b LEFT JOIN meses_pais m USING (servicio, anio)
  WHERE b.meses >= coalesce(m.meses, 12)
),
base AS (
  SELECT servicio, year(fecha) AS anio, sentido, bus_clave(extremo_crudo) AS extremo_clave,
         any_value(extremo_crudo) AS extremo_crudo, count(*) AS viajes,
         sum(asientos) AS asientos, sum(pasajeros) AS pasajeros
  FROM fct_bus_viaje SEMI JOIN con_base ON con_base.servicio = fct_bus_viaje.servicio
                                       AND con_base.anio = year(fct_bus_viaje.fecha)
  GROUP BY ALL
)
SELECT servicio, anio, sentido, extremo_clave, extremo_crudo, viajes, asientos, pasajeros,
       'base_por_viaje' AS fuente
FROM base
UNION ALL
SELECT p.servicio, p.anio, p.sentido, p.extremo_clave, p.extremo_crudo, p.viajes, p.asientos,
       p.pasajeros, 'anual_por_ruta'
FROM fct_bus_ruta_anual_publicada p
ANTI JOIN con_base c USING (servicio, anio);

-- Nombre de cada localidad para mostrar (preferir la versión con tildes) y su provincia (la
-- traen las bases por viaje).
CREATE OR REPLACE TABLE dim_bus_localidad AS
WITH nombres AS (
  SELECT extremo_crudo AS nombre, NULL AS provincia FROM fct_bus_ruta_anual_publicada
  UNION ALL
  SELECT extremo_crudo, extremo_provincia FROM fct_bus_viaje
)
SELECT bus_clave(nombre)                                                     AS clave,
       replace(replace(max_by(nombre, (nombre <> strip_accents(nombre))::INT), ' De ', ' de '),
               ' Del ', ' del ')                                             AS nombre,
       replace(max_by(provincia, (provincia <> strip_accents(provincia))::INT)
               FILTER (WHERE provincia IS NOT NULL), ' De ', ' de ')         AS provincia
FROM nombres
GROUP BY 1;
