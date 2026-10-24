# QA — BD PotenciarMDQ

## Filas y nulos por archivo

| source_file | filas | pct_fecha_null | pct_hora_null | pct_pax_null | pct_aeronave_null | pct_con_matricula | pct_provisorio | desde | hasta |
|---|---|---|---|---|---|---|---|---|---|
| 20261024_201912-informe-ministerio-actualizado-dic-final.csv | 580697 | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 2019-01-01 | 2019-12-31 |
| 20261024_202012-informe-ministerio-actualizado-dic-final.csv | 212726 | 0.0 | 0.0 | 0.0 | 85.3 | 0.0 | 0.0 | 2019-12-31 | 2020-12-31 |
| 20261024_202112-informe-ministerio-actualizado-dic-final.csv | 329781 | 0.0 | 0.0 | 0.0 | 14.06 | 0.0 | 0.0 | 2020-12-31 | 2021-12-31 |
| 20261024_202212-informe-ministerio-actualizado-dic-final.csv | 477903 | 0.0 | 0.0 | 0.0 | 15.28 | 0.0 | 0.0 | 2021-12-31 | 2022-12-31 |
| 20261024_202312-informe-ministerio-actualizado-dic.csv | 557152 | 0.0 | 0.0 | 0.0 | 15.63 | 0.0 | 0.0 | 2022-12-31 | 2023-12-31 |
| 20261024_202412-informe-ministerio-actualizado-dic-final.csv | 578602 | 0.0 | 0.0 | 0.0 | 17.01 | 0.0 | 0.0 | 2023-12-31 | 2024-12-31 |
| 20261024_202512-informe-ministerio-actualizado-dic-final.csv | 597784 | 0.0 | 0.0 | 0.0 | 22.73 | 0.0 | 0.0 | 2024-12-31 | 2025-12-31 |
| 20261024_202609-informe-ministerio-vf-matricula.csv | 419262 | 0.0 | 0.0 | 0.0 | 26.9 | 100.0 | 21.99 | 2025-12-31 | 2026-09-30 |

## Valores fuera de vocabulario: `clasificacion_vuelo`

| valor | filas |
|---|---|


## Valores fuera de vocabulario: `tipo_movimiento`

| valor | filas |
|---|---|


## Valores fuera de vocabulario: `calidad_dato`

| valor | filas |
|---|---|


## Clases de vuelo (ajustar `clases_comerciales` en config/mdq.yaml)

| clase_vuelo | es_comercial | filas |
|---|---|---|
| regular | True | 2122252 |
| vuelo_privado_con_matricula_nacional | False | 542059 |
| vuelo_escuela | False | 505222 |
| no_regular | True | 300365 |
| vuelo_oficial_nacional | False | 209269 |
| vuelo_privado_con_matricula_extranjera | False | 30633 |
| vuelo_de_adiestramiento | False | 27978 |
| trabajo_aereo | False | 12788 |
| vuelo_oficial_extranjero | False | 3341 |

## Duplicados exactos

| filas_duplicadas |
|---|
| 8143 |

## Correcciones de aeropuerto aplicadas

| aeropuerto_original | aeropuerto | filas |
|---|---|---|
| MDB | MDP | 9 |

## Cobertura de enriquecimiento (vuelos comerciales)

| pct_aeronave_otro | pct_aerolinea_sin_regla | pct_sin_distancia | pct_sin_asientos |
|---|---|---|---|
| 0.13 | 7.12 | 0.9 | 43.4 |

## Aeronaves sin clasificar (top 25 → ampliar config/aeronaves.yaml)

| aeronave | movimientos |
|---|---|
| AIB-A-330-223 | 1515 |
| LBG-SH2 | 511 |
| CE-C-501 | 457 |
| BE-B-36-TC | 416 |
| BE-V-35-B | 403 |
| ER-415-CD | 351 |
| BE-E55 | 310 |
| AVA-A-1 | 309 |
| HAF-HA-420 | 287 |
| BE-G36 | 286 |
| MC-BO-105-CBS | 282 |
| CE-C-337-G | 268 |
| BE-DUKE B-60 | 241 |
| CC-LY | 224 |
| BE-65-B-80 | 215 |
| BE-C-23 | 211 |
| RW-100-150 | 206 |
| RQ-RANQUEL | 191 |
| II-ARAVA 102 | 188 |
| AGW-AW 109SP | 165 |
| I.A-1124 | 165 |
| CE-T-303 | 153 |
| BE-M-35 | 151 |
| ARH-EC 130 B4 | 142 |
| TWC-500-C | 140 |

