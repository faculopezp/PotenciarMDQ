-- Participación por aerolínea (nombre normalizado) y año, aviación de línea (regular + charter).
WITH a AS (
  SELECT
    anio, aerolinea_nombre, aerolinea_tipo,
    count(*)                    AS movimientos,
    coalesce(sum(pasajeros), 0) AS pasajeros,
    round(sum(pasajeros) FILTER (asientos_estimados IS NOT NULL)
          / nullif(sum(asientos_estimados) FILTER (pasajeros IS NOT NULL), 0), 3) AS lf_estimado
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco') AND es_linea
  GROUP BY anio, aerolinea_nombre, aerolinea_tipo
)
SELECT *, round(pasajeros / nullif(sum(pasajeros) OVER (PARTITION BY anio), 0), 4) AS share_pasajeros
FROM a
ORDER BY anio, pasajeros DESC
