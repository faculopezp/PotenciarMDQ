-- Con qué tipo de aeronave vuela cada segmento en MDQ, por año. El pistón se separa por plazas
-- con el mismo umbral que el taxi aéreo (config/mdq.yaml → perfil_aeronave.taxi_min_plazas).
WITH m AS (
  SELECT
    anio, segmento, pasajeros,
    CASE
      WHEN aeronave_categoria = 'jet_ejecutivo' THEN 'jet_ejecutivo'
      WHEN aeronave_categoria = 'turbohelice_ejecutivo' THEN 'turbohelice'
      WHEN aeronave_categoria = 'aviacion_general_piston'
        OR list_contains(getvariable('taxi_modelos_piston'), aeronave_modelo)
        THEN CASE WHEN coalesce(aeronave_plazas, 0) >= getvariable('taxi_min_plazas')
                  THEN 'piston_6' ELSE 'piston_liviano' END
      WHEN aeronave_categoria = 'helicoptero' THEN 'helicoptero'
      WHEN list_contains(getvariable('categorias_linea'), aeronave_categoria) THEN 'avion_de_linea'
      ELSE 'sin_dato'
    END AS perfil
  FROM fct_movimiento
  WHERE aeropuerto = getvariable('foco')
),
a AS (
  SELECT anio, segmento, perfil, count(*) AS movimientos,
         coalesce(sum(pasajeros), 0) AS pasajeros, round(avg(pasajeros), 2) AS pax_promedio
  FROM m GROUP BY anio, segmento, perfil
)
SELECT *, round(movimientos / sum(movimientos) OVER (PARTITION BY anio, segmento), 4)
            AS share_en_segmento
FROM a
ORDER BY anio, segmento, movimientos DESC
