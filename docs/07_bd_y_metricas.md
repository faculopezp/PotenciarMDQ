# Nuestra BD: tablas, columnas y métricas

Archivo: `data/potenciar_mdq.duckdb` (+ copia en `data/bd/*.parquet`). Se reconstruye con `make bd`.
Validada con datos reales ANAC 2023–2026 (2,1 M de movimientos, 41 s).

**Nivel de confianza** de cada columna: **D** = dato de ANAC tal cual · **N** = normalizado
(mismo dato, limpio) · **C** = calculado exacto · **E** = estimado (modelo/heurística, leer con cuidado).

## Formatos reales de ANAC que la estandarización resuelve

| Problema | Ejemplo real | Regla |
|---|---|---|
| Coma decimal en pasajeros (2023–2025) | `199,00` | → `199` (BIGINT) |
| Hora sin cero inicial | `0:01` | → `00:01:00` |
| "0" como sin dato | Aerolínea `0`, Aeronave `0` | → NULL |
| Columna nueva en 2026 | `Matrícula` | Se agrega; NULL antes de 2026 |
| `PAX` ≠ `Pasajeros` | cabotaje: PAX = Pasajeros / 2 | `pax_nacional` (para totales país); `pasajeros` para aeropuerto |
| Error de código | 10 vuelos E190 del 13/08/2023 como `MDB` (Batán) | Corrección configurable → `MDP`, con flag |
| Encoding / gzip / CRLF | — | Detección automática |

## Dimensiones

### `dim_fecha` (una fila por día)
`fecha`, `anio`, `mes`, `dia`, `trimestre`, `semana_iso`, `dia_semana` (1 = lun), `dia_semana_nombre`,
`es_fin_de_semana`, `es_feriado`, `feriado_nombre` (incluye feriados puente), `es_no_laborable`,
`es_finde_largo` (racha ≥ 3 días no laborables), `es_temporada_verano` (dic–feb), `verano_anio`
(diciembre cuenta para el verano siguiente), `es_julio` (proxy de vacaciones de invierno).

### `dim_aeropuerto` (OurAirports)
`codigo` (= código que usa ANAC: local para AR, OACI para el exterior), `oaci`, `iata`, `nombre`,
`ciudad`, `pais`, `region`, `lat`, `lon`, `tipo`, `es_foco`, `es_par`, `distancia_mdq_km`.

