# Muestras para validar — MDQ

## 1. Vuelos oficiales y militares sin modelo de avión (2021+)

Perfil del faltante:

| movimientos | sin_operador | vuelos_locales | con_pasajeros | con_matricula |
|---|---|---|---|---|
| 5177 | 3957 | 2410 | 736 | 211 |

Orígenes/destinos más frecuentes:

| origen_destino | movimientos |
|---|---|
| MDP | 2410 |
| DIL | 818 |
| AER | 398 |
| BCA | 334 |
| PAL | 259 |
| PDI | 148 |
| FDO | 143 |
| MOR | 67 |
| HPN | 53 |
| VIE | 47 |

Operadores informados:

| aerolinea_nombre | movimientos |
|---|---|
| Sin dato | 3957 |
| Fuerza Aérea Argentina | 472 |
| LADE | 396 |
| Ejército Argentino | 94 |
| Armada Argentina | 56 |
| Prefectura Naval Argentina | 38 |
| Usmil - Guardia Nac.F.Aer. (Eeuu) | 35 |
| Presidencia De La Nacion | 28 |
| Embajada De Los Estados Unidos | 24 |
| Gob.Estado Parana Brasil | 23 |

Muestra (20 filas):

| fecha | hora_local | clase_vuelo | clasificacion_vuelo | tipo_movimiento | origen_destino | aerolinea_nombre | aeronave | matricula | pasajeros |
|---|---|---|---|---|---|---|---|---|---|
| 2025-03-13 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2021-08-26 | 6 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2024-06-05 | 12 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2023-07-10 | 10 | vuelo_oficial_nacional | cabotaje | despegue | DIL | Sin dato |  |  | 0 |
| 2026-03-12 | 10 | vuelo_oficial_extranjero | cabotaje | despegue | MDP | Embajada De Los Estados Unidos |  | 760168 | 0 |
| 2024-03-26 | 11 | vuelo_oficial_nacional | cabotaje | aterrizaje | DIL | Sin dato |  |  | 0 |
| 2023-03-09 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2022-02-23 | 20 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2025-07-30 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2024-01-18 | 16 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2023-07-07 | 10 | vuelo_oficial_nacional | cabotaje | aterrizaje | PDI | Sin dato |  |  | 0 |
| 2021-07-15 | 12 | vuelo_oficial_nacional | cabotaje | despegue | BCA | Sin dato |  |  | 0 |
| 2023-07-05 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2021-08-05 | 13 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2026-03-04 | 20 | vuelo_oficial_nacional | cabotaje | aterrizaje | FDO | Prefectura Naval Argentina |  | PA73 | 0 |
| 2024-02-15 | 20 | vuelo_oficial_nacional | cabotaje | despegue | MDP | Sin dato |  |  | 0 |
| 2026-04-30 | 16 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Armada Argentina |  | 2H244 | 0 |
| 2025-06-02 | 12 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |
| 2022-12-06 | 17 | vuelo_oficial_nacional | cabotaje | aterrizaje | DIL | Sin dato |  |  | 0 |
| 2025-07-01 | 11 | vuelo_oficial_nacional | cabotaje | aterrizaje | MDP | Sin dato |  |  | 0 |

## 2. Vuelos de línea 2019–2020 sin aeronave, 20 a 96 pasajeros

Por operador y familia inferida:

| anio | aerolinea_nombre | aeronave_familia_inferida | movimientos | pax_promedio | pax_max |
|---|---|---|---|---|---|
| 2019 | Aerolíneas Argentinas | Embraer E190 | 3 | 74.3 | 88 |
| 2019 | American Jet | Sin dato | 3 | 44.0 | 44 |
| 2019 | Avian (Avianca Argentina) | ATR 42/72 | 1 | 51.0 | 51 |
| 2020 | Aerolíneas Argentinas | Embraer E190 | 601 | 70.0 | 96 |
| 2020 | American Jet | Sin dato | 2 | 38.5 | 40 |
| 2020 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 1 | 40.0 | 40 |

Muestra (20 filas):

| fecha | hora_local | clase_vuelo | clasificacion_vuelo | tipo_movimiento | origen_destino | aerolinea_nombre | aeronave | matricula | pasajeros | aeronave_familia_inferida |
|---|---|---|---|---|---|---|---|---|---|---|
| 2020-02-05 | 13 | regular | cabotaje | aterrizaje | EZE | Aerolíneas Argentinas |  |  | 64 | Embraer E190 |
| 2020-02-04 | 15 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 96 | Embraer E190 |
| 2020-02-27 | 10 | regular | cabotaje | despegue | BCA | Aerolíneas Argentinas |  |  | 39 | Embraer E190 |
| 2020-02-28 | 9 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 56 | Embraer E190 |
| 2020-01-10 | 14 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 83 | Embraer E190 |
| 2020-03-03 | 10 | regular | cabotaje | aterrizaje | EZE | Aerolíneas Argentinas |  |  | 54 | Embraer E190 |
| 2020-01-15 | 12 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 86 | Embraer E190 |
| 2020-02-15 | 14 | regular | cabotaje | despegue | CBA | Aerolíneas Argentinas |  |  | 83 | Embraer E190 |
| 2020-02-15 | 23 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 84 | Embraer E190 |
| 2020-02-01 | 16 | regular | cabotaje | despegue | EZE | Aerolíneas Argentinas |  |  | 90 | Embraer E190 |
| 2020-02-28 | 16 | regular | cabotaje | despegue | TUC | Aerolíneas Argentinas |  |  | 90 | Embraer E190 |
| 2020-03-15 | 13 | regular | cabotaje | aterrizaje | CBA | Aerolíneas Argentinas |  |  | 63 | Embraer E190 |
| 2020-01-29 | 14 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 65 | Embraer E190 |
| 2020-02-25 | 20 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 96 | Embraer E190 |
| 2020-02-29 | 19 | regular | cabotaje | aterrizaje | BCA | Aerolíneas Argentinas |  |  | 57 | Embraer E190 |
| 2020-02-01 | 21 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 84 | Embraer E190 |
| 2020-02-22 | 21 | regular | cabotaje | aterrizaje | AER | Aerolíneas Argentinas |  |  | 26 | Embraer E190 |
| 2020-02-29 | 21 | regular | cabotaje | despegue | AER | Aerolíneas Argentinas |  |  | 94 | Embraer E190 |
| 2020-01-03 | 18 | regular | cabotaje | aterrizaje | BCA | Aerolíneas Argentinas |  |  | 66 | Embraer E190 |
| 2020-02-06 | 19 | regular | cabotaje | aterrizaje | BCA | Aerolíneas Argentinas |  |  | 42 | Embraer E190 |

## 3. Inferencias aplicadas (config/aeronaves.yaml → inferencia)

