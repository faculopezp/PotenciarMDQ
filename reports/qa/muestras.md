# Muestras para validar — MDQ

## 1. Vuelos oficiales y militares sin modelo de avión (2021+)

Perfil del faltante:

| movimientos | sin_operador | vuelos_locales | con_pasajeros | con_matricula |
|---|---|---|---|---|
| 5606 | 4773 | 2603 | 877 | 635 |

Orígenes/destinos más frecuentes:

| origen_destino | movimientos |
|---|---|
| MDP | 2603 |
| DIL | 828 |
| AER | 476 |
| BCA | 417 |
| PAL | 269 |
| FDO | 154 |
| PDI | 148 |
| MOR | 70 |
| HPN | 63 |
| VIE | 58 |

Operadores informados:

| aerolinea_nombre | movimientos |
|---|---|
| Sin dato | 4773 |
| LADE | 511 |
| Ejercito Argentino | 96 |
| Fuerza Aérea Argentina | 68 |
| Usmil - Guardia Nac.F.Aer. (Eeuu) | 36 |
| Embajada De Los Estados Unidos | 24 |
| Gob.Estado Parana Brasil | 22 |
| Presidencia De La Nacion | 18 |
| L.A.D.E. | 10 |
| Fuerza Aerea Uruguaya | 8 |

Muestra (20 filas):

| fecha | hora_local | clase_vuelo | clasificacion_vuelo | tipo_movimiento | origen_destino | aerolinea_nombre | aeronave | matricula | pasajeros |
|---|---|---|---|---|---|---|---|---|---|
| 2025-03-13 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2021-08-26 | 6 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2024-06-05 | 12 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2023-07-10 | 10 | vuelo_oficial_nacional | cabotaje | despegue | DIL | Sin dato |  |  | 0 |
| 2026-03-12 | 10 | vuelo_oficial_extranjero | cabotaje | despegue | MDP | Embajada De Los Estados Unidos |  | 760168 | 0 |
| 2024-03-26 | 11 | vuelo_oficial_nacional | cabotaje | aterrizaje | DIL | Sin dato |  |  | 0 |
| 2026-06-19 | 9 | vuelo_oficial_nacional | cabotaje | despegue | TRC | Sin dato |  | PG380 | 2 |
| 2023-03-09 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2022-02-23 | 20 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2025-07-30 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2026-02-11 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  | PA41 | 0 |
| 2024-01-18 | 16 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2023-07-07 | 10 | vuelo_oficial_nacional | cabotaje | aterrizaje | PDI | Sin dato |  |  | 0 |
| 2021-07-15 | 12 | vuelo_oficial_nacional | cabotaje | despegue | BCA | Sin dato |  |  | 0 |
| 2023-07-05 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2021-08-05 | 13 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2026-03-04 | 20 | vuelo_oficial_nacional | cabotaje | aterrizaje | FDO | Sin dato |  | PA73 | 0 |
| 2024-02-15 | 20 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2026-04-30 | 16 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  | 2H244 | 0 |
| 2025-06-02 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |

## 2. Vuelos de línea 2019–2020 sin aeronave, 20 a 96 pasajeros

Por operador y familia inferida:

| anio | aerolinea_nombre | aeronave_familia_inferida | movimientos | pax_promedio | pax_max |
|---|---|---|---|---|---|
| 2019 | Aerolíneas Argentinas | Sin dato | 4129 | 70.6 | 96 |
| 2019 | Avian (Avianca Argentina) | ATR 42/72 | 601 | 44.4 | 72 |
| 2019 | Avian (Avianca Argentina) | Sin dato | 16 | 76.1 | 89 |
| 2019 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 13 | 40.4 | 44 |
| 2019 | American Jet | Sin dato | 3 | 44.0 | 44 |
| 2020 | Aerolíneas Argentinas | Sin dato | 967 | 73.4 | 96 |
| 2020 | American Jet | Sin dato | 2 | 38.5 | 40 |
| 2020 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 1 | 40.0 | 40 |

Muestra (20 filas):

