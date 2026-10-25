# Auditoría de datos faltantes

Qué falta, qué se puede recuperar con cruces exactos y qué haría falta para el resto.

## 1. Completitud por año

País:

| anio | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_matricula | pct_sin_pasajeros | pct_sin_hora | pct_sin_od | pct_od_lad |
|---|---|---|---|---|---|---|---|---|
| 2019 | 580749 | 31.4 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.9 |
| 2020 | 212686 | 48.6 | 85.3 | 100.0 | 0.0 | 0.0 | 0.0 | 1.1 |
| 2021 | 329800 | 54.3 | 14.1 | 100.0 | 0.0 | 0.0 | 0.0 | 1.2 |
| 2022 | 477930 | 38.3 | 15.3 | 100.0 | 0.0 | 0.0 | 0.0 | 1.3 |
| 2023 | 557168 | 33.1 | 15.6 | 100.0 | 0.0 | 0.0 | 0.0 | 1.3 |
| 2024 | 578592 | 36.5 | 17.0 | 100.0 | 0.0 | 0.0 | 0.0 | 1.6 |
| 2025 | 597783 | 33.6 | 22.7 | 100.0 | 0.0 | 0.0 | 0.0 | 1.6 |
| 2026 | 419199 | 31.9 | 26.9 | 0.0 | 0.0 | 0.0 | 0.0 | 1.6 |

Foco (MDQ):

| anio | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_matricula | pct_sin_pasajeros | pct_sin_hora | pct_sin_od | pct_od_lad |
|---|---|---|---|---|---|---|---|---|
| 2019 | 8388 | 32.1 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.2 |
| 2020 | 3022 | 50.6 | 82.4 | 100.0 | 0.0 | 0.0 | 0.0 | 0.2 |
| 2021 | 3957 | 66.0 | 15.9 | 100.0 | 0.0 | 0.0 | 0.0 | 0.9 |
| 2022 | 6387 | 49.9 | 15.1 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2023 | 7571 | 47.2 | 19.2 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2024 | 7530 | 48.3 | 25.2 | 100.0 | 0.0 | 0.0 | 0.0 | 0.3 |
| 2025 | 6825 | 48.4 | 18.4 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2026 | 4455 | 47.3 | 18.3 | 0.0 | 0.0 | 0.0 | 0.0 | 2.2 |

Foco 2021+, por segmento:

| segmento | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_pasajeros |
|---|---|---|---|---|
| linea_regular | 15665 | 0.3 | 2.0 | 0.0 |
| privado | 8552 | 92.6 | 5.7 | 0.0 |
| oficial | 6265 | 85.7 | 89.5 | 0.0 |
| taxi_aereo | 3072 | 84.1 | 10.9 | 0.0 |
| instruccion | 2695 | 89.8 | 0.2 | 0.0 |
| charter_linea | 457 | 15.8 | 59.3 | 0.0 |
| trabajo_aereo | 19 | 100.0 | 0.0 | 0.0 |

## 2A. Operador por matrícula

| ambito | faltan_con_matricula | recuperables_unanime | matricula_con_algun_dato |
|---|---|---|---|
| MDQ | 2109 | 431 | 824 |
| resto del país | 131409 | 20229 | 42853 |

Foco, por segmento:

| segmento | faltan_con_matricula | recuperables_unanime |
|---|---|---|
| privado | 925 | 47 |
| oficial | 589 | 161 |
| instruccion | 330 | 186 |
| taxi_aereo | 261 | 34 |
| charter_linea | 2 | 2 |
| linea_regular | 2 | 1 |

Qué se recupera (foco, top 12):

| valor_recuperado | movimientos |
|---|---|
| CENTRO DE EXTENSION PROFESIONAL AERONAUTICA PREFECTURA NAVAL ARGENTINA CEPA - CIAC TIPO I | 84 |
| OFICIAL INSPECTOR MARIO E. WALLACE- POLICIA DE LA PROV. DE BS AS- CIAC TIPO III | 71 |
| FLIGHT TRAINING AMERICA- MK AEROMEDIA S.A | 65 |
| PRO FLIGHT ACADEMY SRL-CIAC TIPO III | 43 |
| JUST FLIGHT S.A. "ROYAL CLASS" | 34 |
| CWO S.A. - SUN FLIGHT- CIAC TIPO II | 25 |
| SAETA | 14 |
| CEAP - AERO CHANNEL S.R.L- CIAC TIPO II | 13 |
| TWR SRL | 10 |
| RADIAL 340 S.A.S.- CIAC TIPO II | 10 |
| PRESIDENCIA DE LA NACION | 10 |
| FLIGHT CENTER- TWR S.R.L-CIAC TIPO III | 9 |

## 2B. Aeronave por matrícula

| ambito | faltan_con_matricula | recuperables_unanime | matricula_con_algun_dato |
|---|---|---|---|
| MDQ | 815 | 0 | 0 |
| resto del país | 111963 | 1 | 1 |

Foco, por segmento:

| segmento | faltan_con_matricula | recuperables_unanime |
|---|---|---|
| oficial | 635 | 0 |
| charter_linea | 58 | 0 |
| linea_regular | 57 | 0 |
| privado | 42 | 0 |
| taxi_aereo | 23 | 0 |

Qué se recupera (foco, top 12):

| valor_recuperado | movimientos |
|---|---|


Comparación con la regla vigente (operador con >= 80 % de consistencia):

| operador_inferido_80 | en_foco |
|---|---|
| 36758 | 599 |

Aeronave faltante con matrícula presente en OpenSky (registro externo):

| faltan_con_matricula | con_tipo_en_opensky | en_foco |
|---|---|---|
| 112778 | 1 | 0 |

## 2C. El otro extremo del mismo vuelo (por matrícula, un solo candidato)

| ambito | movimientos_con_par_unico | operador_recuperable | aeronave_recuperable | pasajeros_recuperables | aeronave_distinta_en_cada_extremo |
|---|---|---|---|---|---|
| MDQ | 2646 | 38 | 0 | 0 | 0 |
| resto del país | 195792 | 1154 | 1 | 0 | 0 |

## 2D. Portal municipal 2015–2019 ↔ ANAC 2019 (foco)

Claves: fecha, hora local, aterrizaje/despegue, origen/destino y aerolínea.

| movimientos_anac_2019 | registros_municipales_2019 | anac_sin_aeronave | cruces_1_a_1 | aeronave_recuperable |
|---|---|---|---|---|
| 8388 | 2141 | 8388 | 1356 | 1356 |

Aeronaves recuperables, por segmento y modelo municipal:

| segmento | aeronave_municipal | movimientos |
|---|---|---|
| linea_regular | EMBRAER E-190 | 1209 |
| linea_regular | BOEING B-737 | 138 |
| charter_linea | EMBRAER E-145 | 9 |

## 3. Sin cruce posible con las fuentes actuales

| caso | movimientos_foco |
|---|---|
| Aeronave sin matrícula (2019–2025) | 17082 |
| Operador sin matrícula (2019–2025) | 20536 |
| Origen/destino en lugar apto denunciado (sin coordenadas) | 266 |
| Pasajeros sin dato | 0 |
