-- Tren: pasajeros pagos de los servicios de larga distancia, regionales y turísticos (CNRT), por
-- mes y servicio, de todo el país. es_foco = el servicio llega a Mar del Plata (Constitución–Mar
-- del Plata, con o sin extensión a Miramar). Los pasajeros son del servicio entero: incluyen a
-- quienes viajan entre estaciones intermedias, en los dos sentidos.
CREATE OR REPLACE TABLE fct_tren_mensual AS
SELECT anio, mes, make_date(anio, mes, 1) AS periodo, linea, operador, tipo_servicio,
       jurisdiccion, servicio, pax,
       servicio ILIKE '%mar del plata%' AS es_foco,
       -- La planilla escribe SOFSE y, desde 2025, también SOFSA: es el mismo operador.
       CASE WHEN operador ILIKE 'SOFS%' THEN 'Trenes Argentinos (SOFSE)'
            WHEN operador ILIKE 'FERROBAIRES' THEN 'Ferrobaires (provincia)'
            ELSE operador END AS operador_nombre,
       archivo
FROM stg_tren
WHERE pax IS NOT NULL;