| fecha | hora_local | clase_vuelo | clasificacion_vuelo | tipo_movimiento | origen_destino | aerolinea_nombre | aeronave | matricula | pasajeros | aeronave_familia_inferida |
|---|---|---|---|---|---|---|---|---|---|---|
| 2019-01-31 | 9 | regular | cabotaje | aterrizaje | AER | Avian (Avianca Argentina) |  |  | 59 | ATR 42/72 |
| 2019-08-06 | 20 | regular | cabotaje | despegue | EZE | Aerolíneas Argentinas |  |  | 50 | Sin dato |
| 2019-05-21 | 8 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 81 | Sin dato |
| 2019-11-11 | 22 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 82 | Sin dato |
| 2019-02-07 | 19 | regular | cabotaje | aterrizaje | BCA | Aerolíneas Argentinas |  |  | 53 | Sin dato |
| 2019-02-25 | 19 | regular | cabotaje | despegue | EZE | Aerolíneas Argentinas |  |  | 55 | Sin dato |
| 2019-01-31 | 10 | regular | cabotaje | despegue | BCA | Aerolíneas Argentinas |  |  | 67 | Sin dato |
| 2019-09-06 | 19 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 92 | Sin dato |
| 2019-08-04 | 12 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 84 | Sin dato |
| 2019-01-23 | 14 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 91 | Sin dato |
| 2020-02-05 | 13 | regular | cabotaje | aterrizaje | EZE | Aerolíneas Argentinas |  |  | 64 | Sin dato |
| 2020-03-17 | 8 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 42 | Sin dato |
| 2019-07-15 | 14 | regular | cabotaje | despegue | CBA | Aerolíneas Argentinas |  |  | 79 | Sin dato |
| 2020-02-04 | 15 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 96 | Sin dato |
| 2019-05-17 | 17 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 90 | Sin dato |
| 2019-01-15 | 13 | regular | cabotaje | despegue | CBA | Aerolíneas Argentinas |  |  | 80 | Sin dato |
| 2019-02-08 | 8 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 79 | Sin dato |
| 2019-01-29 | 19 | regular | cabotaje | aterrizaje | AER | Avian (Avianca Argentina) |  |  | 29 | ATR 42/72 |
| 2019-04-03 | 13 | regular | cabotaje | aterrizaje | CBA | Aerolíneas Argentinas |  |  | 71 | Sin dato |
| 2019-02-14 | 8 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 87 | Sin dato |

## 3. Inferencias aplicadas (config/aeronaves.yaml → inferencia)

| anio | aerolinea_nombre | aeronave_familia_inferida | movimientos | pax_min | pax_max |
|---|---|---|---|---|---|
| 2019 | Avian (Avianca Argentina) | ATR 42/72 | 662 | 2 | 72 |
| 2019 | Aerolíneas Argentinas | Boeing 737 | 443 | 97 | 179 |
| 2019 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 22 | 0 | 46 |
| 2020 | Aerolíneas Argentinas | Boeing 737 | 275 | 97 | 178 |
| 2020 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 2 | 24 | 40 |
| 2022 | Avian (Avianca Argentina) | ATR 42/72 | 2 | 0 | 0 |
| 2024 | Avian (Avianca Argentina) | ATR 42/72 | 2 | 0 | 0 |

## 4. Taxi aéreo declarado en biplaza → analizado como privado