| anio | aerolinea_nombre | aeronave_familia_inferida | movimientos | pax_min | pax_max |
|---|---|---|---|---|---|
| 2019 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 7 | 15 | 46 |
| 2019 | Aerolíneas Argentinas | Embraer E190 | 4 | 54 | 90 |
| 2019 | Avian (Avianca Argentina) | ATR 42/72 | 1 | 51 | 51 |
| 2020 | Aerolíneas Argentinas | Embraer E190 | 986 | 4 | 172 |
| 2020 | Aerolíneas Argentinas | Boeing 737 | 121 | 36 | 178 |
| 2020 | Flyest S.A. Líneas Aéreas | Bombardier CRJ | 2 | 24 | 40 |
| 2023 | Aerolíneas Argentinas | Embraer E190 | 1 | 1 | 1 |

## 3b. Backtest de las reglas (línea 2021+ en el foco, avión conocido)

Se aplica cada regla como si no se supiera el avión y se compara con el real.

| orden | operador | pax_min | pax_max | modelo_inferido | vuelos | pct_acierto_familia | pct_acierto_modelo |
|---|---|---|---|---|---|---|---|
| 2 | AEROLINEAS ARGENTINAS|AUSTRAL | 1.0 | 96.0 | Embraer E190 | 10484 | 93.3 | 93.3 |
| 3 | AEROLINEAS ARGENTINAS|AUSTRAL | 129.0 | 200.0 | Boeing 737-800 / MAX 8 | 2410 | 99.7 | 95.2 |

## 4. Taxi aéreo a pistón con menos de taxi_min_plazas → analizado como privado