### `dim_aerolinea` (`config/aerolineas.yaml`)
`aerolinea` (texto ANAC) → `aerolinea_nombre` (normalizado: "AEROLINEAS ARGENTINAS SA" → "Aerolíneas
Argentinas") y `aerolinea_tipo` (bandera, low_cost, regional, estatal, taxi_aereo, extranjera, carga, otra).

### `dim_aeronave` (`config/aeronaves.yaml`)
`aeronave` (código ANAC, ej. `EMB-ERJ190100IGW`) → `fabricante`, `familia` (Embraer E190, Boeing 737…),
`categoria`: jet_fuselaje_ancho, jet_fuselaje_angosto, jet_regional, turbohelice_regional,
jet_ejecutivo, turbohelice_ejecutivo, helicoptero, agricola, aviacion_general_piston, otro.
Cobertura real: 99,9 % de los movimientos comerciales clasificados.

### `dim_capacidad` (E)
Asientos estimados por `aerolinea + aeronave` (o solo `aeronave`): percentil 95 de pasajeros
observados en vuelos comerciales de todo el país (mínimo 30 vuelos). Resultado con datos reales:
E190 de Aerolíneas = 96, 737-8 de Aerolíneas = 172, 737-8Q8 de Flybondi = 189 (coinciden con las
configuraciones publicadas por esas aerolíneas). Para tipos con pocos vuelos completos el p95 queda
por debajo de la capacidad real y el load factor sale inflado: por eso se marca como estimado.

## Hechos

### `fct_movimiento` — 1 fila = 1 aterrizaje o despegue

| Grupo | Columnas | Conf. |
|---|---|---|
| Tiempo | `fecha_utc`, `hora_utc`, `ts_utc`, `ts_local`, `fecha` (local), `anio`, `mes`, `hora_local`, `franja_horaria` (madrugada/mañana/tarde/noche) | D/C |
| Calendario | `dia_semana`, `dia_semana_nombre`, `es_fin_de_semana`, `es_feriado`, `es_finde_largo`, `es_temporada_verano`, `verano_anio` | C |
| Tipo de vuelo | `clase_vuelo`, `es_comercial`, `es_regular`, `clasificacion_vuelo` (cabotaje/internacional), `tipo_movimiento` | N/C |
| Lugar | `aeropuerto`, `aeropuerto_original`, `aeropuerto_corregido`, `origen_destino`, `distancia_km` | N/C |
| Operador y avión | `aerolinea`, `aerolinea_nombre`, `aerolinea_tipo`, `aeronave`, `aeronave_fabricante`, `aeronave_familia`, `aeronave_categoria`, `matricula`, `matricula_origen` | D/N |
| Demanda | `pasajeros`, `pax_nacional` | D |
| Oferta (E) | `asientos_estimados`, `fuente_asientos`, `lf_estimado` | E |
| Producción (E) | `rpk_est` = pasajeros × km, `ask_est` = asientos × km | C/E |
| Calidad | `calidad_dato`, `es_provisorio`, `source_file` | D |

### `fct_tramo` — vuelos reconstruidos (cabotaje comercial)
Une despegue en A con el primer aterrizaje en B del mismo operador y modelo (y matrícula desde 2026),
entre 15 y 600 min. Cobertura real: 86 % de los despegues de cabotaje.
Columnas: `origen`, `destino`, `salida_utc`, `llegada_utc`, `duracion_min` (pista a pista),
`velocidad_bloque_kmh`, `pax_despegue`, `pax_aterrizaje`, `pax_diferencia`, `metodo_emparejamiento`.
Validación real: AEP→MDQ mediana 44 min (E190) / 42 min (737).

### `fct_rotacion` — turnaround en MDQ y pares
Aterrizaje → siguiente despegue del mismo avión (15 min a 36 h). `tiempo_en_tierra_min`,
`tipo_rotacion` (rotacion ≤ 120 min · escala_larga · pernocte = pasa la noche), `viene_de`, `va_a`.
Validación real: con matrícula (2026) mediana 52 min; con método por modelo (2023–2025) 51 min.

## Métricas de aviación disponibles (y fórmula)

| Métrica | Fórmula | Dónde | Conf. |
|---|---|---|---|
| Movimientos / ATM | count(*), count(*) FILTER (es_comercial) | marts | C |
| Pasajeros (ACI) | Σ pasajeros en MDQ (embarcados + desembarcados) | marts | D |
| Pasajeros por movimiento | pax comerciales / movimientos comerciales | `mart_mdq_anual` | C |
| **Load factor** | Σ pax / Σ asientos estimados (solo filas con ambos) | anual, mensual, rutas, aerolíneas, pares | E |
| **ASK / RPK** | Σ asientos × km / Σ pax × km | `mart_mdq_anual` | E/C |
| Distancia media por pasajero | RPK / pax | `mart_mdq_anual` | C |
| **Turnaround** | mediana de tiempo en tierra (rotaciones ≤ 120 min) | rotaciones, anual, pares | E |
| Pernoctes | rotaciones que cruzan la noche | `mart_mdq_anual` | E |
| **Duración de vuelo** | mediana de `duracion_min` por ruta | tramos, rutas | E |
| Velocidad de bloque | km / horas de vuelo | tramos | E |
| **Hora pico (SBR)** | 30.ª hora con más pasajeros del año | anual | C |
| **TPHP (FAA)** | hora pico del día promedio del mes pico | anual | C |
| Récord horario | máx. pasajeros en una hora | anual | C |
| Índice estacional | pax mes / promedio mensual del año | mensual | C |
| Ratio pico/valle | máx. mensual / mín. mensual | anual, pares | C |
| Coef. de variación mensual | desvío / media | anual | C |
| Share temporada de verano | pax dic–feb / pax año | anual, pares | C |
| Balance direccional | pax llegados − pax salidos | mensual, diario | C |
| Media móvil 7 días y var. interanual | sobre la serie diaria (t − 364 días) | diario | C |
| Frecuencia semanal por ruta | salidas / semanas | rutas | C |
| HHI aerolíneas | Σ share² × 10.000 | anual | C |
| Destinos regulares | origen_destino distintos con vuelos regulares | anual, pares | C |
| Share no comercial | movimientos no comerciales / total | anual, pares | C |
| Matrículas distintas | aviones distintos (desde 2026) | anual | D |

**No calculables con estos datos:** puntualidad, cancelaciones, tarifas, origen de los pasajeros.

## Marts (lo que consume la web)

`mart_mdq_anual`, `mart_mdq_mensual`, `mart_mdq_diario`, `mart_mdq_hora_semana`, `mart_mdq_rutas`
(con coordenadas), `mart_mdq_verano`, `mart_mdq_aerolineas`, `mart_mdq_aeronaves`,
`mart_mdq_rotaciones`, `mart_mdq_tramos`, `mart_mdq_aviacion_general`, `mart_benchmark_pares`,
`mart_mdq_explorador`. Todos en `sql/`.

## Ampliación 2026-10-24: toda la aviación, serie larga y analítica

| Objeto | Qué agrega |
|---|---|
| `fct_movimiento.segmento`, `es_linea`, `es_vuelo_local` | Segmentos: línea regular, charter de línea, taxi aéreo, privado, oficial/militar, escuelas, trabajo aéreo (`config/mdq.yaml → segmentos`) |
| `fct_municipal_mensual` | Series del portal municipal en formato largo (dataset, serie, año, mes, valor, unidad) |
| `fct_mdq_vuelos_hist` | Movimientos 2015–2019 del portal municipal (muestra ~52 %), con segmento y familia |
| `dim_clima` | Clima diario en MDQ (Open-Meteo): código de tiempo, lluvia, viento, ráfagas, temperatura |
| `mart_mdq_segmentos_*`, `mart_mdq_avion_tipico`, `mart_mdq_operadores` | Perfil de cada segmento, avión típico (por movimientos y por pasajeros), operadores y orígenes |
| `mart_mdq_serie_larga`, `mart_mdq_turismo`, `mart_mdq_findes_largos` | Serie 2001+, turistas vs pasajeros aéreos, visitantes por fin de semana largo |
| `mart_ranking_nacional`, `mart_red_aeropuertos` | Puesto de MDQ por pasajeros y por PageRank en la red de cabotaje |
| `mart_mdq_dias_atipicos` | Gráfico de control diario + clima; eventos con fuente en `config/eventos.yaml` |
| `mart_mdq_tendencia`, `mart_mdq_pronostico` | STL sobre la serie larga; Holt-Winters a 6 meses con banda del 80 % |

**Aeronave faltante (2019+, MDQ):** 37 % de los movimientos no tienen modelo. 2019: 100 % (el CSV de ANAC no lo
informa); 2020: 82 %; 2021+: 15–25 %, concentrado en vuelos oficiales/militares (91 % sin modelo). El reporte de
QA ("Aeronave faltante en el foco") cuantifica por año, segmento y rango de pasajeros cuántos se podrían
inferir (ej. > 96 pasajeros solo puede ser un jet de fuselaje angosto).
