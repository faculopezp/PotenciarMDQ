-- Turnaround (tiempo en tierra) en MDQ por año, aerolínea y familia de aeronave.
SELECT
  anio, aerolinea_nombre, aeronave_familia, tipo_rotacion, metodo_emparejamiento,
  count(*)                                       AS rotaciones,
  median(tiempo_en_tierra_min)                   AS mediana_min,
  quantile_cont(tiempo_en_tierra_min, 0.25)      AS p25_min,
  quantile_cont(tiempo_en_tierra_min, 0.75)      AS p75_min
FROM fct_rotacion
WHERE aeropuerto = getvariable('foco')
GROUP BY ALL
ORDER BY anio, rotaciones DESC