| anio | aeronave_modelo | aeronave_plazas | movimientos | pax_promedio | pax_max |
|---|---|---|---|---|---|
| 2019 | Piper M500 (PA-46-500TP) |  | 54 | 0.2 | 2 |
| 2019 | Tecnam P2002 Sierra | 2 | 46 | 0.0 | 0 |
| 2019 | Cessna Citation II/Bravo (550) |  | 22 | 3.32 | 7 |
| 2019 | Beechcraft King Air B200GT |  | 19 | 1.47 | 7 |
| 2019 | Tecnam P2006T | 4 | 16 | 0.81 | 2 |
| 2019 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 14 | 0.07 | 1 |
| 2019 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 14 | 2.29 | 5 |
| 2019 | Piper PA-28R Arrow | 4 | 13 | 0.0 | 0 |
| 2019 | Piper PA-38 Tomahawk | 2 | 12 | 0.0 | 0 |
| 2019 | Piper PA-30/39 Twin Comanche | 4 | 10 | 0.0 | 0 |
| 2019 | Embraer Phenom 100 |  | 6 | 0.83 | 4 |
| 2019 | Piper M600 (PA-46-600TP) |  | 6 | 0.0 | 0 |
| 2019 | Hawker 800XP |  | 6 | 0.0 | 0 |
| 2019 | Beechcraft King Air 200/B200 |  | 6 | 6.0 | 10 |
| 2019 | Tecnam P92 | 2 | 5 | 0.0 | 0 |
| 2019 |  |  | 5 | 0.0 | 0 |
| 2019 | Learjet 60 |  | 5 | 3.6 | 8 |
| 2019 | Cessna Citation CJ1/M2 (525) |  | 5 | 1.6 | 3 |
| 2019 | Cessna Citation V/Ultra/Encore (560) |  | 5 | 3.2 | 8 |
| 2019 | Ultraliviano (Petrel/912) | 2 | 4 | 0.0 | 0 |
| 2019 | Learjet 45 |  | 4 | 2.5 | 4 |
| 2019 | Cessna Citation Excel/XLS (560XL) |  | 3 | 1.67 | 4 |
| 2019 | Learjet 31 |  | 3 | 1.67 | 2 |
| 2019 | Piper Cheyenne (PA-31T/42) |  | 3 | 4.67 | 5 |
| 2019 | Cessna Citation Mustang (510) |  | 3 | 0.0 | 0 |
| 2019 | Cessna Citation CJ3 (525B) |  | 2 | 1.0 | 1 |
| 2019 | HondaJet HA-420 |  | 2 | 0.0 | 0 |
| 2019 | Beechjet 400A |  | 2 | 3.5 | 5 |
| 2019 | Grumman American GA-7 Cougar | 4 | 2 | 0.0 | 0 |
| 2019 | Robinson R44 | 4 | 2 | 1.5 | 3 |
| 2019 | Cessna Citation CJ2 (525A) |  | 2 | 1.0 | 2 |
| 2019 | Mitsubishi MU-2B |  | 2 | 2.0 | 4 |
| 2019 | Pipistrel Virus | 2 | 2 | 0.0 | 0 |
| 2019 | Pipistrel Alpha Trainer | 2 | 2 | 0.0 | 0 |
| 2019 | Cessna Citation Bravo (550B) |  | 2 | 0.5 | 1 |
| 2019 | Beechcraft Baron 58 | 6 | 1 | 0.0 | 0 |
| 2019 | Beechcraft King Air 300 |  | 1 | 2.0 | 2 |
| 2019 | Piper PA-24 Comanche | 4 | 1 | 0.0 | 0 |
| 2020 | Cessna 150 | 2 | 38 | 0.0 | 0 |
| 2020 | Tecnam P2002 Sierra | 2 | 18 | 0.0 | 0 |
| 2020 | Piper M500 (PA-46-500TP) |  | 9 | 0.33 | 1 |
| 2020 | Cessna 152 | 2 | 6 | 0.0 | 0 |
| 2020 | Cessna Citation I (500/501) |  | 6 | 2.0 | 3 |
| 2020 | Tecnam P92 | 2 | 6 | 0.0 | 0 |
| 2020 | Cessna 182 | 4 | 5 | 0.0 | 0 |
| 2020 | Cessna 182RG | 4 | 4 | 0.0 | 0 |
| 2020 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 4 | 0.0 | 0 |
| 2020 | Learjet 25 |  | 3 | 0.0 | 0 |
| 2020 | Cessna 208B Grand Caravan |  | 3 | 2.33 | 4 |
| 2020 | Beechcraft King Air 200/B200 |  | 3 | 0.67 | 1 |
| 2020 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 2 | 2.5 | 4 |
| 2020 | Cessna 172 | 4 | 2 | 1.0 | 1 |
| 2020 | HondaJet HA-420 |  | 2 | 0.0 | 0 |
| 2020 | Piper PA-28R Arrow | 4 | 2 | 0.0 | 0 |
| 2020 | Piper PA-38 Tomahawk | 2 | 2 | 0.0 | 0 |
| 2020 | Aero Boero 95/115 | 3 | 2 | 0.0 | 0 |
| 2020 | Learjet 35 |  | 2 | 1.0 | 1 |
| 2020 | Cessna Citation III/VI/VII (650) |  | 2 | 3.5 | 6 |
| 2020 | Embraer Phenom 100 |  | 1 | 0.0 | 0 |
| 2021 | Tecnam P2002 Sierra | 2 | 47 | 0.0 | 0 |
| 2021 | Piper M500 (PA-46-500TP) |  | 44 | 0.36 | 2 |
| 2021 | Cessna 150 | 2 | 33 | 0.0 | 0 |
| 2021 | Tecnam P92 | 2 | 30 | 0.07 | 1 |
| 2021 | Cessna 182 | 4 | 27 | 0.26 | 3 |
| 2021 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 25 | 2.88 | 6 |
| 2021 | Cessna 152 | 2 | 22 | 0.0 | 0 |
| 2021 | Learjet 60 |  | 20 | 2.3 | 8 |
| 2021 | Cessna Citation II/Bravo (550) |  | 16 | 3.5 | 8 |
| 2021 | Cessna 172 | 4 | 15 | 1.07 | 2 |
| 2021 | Cessna Citation V/Ultra/Encore (560) |  | 15 | 2.67 | 7 |
| 2021 | Cessna Citation CJ1/M2 (525) |  | 14 | 2.43 | 7 |
| 2021 | Cessna Citation Excel/XLS (560XL) |  | 14 | 1.21 | 7 |
| 2021 | Piper PA-28R Arrow | 4 | 14 | 1.21 | 3 |
| 2021 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 13 | 0.46 | 3 |
| 2021 | Cessna Citation I (500/501) |  | 10 | 1.5 | 5 |
| 2021 | Beechcraft King Air B200GT |  | 9 | 1.67 | 6 |
| 2021 | Learjet 45 |  | 8 | 2.0 | 6 |
| 2021 | Piper PA-38 Tomahawk | 2 | 7 | 0.0 | 0 |
| 2021 | Cessna 208B Grand Caravan |  | 6 | 2.17 | 5 |
| 2021 | Beechcraft King Air 200/B200 |  | 6 | 4.17 | 7 |
| 2021 | BRM Aero Bristell | 2 | 5 | 0.0 | 0 |
| 2021 | Cirrus SR22 | 5 | 4 | 0.25 | 1 |
| 2021 | Embraer Phenom 100 |  | 4 | 3.5 | 5 |
| 2021 | Cessna Citation CJ3 (525B) |  | 4 | 0.5 | 1 |
| 2021 | Hawker 800XP |  | 4 | 4.75 | 7 |
| 2021 | Learjet 31 |  | 3 | 2.33 | 4 |
| 2021 | Cessna |  | 3 | 0.0 | 0 |
| 2021 | Mooney M20 | 4 | 3 | 0.33 | 1 |
| 2021 | Bombardier Challenger 604/605 |  | 2 | 2.0 | 4 |
| 2021 | Pipistrel Alpha Trainer | 2 | 2 | 0.0 | 0 |
| 2021 | Cirrus SR20 | 5 | 2 | 2.0 | 2 |
| 2021 | Cessna 177 | 4 | 2 | 0.0 | 0 |
| 2021 | Cessna Citation Mustang (510) |  | 2 | 0.0 | 0 |
| 2021 | Cessna 208 Caravan |  | 2 | 0.5 | 1 |
| 2021 | Tecnam P2006T | 4 | 2 | 0.0 | 0 |
| 2021 | Piper Cheyenne (PA-31T/42) |  | 2 | 2.5 | 5 |
| 2021 | Beechjet 400A |  | 2 | 2.0 | 2 |
| 2021 | Piper PA-30/39 Twin Comanche | 4 | 2 | 0.0 | 0 |
| 2021 | Cessna Citation II/SP (551) |  | 2 | 3.5 | 7 |
| 2021 | Pipistrel Virus | 2 | 1 | 0.0 | 0 |
| 2021 | Express Design Express CT |  | 1 | 5.0 | 5 |
| 2021 | Beechcraft King Air 300 |  | 1 | 5.0 | 5 |
| 2021 | Robinson R44 | 4 | 1 | 0.0 | 0 |
| 2021 | Learjet 25 |  | 1 | 1.0 | 1 |
| 2022 | Cessna 150 | 2 | 94 | 0.0 | 0 |
| 2022 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 85 | 1.79 | 6 |
| 2022 | Cessna Citation Excel/XLS (560XL) |  | 54 | 1.48 | 7 |
| 2022 | Piper M500 (PA-46-500TP) |  | 41 | 0.15 | 1 |
| 2022 | Learjet 60 |  | 38 | 2.87 | 9 |
| 2022 | Beechcraft King Air 200/B200 |  | 30 | 3.07 | 8 |
| 2022 | Tecnam P2006T | 4 | 27 | 0.89 | 2 |
| 2022 | Beechcraft King Air B200GT |  | 23 | 1.91 | 8 |
| 2022 | Tecnam P2002 Sierra | 2 | 21 | 0.0 | 0 |
| 2022 | BRM Aero Bristell | 2 | 21 | 0.05 | 1 |
| 2022 | Tecnam P92 | 2 | 20 | 0.0 | 0 |
| 2022 | Learjet 45 |  | 19 | 3.63 | 8 |
| 2022 | Cessna Citation V/Ultra/Encore (560) |  | 19 | 2.95 | 9 |
| 2022 | Cessna 152 | 2 | 17 | 0.0 | 0 |
| 2022 | Learjet 31 |  | 17 | 3.71 | 9 |
| 2022 | Cessna Citation II/Bravo (550) |  | 14 | 2.43 | 7 |
| 2022 | Cessna 208B Grand Caravan |  | 12 | 1.08 | 6 |
| 2022 | Cessna Citation Mustang (510) |  | 10 | 1.2 | 4 |
| 2022 | Cirrus SR22 | 5 | 9 | 2.33 | 4 |
| 2022 | Cessna 182 | 4 | 9 | 0.89 | 4 |
| 2022 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 9 | 0.78 | 2 |
| 2022 | Cessna Citation I (500/501) |  | 8 | 1.5 | 4 |
| 2022 | Robinson R44 | 4 | 8 | 1.5 | 2 |
| 2022 | HondaJet HA-420 |  | 7 | 1.86 | 5 |
| 2022 | Piper PA-28R Arrow | 4 | 6 | 0.83 | 2 |
| 2022 | Piper PA-38 Tomahawk | 2 | 6 | 0.0 | 0 |
| 2022 | Piper M600 (PA-46-600TP) |  | 6 | 0.0 | 0 |
| 2022 | Cessna 172 | 4 | 6 | 0.17 | 1 |
| 2022 | Beechjet 400A |  | 5 | 2.2 | 4 |
| 2022 | Mooney M20 | 4 | 5 | 0.4 | 1 |
| 2022 | Hawker 800XP |  | 5 | 6.0 | 9 |
| 2022 | Cessna Citation CJ1/M2 (525) |  | 5 | 2.6 | 5 |
| 2022 | Learjet 35 |  | 4 | 1.0 | 3 |
| 2022 | Piper PA-34 Seneca | 6 | 4 | 0.0 | 0 |
| 2022 | Bombardier Challenger 604/605 |  | 3 | 3.67 | 11 |
| 2022 | Cessna Citation II/SP (551) |  | 3 | 2.33 | 4 |
| 2022 | Piper PA-30/39 Twin Comanche | 4 | 3 | 1.33 | 2 |
| 2022 | Cirrus SR20 | 5 | 3 | 0.0 | 0 |
| 2022 | Tecnam P2008 | 2 | 2 | 0.0 | 0 |
| 2022 | Aero Commander 690 |  | 2 | 6.0 | 6 |
| 2022 | Mitsubishi MU-2B |  | 2 | 2.0 | 4 |
| 2022 | Embraer Phenom 100 |  | 2 | 2.5 | 5 |
| 2022 | Pilatus PC-12 |  | 2 | 2.0 | 2 |
| 2022 | Beechcraft King Air F90 |  | 2 | 0.0 | 0 |
| 2022 | Piper Cub (PA-11/12/18) | 2 | 1 | 1.0 | 1 |
| 2022 | Piper Cheyenne (PA-31T/42) |  | 1 | 0.0 | 0 |
| 2022 |  |  | 1 | 0.0 | 0 |
| 2022 | Inp-New (otro) |  | 1 | 0.0 | 0 |
| 2023 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 111 | 1.73 | 6 |
| 2023 | Cessna 150 | 2 | 82 | 0.0 | 0 |
| 2023 | Learjet 60 |  | 58 | 2.64 | 9 |
| 2023 | Piper M500 (PA-46-500TP) |  | 37 | 0.11 | 2 |
| 2023 | Cessna 208B Grand Caravan |  | 33 | 1.09 | 5 |
| 2023 | Cessna 182 | 4 | 26 | 0.15 | 2 |
| 2023 | Beechcraft King Air 200/B200 |  | 24 | 2.75 | 8 |
| 2023 | Cessna Citation CJ1/M2 (525) |  | 24 | 2.0 | 5 |
| 2023 | Cessna Citation V/Ultra/Encore (560) |  | 24 | 3.08 | 7 |
| 2023 | Tecnam P2002 Sierra | 2 | 22 | 0.0 | 0 |
| 2023 | Cessna Citation II/SP (551) |  | 20 | 0.6 | 5 |
| 2023 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 19 | 0.84 | 3 |
| 2023 | Beechcraft King Air B200GT |  | 19 | 3.21 | 11 |
| 2023 | BRM Aero Bristell | 2 | 17 | 0.0 | 0 |
| 2023 | Cessna Citation II/Bravo (550) |  | 15 | 2.93 | 5 |
| 2023 | Learjet 45 |  | 14 | 3.14 | 9 |
| 2023 | Cessna 152 | 2 | 14 | 0.0 | 0 |
| 2023 | Tecnam P92 | 2 | 13 | 0.0 | 0 |
| 2023 | Learjet 35 |  | 11 | 2.18 | 5 |
| 2023 | Piper PA-38 Tomahawk | 2 | 11 | 0.0 | 0 |
| 2023 | Beechcraft King Air 300 |  | 11 | 1.0 | 5 |
| 2023 | Embraer Phenom 100 |  | 10 | 1.0 | 4 |
| 2023 | Cessna Citation Excel/XLS (560XL) |  | 9 | 3.0 | 6 |
| 2023 | HondaJet HA-420 |  | 9 | 2.11 | 4 |
| 2023 | Bombardier Challenger 604/605 |  | 7 | 3.71 | 11 |
| 2023 | Mooney M20 | 4 | 7 | 1.14 | 2 |
| 2023 | Tecnam P2006T | 4 | 6 | 0.67 | 2 |
| 2023 | Gulfstream IV/G400/G450 |  | 6 | 3.33 | 7 |
| 2023 | Learjet 31 |  | 6 | 1.33 | 3 |
| 2023 | Cirrus SR22 | 5 | 5 | 0.6 | 2 |
| 2023 | Cessna 172 | 4 | 5 | 0.4 | 1 |
| 2023 | Cessna Citation I (500/501) |  | 4 | 1.0 | 2 |
| 2023 | Piper PA-28R Arrow | 4 | 4 | 0.0 | 0 |
| 2023 | Hawker 800XP |  | 4 | 3.25 | 7 |
| 2023 | Beechjet 400A |  | 4 | 2.0 | 4 |
| 2023 | Tecnam Astore | 2 | 3 | 0.0 | 0 |
| 2023 | Aero Commander 690 |  | 3 | 2.33 | 3 |
| 2023 | Dassault Falcon 900EX |  | 3 | 5.0 | 11 |
| 2023 | Cessna Citation CJ2 (525A) |  | 2 | 5.0 | 5 |
| 2023 | Cessna Citation Mustang (510) |  | 2 | 1.0 | 2 |
| 2023 | Cessna 208 Caravan |  | 2 | 4.5 | 6 |
| 2023 | Grumman American GA-7 Cougar | 4 | 2 | 0.0 | 0 |
| 2023 | Cessna Citation CJ3 (525B) |  | 1 | 2.0 | 2 |
| 2023 | Pitts S-2B | 2 | 1 | 0.0 | 0 |
| 2023 | Bombardier Challenger 300/350 |  | 1 | 4.0 | 4 |
| 2023 | Extra EA-500 |  | 1 | 1.0 | 1 |
| 2023 | Piper PA-23 Apache/Aztec | 5 | 1 | 0.0 | 0 |
| 2023 | Piper PA-34 Seneca | 6 | 1 | 0.0 | 0 |
| 2023 | Cessna |  | 1 | 7.0 | 7 |
| 2024 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 99 | 1.24 | 7 |
| 2024 | Cessna 150 | 2 | 44 | 0.0 | 0 |
| 2024 | Tecnam P2002 Sierra | 2 | 42 | 0.0 | 0 |
| 2024 | Piper M500 (PA-46-500TP) |  | 41 | 0.1 | 2 |
| 2024 | Cessna 152 | 2 | 39 | 0.05 | 1 |
| 2024 | Learjet 60 |  | 26 | 2.85 | 8 |
| 2024 | Cessna 208B Grand Caravan |  | 24 | 1.29 | 10 |
| 2024 | Cessna Citation II/SP (551) |  | 24 | 0.21 | 2 |
| 2024 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 19 | 0.63 | 3 |
| 2024 | Cessna 182 | 4 | 18 | 0.67 | 3 |
| 2024 | Beechcraft King Air B200GT |  | 14 | 1.07 | 7 |
| 2024 | Cessna Citation CJ1/M2 (525) |  | 14 | 2.0 | 6 |
| 2024 | Learjet 45 |  | 14 | 2.5 | 9 |
| 2024 | Learjet 31 |  | 12 | 2.75 | 5 |
| 2024 | Tecnam Astore | 2 | 12 | 0.0 | 0 |
| 2024 | Cirrus SR22 | 5 | 11 | 0.82 | 3 |
| 2024 | BRM Aero Bristell | 2 | 10 | 0.0 | 0 |
| 2024 | Cessna Citation Mustang (510) |  | 8 | 1.5 | 4 |
| 2024 | Cessna 172 | 4 | 8 | 0.25 | 1 |
| 2024 | Bombardier Challenger 604/605 |  | 8 | 5.63 | 10 |
| 2024 | Cessna Citation II/Bravo (550) |  | 8 | 5.38 | 6 |
| 2024 | Tecnam P92 | 2 | 8 | 0.0 | 0 |
| 2024 | Embraer Phenom 100 |  | 7 | 1.86 | 4 |
| 2024 | Tecnam P-Mentor | 2 | 7 | 0.0 | 0 |
| 2024 | Embraer Praetor 500 |  | 6 | 0.0 | 0 |
| 2024 | Beechcraft King Air 200/B200 |  | 6 | 3.5 | 7 |
| 2024 | Hawker 800XP |  | 6 | 3.0 | 4 |
| 2024 | Piper PA-28R Arrow | 4 | 6 | 0.5 | 2 |
| 2024 | Pipistrel Alpha Trainer | 2 | 6 | 0.0 | 0 |
| 2024 | Mooney M20 | 4 | 5 | 0.2 | 1 |
| 2024 | Cessna Citation V/Ultra/Encore (560) |  | 4 | 1.5 | 4 |
| 2024 | Cessna 208 Caravan |  | 4 | 0.0 | 0 |
| 2024 | Tecnam P2006T | 4 | 4 | 0.0 | 0 |
| 2024 | Cessna Citation Bravo (550B) |  | 4 | 3.5 | 5 |
| 2024 | Cessna Citation Excel/XLS (560XL) |  | 3 | 3.67 | 4 |
| 2024 | Cessna Citation I (500/501) |  | 3 | 4.33 | 6 |
| 2024 | Gulfstream IV/G400/G450 |  | 2 | 1.0 | 1 |
| 2024 | Beechcraft King Air 300 |  | 2 | 1.5 | 3 |
| 2024 | Tecnam P2008 | 2 | 2 | 0.0 | 0 |
| 2024 | Bombardier Challenger 300/350 |  | 2 | 3.0 | 3 |
| 2024 | Cessna Citation CJ2 (525A) |  | 2 | 3.0 | 3 |
| 2024 | Cessna Citation Sovereign (680) |  | 2 | 8.0 | 8 |
| 2024 | Piper PA-30/39 Twin Comanche | 4 | 2 | 1.0 | 1 |
| 2024 | Beechcraft Bonanza 33/35 | 5 | 1 | 0.0 | 0 |
| 2024 | Cirrus SR22T | 5 | 1 | 2.0 | 2 |
| 2024 | Aero Commander 690 |  | 1 | 2.0 | 2 |
| 2024 | Beechcraft King Air 350 (B300) |  | 1 | 5.0 | 5 |
| 2024 | Tecnam P2010 | 4 | 1 | 0.0 | 0 |
| 2024 | Piper PA-38 Tomahawk | 2 | 1 | 0.0 | 0 |
| 2024 | Cessna Citation CJ3 (525B) |  | 1 | 4.0 | 4 |
| 2025 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 77 | 1.16 | 7 |
| 2025 | Cessna 150 | 2 | 57 | 0.0 | 0 |
| 2025 | Tecnam P2002 Sierra | 2 | 54 | 0.0 | 0 |
| 2025 | Cessna 182 | 4 | 46 | 0.22 | 2 |
| 2025 | Learjet 60 |  | 30 | 2.97 | 7 |
| 2025 | Tecnam P2006T | 4 | 26 | 4.0 | 92 |
| 2025 | Cessna Citation II/SP (551) |  | 26 | 0.69 | 8 |
| 2025 | Cessna Citation CJ1/M2 (525) |  | 23 | 1.39 | 6 |
| 2025 | Cessna 152 | 2 | 21 | 0.0 | 0 |
| 2025 | Beechcraft King Air B200GT |  | 19 | 2.42 | 6 |
| 2025 | Cirrus SR22 | 5 | 18 | 0.28 | 2 |
| 2025 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 18 | 0.83 | 3 |
| 2025 | BRM Aero Bristell | 2 | 16 | 0.0 | 0 |
| 2025 | Cessna Citation V/Ultra/Encore (560) |  | 15 | 2.6 | 6 |
| 2025 | Cessna 208B Grand Caravan |  | 15 | 2.33 | 5 |
| 2025 | Beechcraft King Air 200/B200 |  | 13 | 3.46 | 8 |
| 2025 | Tecnam P92 | 2 | 13 | 0.08 | 1 |
| 2025 | HondaJet HA-420 |  | 12 | 1.17 | 5 |
| 2025 | Cessna Citation II/Bravo (550) |  | 12 | 2.67 | 5 |
| 2025 | Cessna 172 | 4 | 10 | 0.4 | 2 |
| 2025 | Piper M500 (PA-46-500TP) |  | 10 | 0.7 | 3 |
| 2025 | Learjet 45 |  | 9 | 3.11 | 10 |
| 2025 | Learjet 31 |  | 9 | 3.22 | 6 |
| 2025 | Tecnam Astore | 2 | 9 | 0.0 | 0 |
| 2025 | Cessna Citation Excel/XLS (560XL) |  | 7 | 2.71 | 7 |
| 2025 | Bombardier Challenger 604/605 |  | 7 | 2.0 | 6 |
| 2025 | Evektor Harmony LSA | 2 | 7 | 0.0 | 0 |
| 2025 | Hawker 800XP |  | 6 | 2.33 | 5 |
| 2025 | Beechcraft King Air 350 (B300) |  | 5 | 2.0 | 4 |
| 2025 | Learjet 35 |  | 5 | 5.4 | 9 |
| 2025 | Mooney M20 | 4 | 4 | 0.5 | 1 |
| 2025 | Piper PA-38 Tomahawk | 2 | 4 | 0.0 | 0 |
| 2025 | Beechcraft King Air 300 |  | 4 | 3.25 | 5 |
| 2025 | Tecnam P-Mentor | 2 | 3 | 0.0 | 0 |
| 2025 | Ultraliviano (Petrel/912) | 2 | 3 | 0.0 | 0 |
| 2025 | Piper PA-24 Comanche | 4 | 3 | 3.67 | 7 |
| 2025 | Gulfstream V |  | 2 | 3.5 | 7 |
| 2025 | Piper PA-23 Apache/Aztec | 5 | 2 | 1.0 | 2 |
| 2025 | Beechcraft Bonanza 33/35 | 5 | 2 | 1.0 | 2 |
| 2025 | Cessna Citation III/VI/VII (650) |  | 2 | 1.0 | 2 |
| 2025 | Cessna Citation Mustang (510) |  | 2 | 0.5 | 1 |
| 2025 | Piper PA-28R Arrow | 4 | 2 | 2.0 | 2 |
| 2025 | Embraer Legacy 600 |  | 2 | 1.0 | 2 |
| 2025 | Embraer Phenom 100 |  | 1 | 2.0 | 2 |
| 2025 | Airbus H125/AS350 |  | 1 | 0.0 | 0 |
| 2025 | Piper Cub (PA-11/12/18) | 2 | 1 | 0.0 | 0 |
| 2025 | Beechjet 400A |  | 1 | 1.0 | 1 |
| 2025 | Aero Commander 690 |  | 1 | 2.0 | 2 |
| 2025 | Cessna Citation Bravo (550B) |  | 1 | 3.0 | 3 |
| 2026 | Cessna 150 | 2 | 102 | 0.0 | 0 |
| 2026 | Beechcraft King Air 90 (C90/E90/A90/B90) |  | 80 | 1.13 | 6 |
| 2026 | Tecnam P2002 Sierra | 2 | 38 | 0.0 | 0 |
| 2026 | Cessna Citation CJ1/M2 (525) |  | 35 | 0.37 | 2 |
| 2026 | BRM Aero Bristell | 2 | 19 | 0.0 | 0 |
| 2026 | Learjet 60 |  | 19 | 2.32 | 7 |
| 2026 | Beechcraft King Air B200GT |  | 18 | 1.89 | 6 |
| 2026 | Cessna 182 | 4 | 16 | 0.0 | 0 |
| 2026 | Cirrus SR22 | 5 | 14 | 1.43 | 4 |
| 2026 | Cessna 152 | 2 | 14 | 0.0 | 0 |
| 2026 | Beechcraft King Air 200/B200 |  | 13 | 0.77 | 4 |
| 2026 | Airbus H125/AS350 |  | 12 | 0.25 | 3 |
| 2026 | Cessna Citation V/Ultra/Encore (560) |  | 12 | 2.58 | 7 |
| 2026 | Cessna Citation II/Bravo (550) |  | 12 | 3.25 | 7 |
| 2026 | Cessna 208B Grand Caravan |  | 12 | 1.5 | 8 |
| 2026 | Cessna 172 | 4 | 11 | 0.36 | 2 |
| 2026 | Tecnam P92 | 2 | 8 | 0.0 | 0 |
| 2026 | Tecnam Astore | 2 | 7 | 0.0 | 0 |
| 2026 | Piper PA-28 Cherokee/Warrior/Archer | 4 | 6 | 1.0 | 2 |
| 2026 | Cirrus SF50 Vision Jet |  | 4 | 0.5 | 2 |
| 2026 | Cessna Citation I (500/501) |  | 4 | 2.75 | 5 |
| 2026 | Cessna Citation Excel/XLS (560XL) |  | 3 | 0.0 | 0 |
| 2026 | Tecnam P2006T | 4 | 3 | 0.33 | 1 |
| 2026 | Tecnam P2008 | 2 | 3 | 0.0 | 0 |
| 2026 | Piper PA-28R Arrow | 4 | 3 | 1.0 | 2 |
| 2026 | Learjet 45 |  | 3 | 3.67 | 8 |
| 2026 | Cessna Citation Mustang (510) |  | 2 | 1.5 | 3 |
| 2026 | Cessna Citation Sovereign (680) |  | 2 | 0.0 | 0 |
| 2026 | Cessna 188 AgWagon | 1 | 2 | 0.0 | 0 |
| 2026 | Cessna Citation II/SP (551) |  | 2 | 0.0 | 0 |
| 2026 | Rans S-6S Coyote II | 2 | 2 | 0.0 | 0 |
| 2026 | Cessna 180 | 4 | 2 | 1.0 | 1 |
| 2026 | Gulfstream G550 |  | 2 | 3.0 | 4 |
| 2026 | Embraer Phenom 100 |  | 2 | 1.0 | 1 |
| 2026 | Rans S-19 Venterra | 2 | 1 | 0.0 | 0 |
| 2026 | Learjet 35 |  | 1 | 2.0 | 2 |
| 2026 | Mooney M20 | 4 | 1 | 0.0 | 0 |
| 2026 | Embraer Legacy 600 |  | 1 | 0.0 | 0 |
| 2026 | Tecnam P-Mentor | 2 | 1 | 0.0 | 0 |
| 2026 | Piper PA-30/39 Twin Comanche | 4 | 1 | 1.0 | 1 |
| 2026 | Cessna Citation CJ2 (525A) |  | 1 | 0.0 | 0 |

