-- Con qué tipo de aeronave vuela cada segmento en MDQ, por año (perfil: dim_perfil_familia).
WITH a AS (
  SELECT
    m.anio, m.segmento, coalesce(p.perfil, 'sin_dato') AS perfil,
    count(*)                                      AS movimientos,
    coalesce(sum(m.pasajeros), 0)                 AS pasajeros,
    round(avg(m.pasajeros), 2)                    AS pax_promedio
  FROM fct_movimiento m
  LEFT JOIN dim_perfil_familia p USING (aeronave_familia)
  WHERE m.aeropuerto = getvariable('foco')
  GROUP BY m.anio, m.segmento, coalesce(p.perfil, 'sin_dato')
)
SELECT *, round(movimientos / sum(movimientos) OVER (PARTITION BY anio, segmento), 4)
            AS share_en_segmento
FROM a
ORDER BY anio, segmento, movimientos DESC