| anio | aeronave_modelo | movimientos | pax_promedio | pax_max |
|---|---|---|---|---|
| 2020 | Cessna 150 | 38 | 0.0 | 0 |
| 2020 | Tecnam P2002 Sierra | 18 | 0.0 | 0 |
| 2020 | Tecnam P92 | 6 | 0.0 | 0 |
| 2020 | Cessna 152 | 6 | 0.0 | 0 |
| 2020 | Piper PA-38 Tomahawk | 2 | 0.0 | 0 |
| 2020 | Aero Boero 95/115 | 2 | 0.0 | 0 |
| 2021 | Tecnam P2002 Sierra | 46 | 0.0 | 0 |
| 2021 | Cessna 150 | 33 | 0.0 | 0 |
| 2021 | Tecnam P92 | 30 | 0.07 | 1 |
| 2021 | Cessna 152 | 22 | 0.0 | 0 |
| 2021 | Piper PA-38 Tomahawk | 7 | 0.0 | 0 |
| 2021 | BRM Aero Bristell | 5 | 0.0 | 0 |
| 2022 | Cessna 150 | 93 | 0.0 | 0 |
| 2022 | BRM Aero Bristell | 21 | 0.05 | 1 |
| 2022 | Tecnam P2002 Sierra | 21 | 0.0 | 0 |
| 2022 | Tecnam P92 | 20 | 0.0 | 0 |
| 2022 | Cessna 152 | 17 | 0.0 | 0 |
| 2022 | Piper PA-38 Tomahawk | 6 | 0.0 | 0 |
| 2022 | Piper Cub (PA-11/12/18) | 1 | 1.0 | 1 |
| 2023 | Cessna 150 | 81 | 0.0 | 0 |
| 2023 | Tecnam P2002 Sierra | 21 | 0.0 | 0 |
| 2023 | BRM Aero Bristell | 17 | 0.0 | 0 |
| 2023 | Cessna 152 | 14 | 0.0 | 0 |
| 2023 | Tecnam P92 | 12 | 0.0 | 0 |
| 2023 | Piper PA-38 Tomahawk | 11 | 0.0 | 0 |
| 2023 | Tecnam Astore | 3 | 0.0 | 0 |
| 2024 | Cessna 150 | 44 | 0.0 | 0 |
| 2024 | Tecnam P2002 Sierra | 40 | 0.0 | 0 |
| 2024 | Cessna 152 | 37 | 0.05 | 1 |
| 2024 | Tecnam Astore | 12 | 0.0 | 0 |
| 2024 | BRM Aero Bristell | 10 | 0.0 | 0 |
| 2024 | Tecnam P92 | 8 | 0.0 | 0 |
| 2024 | Tecnam P-Mentor | 7 | 0.0 | 0 |
| 2024 | Tecnam P2008 | 2 | 0.0 | 0 |
| 2024 | Piper PA-38 Tomahawk | 1 | 0.0 | 0 |
| 2025 | Cessna 150 | 57 | 0.0 | 0 |
| 2025 | Tecnam P2002 Sierra | 54 | 0.0 | 0 |
| 2025 | Cessna 152 | 21 | 0.0 | 0 |
| 2025 | BRM Aero Bristell | 16 | 0.0 | 0 |
| 2025 | Tecnam P92 | 13 | 0.08 | 1 |
| 2025 | Tecnam Astore | 9 | 0.0 | 0 |
| 2025 | Evektor Harmony LSA | 7 | 0.0 | 0 |
| 2025 | Ultraliviano (Petrel/912) | 3 | 0.0 | 0 |
| 2025 | Tecnam P-Mentor | 3 | 0.0 | 0 |
| 2025 | Piper PA-38 Tomahawk | 2 | 0.0 | 0 |
| 2025 | Piper Cub (PA-11/12/18) | 1 | 0.0 | 0 |
| 2026 | Cessna 150 | 48 | 0.0 | 0 |
| 2026 | Tecnam P2002 Sierra | 11 | 0.0 | 0 |
| 2026 | Cessna 152 | 10 | 0.0 | 0 |
| 2026 | BRM Aero Bristell | 9 | 0.0 | 0 |
| 2026 | Tecnam P92 | 8 | 0.0 | 0 |
| 2026 | Tecnam Astore | 7 | 0.0 | 0 |
| 2026 | Tecnam P2008 | 3 | 0.0 | 0 |
| 2026 | Van's RV-4/7/8/12 | 2 | 0.0 | 0 |
| 2026 | Tecnam P-Mentor | 1 | 0.0 | 0 |

## 5. Modelos estandarizados: denominaciones ANAC por modelo (foco)

