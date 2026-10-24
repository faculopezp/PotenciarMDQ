-- Capacidad estimada (asientos) por aeronave: percentil 95 de pasajeros observados en vuelos
-- comerciales. Es un proxy basado en datos (ANAC no publica asientos). Con datos reales da 96 para
-- el E190 de Aerolíneas y 189 para el 737-8Q8 de Flybondi; en tipos con pocos vuelos llenos queda
-- corto y el load factor sale inflado. Calibrar con los asientos de Yvera cuando estén.
CREATE OR REPLACE TABLE dim_capacidad AS
WITH c AS (
  SELECT aerolinea, aeronave, pasajeros FROM stg_movimiento
  WHERE list_contains(getvariable('comerciales'), clase_vuelo)
    AND aeronave IS NOT NULL AND pasajeros > 0
)
SELECT 'aerolinea_aeronave' AS metodo, aerolinea, aeronave, count(*) AS n_vuelos,
       round(quantile_cont(pasajeros, 0.95)) AS capacidad
FROM c WHERE aerolinea IS NOT NULL GROUP BY aerolinea, aeronave HAVING count(*) >= 30
UNION ALL
SELECT 'aeronave', NULL, aeronave, count(*), round(quantile_cont(pasajeros, 0.95))
FROM c GROUP BY aeronave HAVING count(*) >= 30;
