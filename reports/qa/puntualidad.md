# Puntualidad y cancelaciones: validación

Fuente: web de Aeropuertos Argentina recopilada por failbondi.fail (último estado de cada vuelo). ANAC: movimientos de línea en el foco.

## 1. Vuelos y pasajeros por mes contra ANAC

Operados = no cancelados. ANAC cuenta despegues y aterrizajes de línea.

| anio | mes | aa_salidas | anac_despegues | aa_llegadas | anac_aterrizajes | aa_pax_sal | anac_pax_sal | dif_pax_sal_pct | aa_pax_lleg | anac_pax_lleg | dif_pax_lleg_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024 | 12 | 40 | 125 | 40 | 126 | 3040 | 11728 | -74.1 | 4004 | 13059 | -69.3 |
| 2025 | 1 | 203 | 197 | 138 | 199 | 20761 | 21063 | -1.4 | 14172 | 21289 | -33.4 |
| 2025 | 2 | 172 | 168 | 0 | 169 | 17116 | 17183 | -0.4 |  | 16200 |  |
| 2025 | 3 | 154 | 152 | 0 | 153 | 15361 | 15427 | -0.4 |  | 13852 |  |
| 2025 | 4 | 127 | 115 | 0 | 119 | 11244 | 11241 | 0.0 |  | 11176 |  |
| 2025 | 5 | 110 | 96 | 0 | 95 | 9610 | 9516 | 1.0 |  | 8965 |  |
| 2025 | 6 | 117 | 98 | 0 | 98 | 9937 | 9690 | 2.5 |  | 9362 |  |
| 2025 | 7 | 129 | 121 | 0 | 122 | 10167 | 10312 | -1.4 |  | 10075 |  |
| 2025 | 8 | 115 | 105 | 0 | 106 | 9045 | 8972 | 0.8 |  | 9111 |  |
| 2025 | 9 | 114 | 102 | 0 | 103 | 10219 | 10287 | -0.7 |  | 9613 |  |
| 2025 | 10 | 117 | 102 | 65 | 106 | 10370 | 10254 | 1.1 | 5317 | 10706 | -50.3 |
| 2025 | 11 | 141 | 129 | 140 | 129 | 12630 | 12366 | 2.1 | 12726 | 12291 | 3.5 |
| 2025 | 12 | 144 | 134 | 144 | 134 | 12443 | 12700 | -2.0 | 13371 | 13476 | -0.8 |
| 2026 | 1 | 202 | 195 | 202 | 196 | 18435 | 18283 | 0.8 | 19462 | 18973 | 2.6 |
| 2026 | 2 | 159 | 146 | 159 | 146 | 14665 | 14623 | 0.3 | 13979 | 13843 | 1.0 |
| 2026 | 3 | 143 | 129 | 143 | 129 | 13867 | 13541 | 2.4 | 13156 | 12920 | 1.8 |
| 2026 | 4 | 122 | 111 | 120 | 111 | 11500 | 11493 | 0.1 | 10912 | 10867 | 0.4 |
| 2026 | 5 | 95 | 90 | 95 | 90 | 8970 | 9033 | -0.7 | 8695 | 8658 | 0.4 |
| 2026 | 6 | 100 | 92 | 98 | 91 | 9418 | 9656 | -2.5 | 9006 | 8857 | 1.7 |
| 2026 | 7 | 101 | 85 | 101 | 84 | 8494 | 8425 | 0.8 | 8428 | 8260 | 2.0 |
| 2026 | 8 | 88 | 79 | 89 | 79 | 7599 | 7614 | -0.2 | 7637 | 7417 | 3.0 |
| 2026 | 9 | 94 | 84 | 93 | 83 | 8778 | 8761 | 0.2 | 8623 | 8729 | -1.2 |
| 2026 | 10 | 92 |  | 90 |  | 7798 |  |  | 8004 |  |  |

## 2. Estados informados