| aeronave_modelo | aeronave_icao | denominaciones | como_figura_en_anac | movimientos |
|---|---|---|---|---|
| Embraer E190 | E190 | 1 | EMB-ERJ190100IGW | 10433 |
| Boeing 737-800 | B738 | 17 | BO-B-737-81D · BO-737-8Q8 · BO-737-8U3 · BO-B737-8BK · BO-B737-8MB · BO-B737-81D · BO-B737-8SH · BO-737-8BK · BO-737-8SH · BO-737-81D · BO-737-86N · BO-737-800 · BO-B737-800 · BO-737-8HX · BO-B737-86J · BO-737-8GJ · BO-B737-8LP | 2973 |
| Cessna 150 | C150 | 13 | CE-150-L · CE-150-K · CE-150 · CE-150-M · CE-150-H · CE-A-150-L · CE-150-A · CE-C-150-L · CE-150-F · CE-150-G · CE-150-J · CE-150-E · CE-AA-150-L | 2212 |
| Boeing 737-700 | B737 | 6 | BO-B-737-7BD · BO-737-7BD · BO-B-737-76N · BO-737-76N · BO-B-737-700 · BO-737-7K2 | 1318 |
| Tecnam P2002 Sierra |  | 7 | TEA-P2002 SIERRA · TEA-P2002 LSA · TEA-P2002 SIERRA MK2 · TEA-P2002-JF · TEA-P2002JF · TEA-P2002 · TEA-P2002 SIERRA MKII | 1067 |
| Cessna 152 | C152 | 4 | CE-152-II · CE-C-152 · CE-152 · CE-152-A | 916 |
| Beechcraft King Air 90 (C90/E90/A90/B90) | BE9L | 12 | BE-C90GT · RAY-C-90-GT · BE-65-A-90 · BE-E-90 · BE-C-90-GTI · BE-C-90 · BE-90-A · BE-C90GTI · HAB-C-90-A · RAY-C90A · BE-C-90-A · BE-C-90-B | 741 |
| Boeing 737 MAX 8 | B38M | 4 | BO-737-8 MAX · BO-B737-8MAX · BO-737-8 · BO-B737-8 | 734 |
| Cessna 182 | C182 | 18 | CE-182-C · CE-TR-182 · CE-182-T · CE-182-B · CE-182-A · CE-182-R · CE-A-182-N · TXA-182T · CE-182-F · CE-A-182-K · CE-R-182 · CE-T182T · CE-182-D · CE-A-182-J · CE-182 · TXA-R182 · CE-182-P · CE-182-G | 685 |
| Learjet 60 | LJ60 | 2 | LJ-60 · LJ-60-XR | 654 |
| BRM Aero Bristell |  | 3 | BRT-LSA · BRT-BRISTELL S-LSA · BRT-BRISTELL LSA | 531 |
| Tecnam P92 |  | 6 | TEA-P92 MKII · TEA-P92 EAGLET · TEA-P92 ECHO CLA · TEA-P92 ECHO MKII · TEA-P92 EAGLET G5 · TEA-P92-JS | 498 |
| Cessna 208B Grand Caravan | C208 | 2 | TXA-208B · CE-208-B | 368 |
| Piper PA-28 Cherokee/Warrior/Archer | P28A | 11 | PA-PA-28-180 · PAA-PA-A-28-181 · PA-PA-28-140 · PA-PA-28-161 · PA-PA-28 · PAA-PA-A-28-180 · PAA-PA-A-28-140 · PA-PA-28-180-D · PA-PA-28-181 · PAA-PA-A-28-236 · PA-PA-28-235 | 358 |
| Cessna Citation II/Bravo (550/551) | C550 | 4 | CE-550-B · CE-551-CITATION · CE-550 · CE-551 | 307 |
| Cessna Citation CJ1/M2 (525) | C525 | 2 | CE-525 · TXA-525 | 277 |
| Cessna 172 | C172 | 17 | CE-172-S · CE-172-M · CE-172-H · CE-172-N · CE-172-C · CE-172-B · CE-172RG · CE-172-L · CE-C-172-L · CE-A172N · CE-172 · CE-172-RG · CE-R-172-K · CE-R-172-G · CE-172-A · CE-172-E · CE-C-172-M | 272 |
| Beechcraft Baron 58 | BE58 | 8 | BE-BARON 58 · BE-58 · TXA-58 · BEF-58 · BE-58-P · HAB-G-58 · BE-G58 · BE-58-TC | 266 |
| Piper PA-31 Navajo | PA31 | 8 | PA-PA-31 · PAA-PA-A-31-325 · PAA-PA-A-31-310 · PA-PA-31P-350 · PAA-PA-A-31-350 · PA-PA-31-325 · PAA-PA-A-31-T · PA-PA-31-350 | 253 |
| Airbus H125/AS350 | AS50 | 3 | EUR-AS-350-B3 · ECU-AS-350-B3 · ARH-AS-350-B3 | 253 |
| Piper M500 (PA-46-500TP) | P46T | 2 | PAA-PA 46-500TP · PA-PA-46-500TP | 241 |
| Beechcraft King Air 200/B200 | BE20 | 3 | BE-200 · BE-B-200 · TXA-B200 | 225 |
| Piper PA-46 Malibu/Mirage | PA46 | 4 | PA-PA-46-350T · PA-PA-46-350-P · PA-PA-46R-350T · PA-PA-46R-350 | 220 |
| Cirrus SR22 | SR22 | 3 | CIR-SR 22T · CIT-SR22 · CIR-SR-22 | 214 |
| Cessna Citation V/Ultra/Encore (560) | C560 | 1 | CE-560 | 207 |
| Learjet 45 | LJ45 | 2 | LJ-45 · LJ-LJ45 | 200 |
| Beechcraft King Air B200GT | BE20 | 4 | TXA-B200GT · HAB-B-200-GT · BE-B-200-GT · BEF-B200GT | 199 |
| Piper PA-38 Tomahawk | PA38 | 2 | PAA-PA-A-38-112 · PA-PA-38-112 | 177 |
| Piper PA-28R Arrow | P28R | 7 | PAA-PA-A-28R201T · PA-PA-28-R-201T · PAA-PA-A-28-R200 · PAA-PA-A-28-R201 · PA-PA-28R-200 · PA-PA-28-200R · PA-PA-28R-180 | 177 |
| Piper PA-34 Seneca | PA34 | 3 | PA-PA-34-200-T · PAA-PA-A-34-200T · PA-PA-34-200 | 173 |
| Cessna Citation Excel/XLS (560XL) | C56X | 3 | TXA-560XL · CE-560-XI · CE-560-XL | 171 |
| Tecnam P2006T |  | 1 | TEA-P2006T | 159 |
| Learjet 31 | LJ31 | 2 | LJ-31-A · LJ-31 | 158 |
| Tecnam Astore |  | 1 | TEA-ASTORE | 135 |
| Beechcraft Baron 55 | BE55 | 5 | TXA-95-B55 · BE-E55 · BE-BARON B-55 · BE-BARON E-55 · BE-95-B55 | 130 |
| Airbus/MBB BK117/H145 |  | 6 | ARH-MBB-BK117 C2 · ARH-MBB-BK117 D-2 · EUR-EC-145 · EUR-MBB-BK-117C2 · EUR-MBB-BK-117C1 · ADG-MBB-BK-117C2 | 117 |
| Beechcraft Bonanza 36 | BE36 | 8 | BE-A-36 · BE-36 · BE-A36 · TXA-A-36 · TXA-G36 · BE-B-36-TC · BE-36 B 36TC · BE-G36 | 116 |
| Fairchild Metro III/23 (SA227) | SW4 | 2 | FA-SA-227-DC · FA-SA-227-AC | 105 |
| Otra |  | 29 | BEF-A36 · BE-D-95-A · TXA-F-33A · LBG-SH2 · WEA-620-A · ARH-EC 130 T2 · RSC-S6S-COYOTEII · HDP-UH-1D · CE-T240 · BE-B60 · EAE-EA500 · BE-B-23 · SLG-SLING 4 · LO-L-18-50 · DIP-CDP 001 · MT-MU-2B-25 · BE-65-B-80 · PT-S-2B · MAX-MH-1521 · TSA-S2R-T34 · RAB-S19-VENTERRA · ST-105 · AV1-BRISTELL CLASSIC · CE-T-303 · DIA-DA 42 · AE-7-EC · MAC-MB-308 · EFL-EA 300/L · EXP-EXPRESS CT | 101 |
| Cessna Citation I (500/501) | C501 | 3 | CE-C-501 · CE-501 · CE-500 | 99 |