## Códigos sin coordenadas (top 25 → revisar dim_aeropuerto)

| origen_destino | movimientos | clasificacion | segmento | aeropuerto_que_lo_informa |
|---|---|---|---|---|
| 2278 | 11069 | internacional | privado | SAL |
| 3073 | 4193 | internacional | charter_linea | SAL |
| 2976 | 3794 | internacional | taxi_aereo | SAL |
| 3017 | 3696 | internacional | taxi_aereo | SAL |
| RAT | 2615 | cabotaje | charter_linea | SAL |
| 2324 | 1729 | internacional | oficial | POS |
| 2463 | 943 | internacional | privado | POS |
| 2870 | 866 | internacional | privado | FDO |
| BGI | 611 | cabotaje | privado | FDO |
| SLA | 587 | cabotaje | privado | ROS |
| HAL | 514 | cabotaje | privado | FDO |
| HNR | 500 | cabotaje | taxi_aereo | GRA |
| MLE | 486 | cabotaje | privado | ROS |
| HOP | 415 | cabotaje | oficial | PAL |
| 2417 | 413 | internacional | privado | FDO |
| 2999 | 410 | internacional | privado | FDO |
| 2341 | 406 | internacional | oficial | PAR |
| 2628 | 402 | internacional | privado | FDO |
| 2855 | 381 | internacional | privado | FDO |
| 2666 | 371 | internacional | privado | FDO |
| 2346 | 339 | internacional | privado | FDO |
| 3075 | 334 | internacional | privado | SAL |
| 2489 | 319 | internacional | privado | SIS |
| 2682 | 315 | internacional | oficial | SVO |
| 2634 | 312 | internacional | privado | SAL |

## Resolución de códigos de origen/destino

| fuente | codigos | movimientos | movimientos_foco |
|---|---|---|---|
| ourairports_local | 694 | 3045465 | 46896 |
| ourairports_oaci | 604 | 649834 | 609 |
| lad_sin_coordenadas | 663 | 48193 | 266 |
| sin_resolver | 161 | 7850 | 216 |
| anac | 18 | 2562 | 148 |

## Lista ANAC vs OurAirports (mismo código, distancia > 5 km)

| codigos_en_ambas | mas_de_5_km | mediana_km |
|---|---|---|
| 671 | 6 | 0.0 |

| codigo | nombre_anac | nombre_ourairports | distancia_km |
|---|---|---|---|
| HRR | MORRISON | Morrison Heliport | 102.0 |
| ROH | ROBERTS/FUMIGACIONES HERBINSEC | Fumigaciones Herbinsec Airport | 65.0 |
| HPG | PIEDRA DEL ÁGUILA/TRANSENER S.A. | Transener S.A. Heliport | 29.7 |
| HHL | LAS LAJAS/EA. HAYCHOL | Estancia Haychol Heliport | 11.1 |
| RAI | RANCHOS/LA IGUALDAD | La Igualdad Airport | 10.0 |
| YPY | YAPEYÚ | Yapeyú Airport | 9.8 |

## Vista previa de la lista ANAC (formato de coordenadas)

| codigo | oaci | iata | nombre | lat | lon |
|---|---|---|---|---|---|
| BHT |  |  | BRAGADO/HARAS TRELLIRIS | -35.33138888888889 | -60.57888888888889 |
| CLT |  | CCT | COLONIA CATRIEL | -37.908055555555556 | -67.82888888888888 |
| DIO |  |  | TANDIL/COMANDANTE EDUARDO A. OLIVERO | -37.346666666666664 | -58.98277777777778 |
| ELZ |  |  | ELIZALDE | -34.975 | -57.9625 |
| GAR |  |  | GENERAL ALVEAR | -35.97888888888889 | -59.90694444444444 |
| GLM |  |  | GUALEGUAYCHÚ/BLM CABAÑAS | -32.9775 | -58.522222222222226 |
| GOR | SACT |  | GOBERNADOR GORDILLO/CHAMICAL | -30.344166666666666 | -66.29416666666667 |
| GRZ |  |  | GENERAL RODRIGUEZ | -34.58277777777778 | -59.00055555555556 |

## Tramos reconstruidos (cabotaje comercial)

| tramos | despegues_cabotaje | pct_emparejado |
|---|---|---|
| 778460 | 915317 | 85.0 |

## Rotaciones: método por matrícula vs por modelo