## 5. Modelos estandarizados: denominaciones ANAC por modelo (foco)

| aeronave_modelo | aeronave_icao | denominaciones | como_figura_en_anac | movimientos |
|---|---|---|---|---|
| Embraer E190 | E190 | 1 | EMB-ERJ190100IGW | 15097 |
| Boeing 737-800 | B738 | 19 | BO-737-85F · BO-737-8Q8 · BO-737-8U3 · BO-B-737-81D · BO-737-8BK · BO-B737-8SH · BO-B737-81D · BO-737-8SH · BO-737-81D · BO-737-86N · BO-B737-8MB · BO-B737-8BK · BO-B737-800 · BO-B737-86J · BO-737-800 · BO-737-8HX · BO-B737-8LP · BO-737-8GJ · BO-737-86J | 3231 |
| Cessna 150 | C150 | 13 | CE-150-L · CE-150-K · CE-150 · CE-150-H · CE-A-150-L · CE-C-150-L · CE-150-A · CE-150-M · CE-150-J · CE-150-G · CE-150-F · CE-AA-150-L · CE-150-E | 2431 |
| Boeing 737-700 | B737 | 6 | BO-B-737-76N · BO-737-76N · BO-737-7BD · BO-B-737-7BD · BO-B-737-700 · BO-737-7K2 | 1486 |
| Tecnam P2002 Sierra |  | 7 | TEA-P2002 SIERRA · TEA-P2002 LSA · TEA-P2002-JF · TEA-P2002JF · TEA-P2002 SIERRA MK2 · TEA-P2002 · TEA-P2002 SIERRA MKII | 1261 |
| Cessna 152 | C152 | 4 | CE-152-II · CE-152 · CE-C-152 · CE-152-A | 1048 |
| Learjet 60 | LJ60 | 2 | LJ-60 · LJ-60-XR | 771 |
| Beechcraft King Air 90 (C90/E90/A90/B90) | BE9L | 12 | BE-C90GT · RAY-C-90-GT · BE-65-A-90 · HAB-C-90-A · BE-C-90-A · RAY-C90A · BE-C-90-GTI · BE-E-90 · BE-C-90 · BE-90-A · BE-C90GTI · BE-C-90-B | 769 |
| Boeing 737 MAX 8 | B38M | 4 | BO-B737-8MAX · BO-737-8 MAX · BO-737-8 · BO-B737-8 | 738 |
| Cessna 182 | C182 | 16 | CE-182-C · CE-182-E · CE-182-B · CE-182-R · CE-182-T · CE-182-A · CE-A-182-K · CE-A-182-J · CE-T182T · CE-182-D · CE-182 · TXA-182T · CE-A-182-N · CE-182-F · CE-182-P · CE-182-G | 714 |
| ATR 72 |  | 1 | ATR-ATR72-212A | 677 |
| Tecnam P92 |  | 6 | TEA-P92 ECHO CLA · TEA-P92 ECHO MKII · TEA-P92 MKII · TEA-P92 EAGLET · TEA-P92 EAGLET G5 · TEA-P92-JS | 543 |
| BRM Aero Bristell |  | 4 | BRT-LSA · BRT-BRISTELL S-LSA · BRT-BRISTELL LSA · AV1-BRISTELL CLASSIC | 533 |
| Piper PA-28 Cherokee/Warrior/Archer | P28A | 11 | PAA-PA-A-28-181 · PA-PA-28-180 · PAA-PA-A-28-140 · PA-PA-28-180-D · PA-PA-28-140 · PA-PA-28-161 · PA-PA-28 · PAA-PA-A-28-180 · PA-PA-28-181 · PAA-PA-A-28-236 · PA-PA-28-235 | 415 |
| Cessna 208B Grand Caravan | C208 | 2 | TXA-208B · CE-208-B | 370 |
| Piper M500 (PA-46-500TP) | P46T | 2 | PAA-PA 46-500TP · PA-PA-46-500TP | 320 |
| Cessna Citation CJ1/M2 (525) | C525 | 2 | CE-525 · TXA-525 | 291 |
| Beechcraft Baron 58 | BE58 | 8 | BE-58 · BE-BARON 58 · TXA-58 · BE-58-P · HAB-G-58 · BEF-58 · BE-58-TC · BE-G58 | 288 |
| Cessna 172 | C172 | 18 | CE-172-S · CE-172-C · CE-172-M · CE-172-N · CE-172-H · CE-172-P · CE-A172N · CE-172 · CE-R-172-K · CE-172-RG · CE-172-B · CE-172RG · CE-172-L · CE-C-172-L · CE-R-172-G · CE-172-A · CE-172-E · CE-C-172-M | 277 |
| Airbus H125/AS350 | AS50 | 3 | ARH-AS-350-B3 · EUR-AS-350-B3 · ECU-AS-350-B3 | 263 |
| Piper PA-31 Navajo | PA31 | 7 | PA-PA-31 · PAA-PA-A-31-350 · PA-PA-31-325 · PAA-PA-A-31-325 · PAA-PA-A-31-310 · PA-PA-31P-350 · PA-PA-31-350 | 261 |
| Cessna Citation II/Bravo (550) | C550 | 1 | CE-550 | 259 |
| Beechcraft King Air 200/B200 | BE20 | 3 | BE-B-200 · BE-200 · TXA-B200 | 250 |
| Cessna Citation V/Ultra/Encore (560) | C560 | 1 | CE-560 | 245 |
| Beechcraft King Air B200GT | BE20 | 4 | BE-B-200-GT · HAB-B-200-GT · BEF-B200GT · TXA-B200GT | 242 |
| Learjet 45 | LJ45 | 2 | LJ-LJ45 · LJ-45 | 234 |
| Piper PA-34 Seneca | PA34 | 3 | PA-PA-34-200-T · PAA-PA-A-34-200T · PA-PA-34-200 | 226 |
| Piper PA-46 Malibu/Mirage | PA46 | 4 | PA-PA-46-350-P · PA-PA-46-350T · PA-PA-46R-350T · PA-PA-46R-350 | 223 |
| Cessna Citation Excel/XLS (560XL) | C56X | 3 | TXA-560XL · CE-560-XI · CE-560-XL | 217 |
| Piper PA-38 Tomahawk | PA38 | 2 | PAA-PA-A-38-112 · PA-PA-38-112 | 213 |
| Cirrus SR22 | SR22 | 2 | CIR-SR-22 · CIT-SR22 | 208 |
| Piper PA-28R Arrow | P28R | 7 | PAA-PA-A-28R201T · PA-PA-28R-200 · PA-PA-28-R-201T · PAA-PA-A-28-R201 · PAA-PA-A-28-R200 · PA-PA-28R-180 · PA-PA-28-200R | 206 |
| Tecnam P2006T |  | 1 | TEA-P2006T | 199 |
| Airbus AS365 Dauphin | AS65 | 1 | EUR-AS-365-N2 | 195 |
| Learjet 31 | LJ31 | 2 | LJ-31-A · LJ-31 | 188 |
| Airbus/MBB BK117/H145 |  | 6 | ARH-MBB-BK117 D-2 · ARH-MBB-BK117 C2 · EUR-EC-145 · EUR-MBB-BK-117C2 · EUR-MBB-BK-117C1 · ADG-MBB-BK-117C2 | 142 |
| Tecnam Astore |  | 1 | TEA-ASTORE | 140 |
| Beechcraft Baron 55 | BE55 | 5 | TXA-95-B55 · BE-E55 · BE-BARON B-55 · BE-BARON E-55 · BE-95-B55 | 134 |
| Beechcraft Bonanza 36 | BE36 | 10 | BE-A-36 · BEF-A36 · MT-MU-2B-36-A · BE-36 · TXA-G36 · BE-B-36-TC · BE-36 B 36TC · TXA-A-36 · BE-A36 · BE-G36 | 130 |
| Cessna Citation II/SP (551) | C551 | 2 | CE-551 · CE-551-CITATION | 128 |