| movimiento | estado | cancelado | vuelos | con_horario_real |
|---|---|---|---|---|
| llegada | Aterrizado | False | 1677 | 1677 |
| llegada |  | False | 38 | 0 |
| llegada | Cancelado | True | 23 | 0 |
| llegada | Consulte Cía. | False | 1 | 0 |
| llegada | Reprogramado | False | 1 | 0 |
| salida | Despegado | False | 2827 | 2827 |
| salida | Cancelado | True | 73 | 0 |
| salida | En Horario | False | 24 | 0 |
| salida |  | False | 24 | 0 |
| salida | NO OPERA | True | 1 | 0 |
| salida | Demorado | False | 1 | 0 |
| salida | Consulte Cía. | False | 1 | 0 |
| salida | Pre Embarque | False | 1 | 0 |
| salida | Reprogramado | False | 1 | 0 |

## 3. Posibles duplicados (mismo sentido, programado y matrícula)

| movimiento | programado | matricula | vuelos |
|---|---|---|---|
| salida | 2025-05-27 18:45:00 | LVCID | AEROLINEAS ARGENTINAS AR 1607 · AEROLINEAS ARGENTINAS AR 1607 |
| salida | 2026-04-11 21:30:00 | LVKFW | ANDES LINEAS AEREAS O4 901 · ANDES LINEAS AEREAS O4 902 |

## 4. Demoras extremas (más de 6 horas o adelantos de más de 1 hora)

| fecha | movimiento | aerolinea | nro | otro_extremo | programado | real | demora_min | estado |
|---|---|---|---|---|---|---|---|---|
| 2026-07-01 | salida | AEROLINEAS ARGENTINAS | AR 1603 | AEP | 2026-07-01 09:10:00 | 2026-07-05 09:22:00 | 5772 | Despegado |
| 2026-08-06 | salida | AEROLINEAS ARGENTINAS | AR 1613 | AEP | 2026-08-06 22:15:00 | 2026-08-07 23:48:00 | 1533 | Despegado |
| 2025-04-18 | salida | LADE | 5U 503 | AEP | 2025-04-17 16:35:00 | 2025-04-18 08:19:00 | 944 | Despegado |
| 2025-11-17 | salida | AEROLINEAS ARGENTINAS | AR 1613 | AEP | 2025-11-17 09:11:00 | 2025-11-17 00:20:00 | -531 | Despegado |
| 2026-07-01 | llegada | LADE | 5U 505 | CRD | 2026-06-30 16:00:00 | 2026-07-01 00:17:00 | 497 | Aterrizado |
| 2026-07-01 | salida | LADE | 5U 505 | AEP | 2026-06-30 16:40:00 | 2026-07-01 00:55:00 | 495 | Despegado |
| 2025-02-28 | salida | AEROLINEAS ARGENTINAS | AR 1567 | COR | 2025-02-28 13:45:00 | 2025-02-28 21:38:00 | 473 | Despegado |
| 2026-03-11 | salida | AEROLINEAS ARGENTINAS | AR 1429 | MDZ | 2026-03-11 15:45:00 | 2026-03-11 23:00:00 | 435 | Despegado |
| 2026-10-10 | salida | AEROLINEAS ARGENTINAS | AR 1609 | AEP | 2026-10-10 13:45:00 | 2026-10-10 20:24:00 | 399 | Despegado |
| 2026-10-10 | llegada | AEROLINEAS ARGENTINAS | AR 1608 | AEP | 2026-10-10 13:05:00 | 2026-10-10 19:41:00 | 396 | Aterrizado |
| 2025-01-08 | llegada | AEROLINEAS ARGENTINAS | AR 1608 | AEP | 2025-01-08 15:09:00 | 2025-01-08 13:11:00 | -118 | Aterrizado |
| 2025-06-27 | salida | ANDES LINEAS AEREAS | O4 655 | EZE | 2025-06-27 23:30:00 | 2025-06-27 21:36:00 | -114 | Despegado |
| 2025-06-27 | salida | ANDES LINEAS AEREAS (ANTIGUO) | OY 653 | PDP | 2025-06-27 15:40:00 | 2025-06-27 14:14:00 | -86 | Despegado |
| 2025-01-08 | llegada | AEROLINEAS ARGENTINAS | AR 1566 | COR | 2025-01-08 15:03:00 | 2025-01-08 13:45:00 | -78 | Aterrizado |
| 2026-05-05 | salida | LADE | 5U 505 | AEP | 2026-05-05 16:30:00 | 2026-05-05 15:24:00 | -66 | Despegado |
| 2026-03-03 | salida | LADE | 5U 505 | AEP | 2026-03-03 16:40:00 | 2026-03-03 15:35:00 | -65 | Despegado |