| aeropuerto | metodo_emparejamiento | tipo_rotacion | n | mediana_min |
|---|---|---|---|---|
| BAR | matricula | escala_larga | 191 | 165.0 |
| BAR | matricula | pernocte | 93 | 1029.0 |
| BAR | matricula | rotacion | 4153 | 68.0 |
| BAR | modelo | escala_larga | 837 | 148.0 |
| BAR | modelo | pernocte | 367 | 925.0 |
| BAR | modelo | rotacion | 31347 | 64.0 |
| BCA | matricula | escala_larga | 67 | 195.0 |
| BCA | matricula | pernocte | 28 | 1139.0 |
| BCA | matricula | rotacion | 1036 | 49.0 |
| BCA | modelo | escala_larga | 131 | 178.0 |
| BCA | modelo | pernocte | 281 | 605.0 |
| BCA | modelo | rotacion | 5126 | 52.0 |
| DOZ | matricula | escala_larga | 134 | 200.0 |
| DOZ | matricula | pernocte | 322 | 633.0 |
| DOZ | matricula | rotacion | 3925 | 61.0 |
| DOZ | modelo | escala_larga | 561 | 190.0 |
| DOZ | modelo | pernocte | 924 | 613.0 |
| DOZ | modelo | rotacion | 26748 | 57.0 |
| MDP | matricula | escala_larga | 266 | 235.0 |
| MDP | matricula | pernocte | 95 | 1148.0 |
| MDP | matricula | rotacion | 1323 | 52.0 |
| MDP | modelo | escala_larga | 364 | 206.0 |
| MDP | modelo | pernocte | 97 | 1413.0 |
| MDP | modelo | rotacion | 7344 | 52.0 |
| NEU | matricula | escala_larga | 295 | 211.0 |
| NEU | matricula | pernocte | 775 | 993.0 |
| NEU | matricula | rotacion | 3694 | 53.0 |
| NEU | modelo | escala_larga | 515 | 247.0 |
| NEU | modelo | pernocte | 1252 | 1028.0 |
| NEU | modelo | rotacion | 18595 | 53.0 |
| SAL | matricula | escala_larga | 241 | 161.0 |
| SAL | matricula | pernocte | 1125 | 1118.0 |
| SAL | matricula | rotacion | 4112 | 56.0 |
| SAL | modelo | escala_larga | 554 | 149.0 |
| SAL | modelo | pernocte | 2664 | 1103.0 |
| SAL | modelo | rotacion | 22399 | 57.0 |

## Aeronave faltante en el foco (potencial de inferencia por pasajeros)