## 6. Validación contra OpenSky (matrícula → tipo ICAO, todo el país)

Coincidencia del designador ICAO asignado por las reglas con el de OpenSky:

| matriculas | coinciden | pct_coinciden |
|---|---|---|
| 562 | 534 | 95.0 |

Discrepancias (revisar regla o dato de OpenSky):

| aeronave | aeronave_modelo | aeronave_icao | icao_opensky | modelo_opensky | matriculas | ejemplo |
|---|---|---|---|---|---|---|
| CE-550 | Cessna Citation II/Bravo (550) | C550 | C55B | Citation Bravo | 3 | LV-BEU |
| TXA-525 | Cessna Citation CJ1/M2 (525) | C525 | C25M | Citation M2 | 2 | LV-GMQ |
| LJ-45 | Learjet 45 | LJ45 | LJ40 | Learjet 40 XR | 2 | LV-CJY |
| CE-T-210-N | Cessna T210 | T210 | C210 |  | 2 | LV-GQC |
| CE-500 | Cessna Citation I (500/501) | C501 | C500 | Citation I | 2 | LV-BID |
| LJ-45 | Learjet 45 | LJ45 | LJ75 |  | 2 | LQ-IJK |
| BE-A-36 | Beechcraft Bonanza 36 | BE36 | BT36 |  | 1 | LV-CDB |
| BOM-BD-100-1A10 | Bombardier Challenger 300/350 | CL30 | CL35 | Challenger 350 | 1 | LV-HAT |
| CIR-SR 22T | Cirrus SR22T | S22T | SR22 |  | 1 | LV-IVV |
| CE-R-172-G | Cessna 172 | C172 | C72R |  | 1 | LV-APA |
| BE-36 | Beechcraft Bonanza 36 | BE36 | BT36 |  | 1 | LV-CNH |
| TXA-G36 | Beechcraft Bonanza 36 | BE36 | BE33 |  | 1 | LV-JUC |
| LAN-L2KC LEGACY | Embraer Legacy 600 | E35L | LEG2 |  | 1 | LV-X544 |
| CE-152 | Cessna 152 | C152 | C150 |  | 1 | LV-IWB |
| TXA-T206H | Cessna T206 | T206 | C206 |  | 1 | LV-JKN |
| LJ-45 | Learjet 45 | LJ45 | LJ40 | Learjet 40 | 1 | LQ-BFS |
| CE-500 | Cessna Citation I (500/501) | C501 | C500 | Cessna Citation I | 1 | LV-BPW |
| CE-525 | Cessna Citation CJ1/M2 (525) | C525 | C25M | Citation M2 | 1 | LV-GUL |
| RO-R66 | Robinson R66 | R66 | AT76 | ATR 72 600 | 1 | LV-GUI |
| RO-R-44RAVEN-II | Robinson R44 | R44 | R66 |  | 1 | LV-JWU |
| BOM-BD-700-1A11 | Bombardier Global Express | GLEX | GL5T | Global 5000 | 1 | LV-GQE |

