-- EVyTH (Encuesta de Viajes y Turismo de los Hogares, Yvera): viajes de residentes en los
-- aglomerados urbanos relevados con destino Mar del Plata. Una fila por visitante y viaje;
-- pondera = factor de expansión (suma = visitantes estimados). Códigos -> texto con el diccionario.
CREATE OR REPLACE MACRO evyth_txt(var, cod) AS
  (SELECT any_value(descripcion) FROM stg_evyth_dicc d
   WHERE d.variable = var AND d.opcion = trim(cod));

CREATE OR REPLACE TABLE fct_evyth_mdq AS
SELECT
  anio, trimestre,
  CASE trim(tipo_visitante) WHEN '1' THEN 'turista' WHEN '2' THEN 'excursionista' END AS tipo_visitante,
  coalesce(evyth_txt('region_origen', region_origen), 'Sin dato')                  AS region_origen,
  -- Medio de transporte agrupado (px09): las categorías chicas van a "Otros".
  CASE trim(px09) WHEN '1' THEN 'Auto' WHEN '2' THEN 'Ómnibus' WHEN '3' THEN 'Tren'
                  WHEN '4' THEN 'Avión' ELSE 'Otros' END                            AS medio,
  coalesce(evyth_txt('px09', px09), 'Sin dato')                                    AS medio_detalle,
  coalesce(evyth_txt('px10_1', px10_1), 'Sin dato')                                AS motivo,
  coalesce(evyth_txt('px08_agrup', px08_agrup), 'Sin dato')                        AS alojamiento,
  TRY_CAST(px07 AS INT)                                                            AS noches,
  pondera
FROM stg_evyth
WHERE pondera IS NOT NULL;
