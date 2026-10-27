-- Puntualidad y cancelaciones: estado de cada vuelo de línea en el aeropuerto del foco según la web
-- de Aeropuertos Argentina (AA2000), recopilado por failbondi.fail desde dic-2024. Último estado
-- de cada vuelo; demora = real − programado (salida: despegue; llegada: aterrizaje), en minutos.
-- a_horario: hasta 15 minutos de demora (criterio habitual de la industria).
-- completo: el mes y sentido tienen al menos 80 % de los vuelos del otro sentido (el scraper no
-- guardó llegadas entre febrero y septiembre de 2025) y el registro cubre el mes entero.
CREATE OR REPLACE TABLE fct_vuelo_aa2000 AS
WITH v AS (
  SELECT *, year(fecha) AS anio, month(fecha) AS mes,
         demora_min <= 15 AS a_horario
  FROM stg_vuelos_aa2000
  WHERE aeropuerto = getvariable('foco_iata')
),
rango AS (SELECT min(fecha) AS desde, max(fecha) AS hasta FROM v),
mes AS (
  SELECT anio, mes,
         count(*) FILTER (WHERE movimiento = 'salida')  AS n_sal,
         count(*) FILTER (WHERE movimiento = 'llegada') AS n_lleg
  FROM v GROUP BY ALL
)
SELECT v.*,
       (CASE WHEN v.movimiento = 'salida' THEN m.n_sal >= 0.8 * m.n_lleg
             ELSE m.n_lleg >= 0.8 * m.n_sal END)
       AND make_date(v.anio, v.mes, 1) >= r.desde
       AND last_day(make_date(v.anio, v.mes, 1)) <= r.hasta AS mes_completo
FROM v JOIN mes m USING (anio, mes) CROSS JOIN rango r;