Tipos ICAO sugeridos por OpenSky para modelos sin designador:

| aeronave_modelo | icao_opensky | matriculas |
|---|---|---|
| Tecnam P2002 Sierra | SIRA | 23 |
| Tecnam P92 | ECHO | 10 |
| Tecnam P2006T | P06T | 5 |
| Piper Cheyenne (PA-31T/42) | PAY2 | 4 |
| Aero Commander 690 | AC90 | 3 |
| BRM Aero Bristell | NG5 | 3 |
| Piper Cheyenne (PA-31T/42) | PAY1 | 3 |
| Tecnam Astore | ASTO | 3 |
| Airbus/MBB BK117/H145 | EC45 | 3 |
| Beechcraft Bonanza 33/35 | BE35 | 2 |
| Aeronca 7EC Champion | CH7A | 2 |
| Piper PA-32 Saratoga/Lance | PA32 | 2 |
| Piper PA-32 Saratoga/Lance | P32T | 2 |
| Tecnam P2010 | TWEN | 2 |
| Learjet 25 | LJ25 | 2 |
| Air Tractor AT-802 | AT8T | 2 |
| Mooney M20 | M20T | 1 |
| Otra | UH1 | 1 |
| Mooney M20 | M20P | 1 |
| Piper Aerostar 600/601 | AEST | 1 |
| Air Tractor AT-401/402 | AT3T | 1 |
| Tecnam P2012 Traveller | P212 | 1 |
| Cessna 177 | C177 | 1 |
| Otra | GLID | 1 |
| Bell | B222 | 1 |
| Petrolini El Boyero | ZZZZ | 1 |
| Piper Cub (PA-11/12/18) | PA11 | 1 |
| Piper PA-22 Tri-Pacer | PA22 | 1 |
| Cessna TTx (T240) | C240 | 1 |
| Tecnam P2008 | P208 | 1 |