| anio | segmento | movimientos | sin_aeronave | sin_aeronave_mas_de_96_pax | sin_aeronave_20_a_96_pax | sin_aeronave_menos_de_20_pax |
|---|---|---|---|---|---|---|
| 2019 | linea_regular | 5324 | 5324 | 445 | 4757 | 122 |
| 2019 | taxi_aereo | 967 | 967 | 0 | 7 | 960 |
| 2019 | privado | 807 | 807 | 0 | 5 | 802 |
| 2019 | oficial | 669 | 669 | 0 | 8 | 661 |
| 2019 | instruccion | 539 | 539 | 0 | 0 | 539 |
| 2019 | trabajo_aereo | 50 | 50 | 0 | 0 | 50 |
| 2019 | charter_linea | 32 | 32 | 0 | 5 | 27 |
| 2020 | linea_regular | 1351 | 1265 | 275 | 968 | 22 |
| 2020 | privado | 532 | 306 | 0 | 0 | 306 |
| 2020 | oficial | 411 | 397 | 0 | 2 | 395 |
| 2020 | instruccion | 382 | 223 | 0 | 0 | 223 |
| 2020 | taxi_aereo | 324 | 276 | 0 | 1 | 275 |
| 2020 | trabajo_aereo | 19 | 19 | 0 | 0 | 19 |
| 2020 | charter_linea | 3 | 3 | 0 | 2 | 1 |
| 2021 | privado | 1212 | 16 | 0 | 0 | 16 |
| 2021 | linea_regular | 1128 | 3 | 0 | 0 | 3 |
| 2021 | oficial | 689 | 585 | 0 | 18 | 567 |
| 2021 | taxi_aereo | 464 | 26 | 0 | 0 | 26 |
| 2021 | instruccion | 421 | 0 | 0 | 0 | 0 |
| 2021 | charter_linea | 31 | 0 | 0 | 0 | 0 |
| 2021 | trabajo_aereo | 12 | 0 | 0 | 0 | 0 |
| 2022 | linea_regular | 2820 | 60 | 0 | 1 | 59 |
| 2022 | privado | 1506 | 46 | 0 | 0 | 46 |
| 2022 | oficial | 897 | 791 | 0 | 20 | 771 |
| 2022 | taxi_aereo | 554 | 44 | 0 | 2 | 42 |
| 2022 | instruccion | 539 | 1 | 0 | 0 | 1 |
| 2022 | charter_linea | 68 | 23 | 0 | 1 | 22 |
| 2022 | trabajo_aereo | 3 | 0 | 0 | 0 | 0 |
| 2023 | linea_regular | 3593 | 89 | 0 | 5 | 84 |
| 2023 | privado | 1668 | 56 | 0 | 0 | 56 |
| 2023 | oficial | 1222 | 1131 | 0 | 14 | 1117 |
| 2023 | taxi_aereo | 603 | 107 | 0 | 0 | 107 |
| 2023 | instruccion | 392 | 3 | 0 | 0 | 3 |
| 2023 | charter_linea | 91 | 68 | 0 | 5 | 63 |
| 2023 | trabajo_aereo | 2 | 0 | 0 | 0 | 0 |
| 2024 | linea_regular | 3233 | 57 | 0 | 4 | 53 |
| 2024 | privado | 1756 | 275 | 0 | 1 | 274 |
| 2024 | oficial | 1491 | 1408 | 0 | 38 | 1370 |
| 2024 | taxi_aereo | 544 | 100 | 0 | 0 | 100 |
| 2024 | instruccion | 417 | 1 | 0 | 0 | 1 |
| 2024 | charter_linea | 89 | 57 | 0 | 3 | 54 |
| 2025 | linea_regular | 2949 | 48 | 0 | 9 | 39 |
| 2025 | privado | 1463 | 55 | 0 | 0 | 55 |
| 2025 | oficial | 1172 | 1056 | 0 | 55 | 1001 |
| 2025 | taxi_aereo | 594 | 34 | 0 | 0 | 34 |
| 2025 | instruccion | 543 | 0 | 0 | 0 | 0 |
| 2025 | charter_linea | 102 | 65 | 0 | 15 | 50 |
| 2025 | trabajo_aereo | 2 | 0 | 0 | 0 | 0 |
| 2026 | linea_regular | 1942 | 57 | 0 | 12 | 45 |
| 2026 | privado | 1131 | 42 | 0 | 0 | 42 |
| 2026 | oficial | 794 | 635 | 0 | 43 | 592 |
| 2026 | taxi_aereo | 328 | 23 | 0 | 0 | 23 |
| 2026 | instruccion | 186 | 0 | 0 | 0 | 0 |
| 2026 | charter_linea | 74 | 58 | 0 | 11 | 47 |

## Meses sin movimientos en el foco

| mes_faltante |
|---|


## Outliers: load factor estimado > 1,1 en el foco

| fecha | aeronave | aerolinea_nombre | pasajeros | asientos_estimados | lf_estimado |
|---|---|---|---|---|---|
| 2022-04-18 | LJ-60 | Aerolíneas Argentinas | 160 | 7.0 | 22.857 |
| 2021-08-26 | CE-150-G | Aerolíneas Argentinas | 87 | 43.0 | 2.023 |
| 2022-01-29 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 183 | 97.0 | 1.887 |
| 2021-12-30 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 181 | 97.0 | 1.866 |
| 2022-11-06 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 156 | 97.0 | 1.608 |
| 2023-10-01 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 143 | 97.0 | 1.474 |
| 2022-12-28 | BO-737-76N | Aerolíneas Argentinas | 172 | 129.0 | 1.333 |
| 2023-10-01 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 125 | 97.0 | 1.289 |
| 2022-10-04 | BO-737-76N | Aerolíneas Argentinas | 162 | 129.0 | 1.256 |
| 2023-01-26 | BO-B737-8MB | Aerolíneas Argentinas | 204 | 172.0 | 1.186 |
| 2024-12-22 | EMB-ERJ190100IGW | Aerolíneas Argentinas | 108 | 97.0 | 1.113 |

## Reconciliación vs fuente oficial (config/reconciliacion.csv)

| anio | mes | aeropuerto_anac | pasajeros_oficial | pasajeros_datos | dif_pax_pct | movimientos_oficial | movimientos_datos | dif_movs_pct |
|---|---|---|---|---|---|---|---|---|