## 6. Validación contra OpenSky (matrícula → tipo ICAO, todo el país)

Coincidencia del designador ICAO asignado por las reglas con el de OpenSky:

| matriculas | coinciden | pct_coinciden |
|---|---|---|
| 559 | 517 | 92.5 |

Discrepancias (revisar regla o dato de OpenSky):

| aeronave | aeronave_modelo | aeronave_icao | icao_opensky | modelo_opensky | matriculas | ejemplo |
|---|---|---|---|---|---|---|
| PAA-PA-A-31-T | Piper PA-31 Navajo | PA31 | PAY2 | PA-31T Cheyenne II | 3 | LV-MNR |
| BE-B-300 | Beechcraft King Air 300/350 | BE30 | B350 | King Air B350 | 3 | LV-CQA |
| CE-550 | Cessna Citation II/Bravo (550/551) | C550 | C55B | Citation Bravo | 3 | LV-BEU |
| CE-500 | Cessna Citation I (500/501) | C501 | C500 | Citation I | 2 | LV-BID |
| TXA-525 | Cessna Citation CJ1/M2 (525) | C525 | C25M | Citation M2 | 2 | LV-GMQ |
| LJ-45 | Learjet 45 | LJ45 | LJ75 |  | 2 | LQ-IJK |
| CIR-SR 22T | Cirrus SR22 | SR22 | S22T |  | 2 | LV-GQY |
| LJ-45 | Learjet 45 | LJ45 | LJ40 | Learjet 40 XR | 2 | LV-CJY |
| CE-R-182 | Cessna 182 | C182 | C82R |  | 2 | LV-CZI |
| TXA-T206H | Cessna 206 | C206 | T206 |  | 1 | LV-GUW |
| BOM-BD-700-1A11 | Bombardier Global Express | GLEX | GL5T | Global 5000 | 1 | LV-GQE |
| BOM-BD-100-1A10 | Bombardier Challenger 300/350 | CL30 | CL35 | Challenger 350 | 1 | LV-HAT |
| TXA-B300 | Beechcraft King Air 300/350 | BE30 | B350 |  | 1 | LV-JKD |
| BE-A-36 | Beechcraft Bonanza 36 | BE36 | BT36 |  | 1 | LV-CDB |
| CE-550-B | Cessna Citation II/Bravo (550/551) | C550 | C55B | Citation Bravo | 1 | LV-CTF |
| LJ-45 | Learjet 45 | LJ45 | LJ40 | Learjet 40 | 1 | LQ-BFS |
| CE-551-CITATION | Cessna Citation II/Bravo (550/551) | C550 | C551 | Citation II | 1 | LV-CEN |
| TXA-G36 | Beechcraft Bonanza 36 | BE36 | BE33 |  | 1 | LV-JUC |
| CE-R-172-G | Cessna 172 | C172 | C72R |  | 1 | LV-APA |
| CE-525 | Cessna Citation CJ1/M2 (525) | C525 | C25M | Citation M2 | 1 | LV-GUL |
| RO-R-44RAVEN-II | Robinson R44 | R44 | R66 |  | 1 | LV-JWU |
| RO-R66 | Robinson R66 | R66 | AT76 | ATR 72 600 | 1 | LV-GUI |
| CE-P-210-N | Cessna 210 | C210 | P210 |  | 1 | LV-MOR |
| LAN-L2KC LEGACY | Embraer Legacy 600 | E35L | LEG2 |  | 1 | LV-X544 |
| CE-500 | Cessna Citation I (500/501) | C501 | C500 | Cessna Citation I | 1 | LV-BPW |
| BE-36 | Beechcraft Bonanza 36 | BE36 | BT36 |  | 1 | LV-CNH |
| CE-152 | Cessna 152 | C152 | C150 |  | 1 | LV-IWB |
| CE-TR-182 | Cessna 182 | C182 | C82R |  | 1 | LV-FQE |
| CE-551 | Cessna Citation II/Bravo (550/551) | C550 | C551 | Citation II | 1 | LV-WXD |
| TXA-R182 | Cessna 182 | C182 | C82R |  | 1 | LV-KBR |

