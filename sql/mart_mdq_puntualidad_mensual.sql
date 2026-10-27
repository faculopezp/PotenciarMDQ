-- Puntualidad y cancelaciones por mes y sentido (AA2000 vía failbondi.fail). Ver 95_puntualidad.sql.
SELECT anio, mes, make_date(anio, mes, 1) AS periodo, movimiento,
       count(*)                                          AS programados,
       count(*) FILTER (WHERE cancelado)                 AS cancelados,
       count(demora_min)                                 AS con_horario_real,
       count(*) FILTER (WHERE a_horario)                 AS a_horario,
       round(count(*) FILTER (WHERE a_horario) / nullif(count(demora_min), 0), 4) AS pct_a_horario,
       round(count(*) FILTER (WHERE cancelado) / count(*), 4)                     AS pct_cancelados,
       round(quantile_cont(demora_min, 0.5))             AS demora_mediana_min,
       round(quantile_cont(demora_min, 0.9))             AS demora_p90_min,
       sum(pasajeros) FILTER (WHERE NOT cancelado)       AS pasajeros,
       bool_and(mes_completo)                            AS completo
FROM fct_vuelo_aa2000
GROUP BY ALL
ORDER BY anio, mes, movimiento