## 7. MADHEL (datos.anac.gob.ar/madhel/api/v2/airports/)

Registros: 712

Columnas:

| column_name | column_type |
|---|---|
| uri | VARCHAR |
| the_geom | STRUCT(geometry STRUCT("type" VARCHAR, coordinates DOUBLE[]), properties STRUCT("name" VARCHAR, gg_point_coordinates DOUBLE[]), "type" VARCHAR) |
| updated_at | TIMESTAMP WITH TIME ZONE |
| human_readable_identifier | VARCHAR |
| local_identifier | VARCHAR |
| pdf_share | VARCHAR |

Primeras filas:

| uri | the_geom | updated_at | human_readable_identifier | local_identifier | pdf_share |
|---|---|---|---|---|---|
| /madhel/api/v2/airports/ACB/?format=json | {'geometry': {'type': Point, 'coordinates': [-60.57066, -33.27226]}, 'properties': {'name': 'CORONEL BOGADO / AGROSERVICIOS - (ACB) - DRCE - PRIVADO NO CONTROLADO [** USO AGROAÉREO **]', 'gg_point_coordinates': [-33.27226, -60.57066]}, 'type': Feature} | 2026-06-01 09:41:51+00 | CORONEL BOGADO / AGROSERVICIOS - (ACB) - DRCE - PRIVADO NO CONTROLADO [** USO AGROAÉREO **] | ACB | /madhel/api/v2/airports/ACB/pdf?format=json |
| /madhel/api/v2/airports/ACH/?format=json | {'geometry': {'type': Point, 'coordinates': [-64.61351, -37.40164]}, 'properties': {'name': 'GENERAL ACHA - (ACH / SAEA) - DRCE - PÚBLICO NO CONTROLADO', 'gg_point_coordinates': [-37.40164, -64.61351]}, 'type': Feature} | 2026-06-01 16:04:20+00 | GENERAL ACHA - (ACH / SAEA) - DRCE - PÚBLICO NO CONTROLADO | ACH | /madhel/api/v2/airports/ACH/pdf?format=json |
| /madhel/api/v2/airports/ACM/?format=json | {'geometry': {'type': Point, 'coordinates': [-60.1417, -34.07574]}, 'properties': {'name': 'ARRECIFES / LA CURA MALAL - (ACM) - DRCE - PRIVADO NO CONTROLADO', 'gg_point_coordinates': [-34.07574, -60.1417]}, 'type': Feature} | 2025-10-06 10:02:51+00 | ARRECIFES / LA CURA MALAL - (ACM) - DRCE - PRIVADO NO CONTROLADO | ACM | /madhel/api/v2/airports/ACM/pdf?format=json |

Códigos numéricos del CSV de movimientos encontrados en MADHEL:

| codigo | movimientos | registro_madhel |
|---|---|---|