Tipos ICAO sugeridos por OpenSky para modelos sin designador:

| aeronave_modelo | icao_opensky | matriculas |
|---|---|---|
| Tecnam P2002 Sierra | SIRA | 23 |
| Tecnam P92 | ECHO | 10 |
| Tecnam P2006T | P06T | 5 |
| Tecnam Astore | ASTO | 3 |
| Piper Cheyenne (PA-31T/42) | PAY1 | 3 |
| Aero Commander 690 | AC90 | 3 |
| Airbus/MBB BK117/H145 | EC45 | 3 |
| BRM Aero Bristell | NG5 | 3 |
| Learjet 25 | LJ25 | 2 |
| Otra | CH7A | 2 |
| Beechcraft Bonanza 33/35 | BE35 | 2 |
| Air Tractor AT-802 | AT8T | 2 |
| Piper PA-32 Saratoga/Lance | PA32 | 2 |
| Piper PA-32 Saratoga/Lance | P32T | 2 |
| Tecnam P2010 | TWEN | 2 |
| Otra | UH1 | 1 |
| Otra | SLG4 | 1 |
| Otra | GLID | 1 |
| Otra | EA50 | 1 |
| Otra | MU2 | 1 |
| Piper PA-22 Tri-Pacer | PA22 | 1 |
| Bell | B222 | 1 |
| Piper Cub (PA-11/12/18) | PA11 | 1 |
| Otra | L8 | 1 |
| Otra | C240 | 1 |
| Evektor Harmony LSA | EV97 | 1 |
| Tecnam P2012 Traveller | P212 | 1 |
| Airbus/MBB BK117/H145 | BK17 | 1 |
| Tecnam P2008 | P208 | 1 |
| Otra | WW24 | 1 |
