-- Puntualidad y cancelaciones por aerolínea y sentido, en todo el registro (AA2000 vía
-- failbondi.fail); solo meses completos de cada sentido.
SELECT aerolinea, movimiento,
       min(fecha) AS desde, max(fecha) AS hasta,
       count(*)                                          AS programados,
       count(*) FILTER (WHERE cancelado)                 AS cancelados,
       count(demora_min)                                 AS con_horario_real,
       round(count(*) FILTER (WHERE a_horario) / nullif(count(demora_min), 0), 4) AS pct_a_horario,
       round(count(*) FILTER (WHERE cancelado) / count(*), 4)                     AS pct_cancelados,
       round(quantile_cont(demora_min, 0.5))             AS demora_mediana_min,
       round(quantile_cont(demora_min, 0.9))             AS demora_p90_min
FROM fct_vuelo_aa2000
WHERE mes_completo
GROUP BY ALL
HAVING count(*) >= 20
ORDER BY movimiento DESC, programados DESC
