# Auditoría de datos faltantes

Qué falta, qué se puede recuperar con cruces exactos y qué haría falta para el resto.

## 1. Completitud por año

País:

| anio | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_matricula | pct_sin_pasajeros | pct_sin_hora | pct_sin_od | pct_od_lad |
|---|---|---|---|---|---|---|---|---|
| 2019 | 580749 | 31.4 | 98.8 | 100.0 | 0.0 | 0.0 | 0.0 | 0.9 |
| 2020 | 212686 | 48.6 | 85.1 | 100.0 | 0.0 | 0.0 | 0.0 | 1.1 |
| 2021 | 329800 | 54.3 | 14.0 | 100.0 | 0.0 | 0.0 | 0.0 | 1.2 |
| 2022 | 477930 | 38.3 | 15.3 | 100.0 | 0.0 | 0.0 | 0.0 | 1.3 |
| 2023 | 557168 | 33.1 | 15.6 | 100.0 | 0.0 | 0.0 | 0.0 | 1.3 |
| 2024 | 578592 | 36.5 | 17.0 | 100.0 | 0.0 | 0.0 | 0.0 | 1.6 |
| 2025 | 597783 | 33.6 | 22.7 | 100.0 | 0.0 | 0.0 | 0.0 | 1.6 |
| 2026 | 419199 | 31.9 | 26.2 | 0.0 | 0.0 | 0.0 | 0.0 | 1.6 |

Foco (MDQ):

| anio | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_matricula | pct_sin_pasajeros | pct_sin_hora | pct_sin_od | pct_od_lad |
|---|---|---|---|---|---|---|---|---|
| 2019 | 8388 | 32.1 | 15.5 | 100.0 | 0.0 | 0.0 | 0.0 | 0.2 |
| 2020 | 3022 | 50.6 | 68.7 | 100.0 | 0.0 | 0.0 | 0.0 | 0.2 |
| 2021 | 3957 | 66.0 | 15.8 | 100.0 | 0.0 | 0.0 | 0.0 | 0.9 |
| 2022 | 6387 | 49.9 | 15.1 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2023 | 7571 | 47.2 | 19.2 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2024 | 7530 | 48.3 | 25.2 | 100.0 | 0.0 | 0.0 | 0.0 | 0.3 |
| 2025 | 6825 | 48.4 | 18.4 | 100.0 | 0.0 | 0.0 | 0.0 | 0.4 |
| 2026 | 4455 | 47.3 | 6.7 | 0.0 | 0.0 | 0.0 | 0.0 | 2.2 |

Foco 2021+, por segmento:

| segmento | movimientos | pct_sin_operador | pct_sin_aeronave | pct_sin_pasajeros |
|---|---|---|---|---|
| linea_regular | 15665 | 0.3 | 1.7 | 0.0 |
| privado | 6587 | 92.0 | 7.4 | 0.0 |
| oficial | 6265 | 85.7 | 82.7 | 0.0 |
| taxi_aereo | 5055 | 88.4 | 6.3 | 0.0 |
| instruccion | 2659 | 89.7 | 0.2 | 0.0 |
| charter_linea | 475 | 18.5 | 49.9 | 0.0 |
| trabajo_aereo | 19 | 100.0 | 0.0 | 0.0 |

## 2A. Operador por matrícula

| ambito | faltan_con_matricula | recuperables_unanime | matricula_con_algun_dato |
|---|---|---|---|
| MDQ | 2109 | 431 | 824 |
| resto del país | 131409 | 20229 | 42853 |

Foco, por segmento:

| segmento | faltan_con_matricula | recuperables_unanime |
|---|---|---|
| privado | 753 | 28 |
| oficial | 589 | 161 |
| taxi_aereo | 475 | 53 |
| instruccion | 286 | 186 |
| charter_linea | 4 | 2 |
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
| RADIAL 340 S.A.S.- CIAC TIPO II | 10 |
| TWR SRL | 10 |
| PRESIDENCIA DE LA NACION | 10 |
| FLIGHT CENTER- TWR S.R.L-CIAC TIPO III | 9 |

## 2B. Aeronave por matrícula

| ambito | faltan_con_matricula | recuperables_unanime | matricula_con_algun_dato |
|---|---|---|---|
| MDQ | 299 | 0 | 0 |
| resto del país | 109676 | 0 | 0 |

Foco, por segmento:

| segmento | faltan_con_matricula | recuperables_unanime |
|---|---|---|
| oficial | 215 | 0 |
| privado | 41 | 0 |
| taxi_aereo | 21 | 0 |
| charter_linea | 12 | 0 |
| linea_regular | 10 | 0 |

Qué se recupera (foco, top 12):

| valor_recuperado | movimientos |
|---|---|


Comparación con la regla vigente (operador con >= 80 % de consistencia):

| operador_inferido_80 | en_foco |
|---|---|
| 51611 | 1552 |

Aeronave faltante con matrícula presente en OpenSky (registro externo):

| faltan_con_matricula | con_tipo_en_opensky | en_foco |
|---|---|---|
| 109975 | 0 | 0 |

## 2C. El otro extremo del mismo vuelo (por matrícula, un solo candidato)

| ambito | movimientos_con_par_unico | operador_recuperable | aeronave_recuperable | pasajeros_recuperables | aeronave_distinta_en_cada_extremo |
|---|---|---|---|---|---|
| MDQ | 2646 | 38 | 0 | 0 | 0 |
| resto del país | 195792 | 1154 | 0 | 0 | 0 |

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

Validación cruzada: familia de la ANAC 2019 versión anterior contra el portal municipal en los mismos vuelos (1 a 1):

| familia_previa | familia_municipal | vuelos |
|---|---|---|
| Embraer E190 | Embraer E190 | 1209 |
| Boeing 737 | Boeing 737 | 138 |

### ANAC 2019 versión anterior ↔ vigente: diagnóstico de claves

Para cada registro de la versión anterior, el de la vigente más cercano en hora (mismo día, aeropuerto, movimiento y origen/destino): diferencia en minutos y si coinciden los pasajeros.

| dif_min | registros | pax_iguales | con_aeronave |
|---|---|---|---|
| 0 | 7670 | 2194 | 6415 |
| otro | 584 | 110 | 540 |
| ±5 | 133 | 3 | 132 |
| -180 | 2 | 0 | 1 |

Registros de la versión anterior sin ningún candidato el mismo día: 

| registros_version_anterior | registros_vigente |
|---|---|
| 8389 | 8387 |

## 2E. El otro extremo del mismo vuelo sin matrícula (2019–2025)

Validación en el foco (vuelos no regulares con operador y avión informados; se esconde uno y se recupera del otro extremo):

| dato | recuperados | coinciden | pct_coinciden |
|---|---|---|---|
| aeronave | 476 | 457 | 96.0 |
| operador | 412 | 407 | 98.8 |

## 2G. Operador por la consulta de Afectación de ANAC

Validación: movimientos con operador informado por ANAC cuya matrícula figura afectada (a una sola empresa, vuelo posterior a la afectación).

| ambito | movimientos | coinciden | pct |
|---|---|---|---|
| MDQ | 1910 | 1909 | 99.9 |
| resto del país | 172133 | 171968 | 99.9 |

Desacuerdos más frecuentes (operador ANAC ≠ empresa afectada):

| operador_anac | empresa_afectada | movimientos |
|---|---|---|
| JUST FLIGHT S.A. "ROYAL CLASS" | VOLAR S.A. | 108 |
| DIGITAL AIR TAXI S.A. | FEELING AIR S.A. | 26 |
| HANGAR UNO S.A- CIAC TIPO II | HANGAR UNO S.A. | 6 |
| JUST FLIGHT S.A. "ROYAL CLASS" | PRIVATE AVIATION CONSULTING S.A. | 3 |
| SERV. Y EMPRENDIMIENTOS AERONÁUTICOS S.A | SERV. EMPRENDIM. AERON. S.A. (FLYZAR) | 2 |
| SEA CO AVIATION | SERV. EMPRENDIM. AERON. S.A. (FLYZAR) | 2 |
| SERV AEREOS SUDAMERICANOS S.A. | SERV. EMPRENDIM. AERON. S.A. (FLYZAR) | 2 |
| CICA | AEROTEC ARGENTINA S.A. | 2 |
| SAPSA | SERV. AER. PATAGONICOS S.A. | 1 |
| BAIRES FLY SA | SERV. EMPRENDIM. AERON. S.A. (FLYZAR) | 1 |

## 2F. Aeronaves del Estado: operador por prefijo de la identificación (2026)

Contrastación con los vuelos que traen operador en ANAC. Los desacuerdos son casi todos ANAC cargando "Fuerza Aérea" en aeronaves de otra fuerza (ej. 1-G-49 Huron de la Armada, PA-40 Dauphin de Prefectura, identificados en fuentes públicas).

| patron | regla | movimientos | con_operador_anac | coinciden | completados | completados_foco |
|---|---|---|---|---|---|---|
| ^(C|M|A|T|H|E|ET|F|VR|V|TC)[0-9]+$ | FUERZA AEREA ARGENTINA | 10468 | 4997 | 4955 | 5471 | 65 |
| ^PA[0-9]+$ | PREFECTURA NAVAL ARGENTINA | 1552 | 32 | 25 | 1520 | 271 |
| ^[0-9][A-Z][0-9]+$ | ARMADA ARGENTINA | 1245 | 15 | 0 | 1230 | 56 |
| ^PG[0-9]+$ | FUERZA AEREA ARGENTINA | 1176 | 194 | 193 | 982 | 32 |
| ^AE[0-9]+$ | EJERCITO ARGENTINO | 779 | 739 | 733 | 40 | 0 |
| ^GN[0-9]+$ | GENDARMERIA NACIONAL ARGENTINA | 206 | 27 | 25 | 179 | 2 |
| ^PF[0-9]+$ | POLICIA FEDERAL ARGENTINA | 99 | 28 | 22 | 71 | 2 |

Modelo por serie con identificación pública (config/estatales.yaml → series):

| serie | aeronave_modelo | movimientos | en_foco |
|---|---|---|---|
| T94 | Embraer ERJ-140 | 564 | 94 |
| T99 | Boeing 737-700 | 464 | 86 |
| TC53 | Fokker F28/F100 | 337 | 42 |
| PA25 | Beechcraft King Air 350 (B300) | 284 | 10 |
| T95 | Embraer ERJ-140 | 256 | 22 |
| PA40 | Airbus AS365 Dauphin | 202 | 111 |
| PA41 | Airbus AS365 Dauphin | 171 | 34 |
| PA22 | Beechcraft King Air 350 (B300) | 144 | 29 |
| PA43 | Airbus AS365 Dauphin | 130 | 50 |
| TC66 | Lockheed C-130 Hercules | 123 | 4 |
| TC64 | Lockheed C-130 Hercules | 64 | 2 |
| PG380 | Cessna 180 | 63 | 32 |

## 4. Aplicado en la base (fct_movimiento)

| ambito | operador_por_matricula | operador_por_otro_extremo | operador_por_prefijo_estatal | operador_otro_extremo_sin_matricula | operador_anac_version_anterior | operador_afectacion_anac | aeronave_anac_version_anterior | aeronave_del_municipio | aeronave_por_serie_estatal | aeronave_otro_extremo_sin_matricula | aeronave_por_asientos_yvera |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MDQ | 383 | 22 | 319 | 643 | 0 | 185 | 7079 | 9 | 516 | 6 | 414 |
| resto del país | 17074 | 456 | 6387 | 11571 | 0 | 14571 | 0 | 0 | 2286 | 245 | 0 |

Privado en jet o turbohélice ejecutivo analizado como taxi aéreo. Evidencia en el foco: cuántos tienen operador o matrícula que también vuela como no regular.

| anio | pasan_a_taxi | con_operador_o_matricula | que_tambien_hacen_taxi |
|---|---|---|---|
| 2019 | 177 | 15 | 15 |
| 2020 | 33 | 0 | 0 |
| 2021 | 216 | 20 | 20 |
| 2022 | 420 | 39 | 39 |
| 2023 | 475 | 47 | 47 |
| 2024 | 348 | 19 | 19 |
| 2025 | 316 | 13 | 13 |
| 2026 | 228 | 228 | 225 |

Asientos: cabina publicada (config/cabinas.yaml) contra el p95 de pasajeros observados:

| aerolinea_nombre | aeronave_modelo | publicados | p95_observado | movimientos_pais | con_mas_pax_que_asientos |
|---|---|---|---|---|---|
| Aerolíneas Argentinas | Boeing 737-800 | 170.0 | 171.0 | 409696 | 30310 |
| Aerolíneas Argentinas | Embraer E190 | 96.0 | 97.0 | 382369 | 20164 |
| Flybondi | Boeing 737-800 | 189.0 | 190.0 | 172854 | 9439 |
| Aerolíneas Argentinas | Boeing 737 MAX 8 | 170.0 | 173.0 | 117103 | 9546 |
| American Jet | Embraer ERJ-145 | 50.0 | 50.0 | 5546 | 125 |
| Andes Líneas Aéreas | Boeing 737-700 | 142.0 | 142.0 | 1404 | 0 |
| Avian (Avianca Argentina) | ATR 72 | 72.0 |  | 599 | 16 |
| LADE | Embraer ERJ-140 | 44.0 |  | 230 | 0 |
| Fuerza Aérea Argentina | Embraer ERJ-140 | 44.0 |  | 28 | 0 |
| Flyest S.A. Líneas Aéreas | Bombardier CRJ200 | 50.0 |  | 11 | 0 |
| Norwegian Argentina | Boeing 737-800 | 189.0 |  | 7 | 0 |
| JetSMART | Embraer ERJ-145 | 50.0 |  | 3 | 3 |
| Andes Líneas Aéreas | Embraer ERJ-145 | 50.0 |  | 2 | 1 |
| Aerolíneas Argentinas | Embraer ERJ-145 | 50.0 |  | 2 | 2 |
| Aerovias De Mexico - Aeromexico | Embraer ERJ-145 | 50.0 |  | 1 | 0 |
| Sky Airline | Embraer ERJ-145 | 50.0 |  | 1 | 1 |
| Flying America | Embraer ERJ-145 | 50.0 |  | 1 | 0 |
| Bocca Jorge Luis Roque | Bombardier CRJ200 | 50.0 |  | 1 | 0 |

Validación: qué habría dicho la inferencia por pasajeros en los vuelos 2019 del foco cuyo avión se recuperó (ANAC versión anterior o portal municipal):

| inferida | real | vuelos | pct |
|---|---|---|---|
| ATR 42/72 | ATR 42/72 | 661 | 100.0 |
| Boeing 737 | Boeing 737 | 138 | 100.0 |
| Bombardier CRJ | Bombardier CRJ | 13 | 100.0 |
| Embraer E190 | Embraer E190 | 4083 | 98.2 |
| Embraer E190 | Boeing 737 | 76 | 1.8 |

## 5. Yvera, base agregada de frecuencias (validación y asientos)

Mismo origen (SIAC/ANAC): coincidir prueba consistencia de procesamiento, no exactitud de la carga. Vuelos y pasajeros por año contra los movimientos regulares y no regulares del foco:

| anio | vuelos_yvera | movimientos_anac | pasajeros_yvera | pasajeros_anac | asientos_yvera | asientos_estimados |
|---|---|---|---|---|---|---|
| 2017 | 3709 |  | 277561 |  | 350401 |  |
| 2018 | 6785 |  | 454287 |  | 596926 |  |
| 2019 | 5418 | 6323 | 382751 | 376692 | 513318 | 515825.0 |
| 2020 | 1373 | 1767 | 110516 | 110828 | 140923 | 50686.0 |
| 2021 | 1168 | 1858 | 85114 | 85191 | 114222 | 115711.0 |
| 2022 | 2901 | 3702 | 275655 | 269660 | 352247 | 352389.0 |
| 2023 | 3790 | 4522 | 310470 | 305089 | 403475 | 400809.0 |
| 2024 | 3464 | 4109 | 295199 | 289341 | 367775 | 364031.0 |
| 2025 | 3229 | 3958 | 298644 | 296491 | 351522 | 344693.0 |
| 2026 | 1834 | 2503 | 168418 | 200584 | 199475 | 236084.0 |

Asientos del vuelo exacto (Yvera, 1 a 1) contra la cabina publicada / p95 que se usaría sin Yvera:

| aerolinea_nombre | aeronave_modelo | vuelos | asientos_yvera | cabina_config | coinciden_con_cabina |
|---|---|---|---|---|---|
| Aerolíneas Argentinas | Embraer E190 | 2999 | 96.0 | 96.0 | 2996 |
| Aerolíneas Argentinas | Boeing 737-800 | 175 | 170.0 | 170.0 | 175 |
| Aerolíneas Argentinas | Boeing 737-700 | 92 | 130.7 |  | 0 |
| Avian (Avianca Argentina) | ATR 72 | 78 | 72.0 | 72.0 | 78 |
| Aerolíneas Argentinas | Boeing 737 MAX 8 | 39 | 171.5 | 170.0 | 36 |
| LADE |  | 37 | 33.1 |  | 0 |
| Andes Líneas Aéreas | Boeing 737-800 | 29 | 176.0 |  | 0 |
| Flybondi | Boeing 737-800 | 19 | 189.0 | 189.0 | 19 |
| Aerolíneas Argentinas | Boeing 737 | 19 | 170.0 |  | 0 |
| LADE | Embraer ERJ-140 | 9 | 31.8 | 44.0 | 4 |
| LADE | Boeing 737-700 | 5 | 99.0 |  | 0 |
| Flyest S.A. Líneas Aéreas |  | 3 | 50.0 |  | 0 |
| Aerolíneas Argentinas | Lockheed L-18 Lodestar | 2 | 89.5 |  | 0 |
| Flyest S.A. Líneas Aéreas | Bombardier CRJ200 | 2 | 50.0 | 50.0 | 2 |
| Sin dato | Embraer Phenom 100 | 1 | 33.0 |  | 0 |
| Just Flight S.A. "Royal Class" | Cessna Citation CJ1/M2 (525) | 1 | 30.0 |  | 0 |
| Aerolíneas Argentinas | Cessna 150 | 1 | 92.0 |  | 0 |

Aeronave por asientos: reglas aprendidas (operador + asientos → modelo o familia, >= 98 % de al menos 20 vuelos con aeronave informada):

| operador | asientos | nivel | valor | vuelos_que_cumplen | vuelos_con_esos_asientos | pct |
|---|---|---|---|---|---|---|
| Aerolíneas Argentinas | 96 | modelo | Embraer E190 | 2187 | 2187 | 100.0 |
| Aerolíneas Argentinas | 170 | familia | Boeing 737 | 173 | 173 | 100.0 |
| Aerolíneas Argentinas | 128 | modelo | Boeing 737-700 | 46 | 46 | 100.0 |
| Flybondi | 189 | modelo | Boeing 737-800 | 28 | 28 | 100.0 |
| Andes Líneas Aéreas | 189 | modelo | Boeing 737-800 | 26 | 26 | 100.0 |
| Aerolíneas Argentinas | 137 | modelo | Boeing 737-700 | 22 | 22 | 100.0 |

Aplicadas en el foco (vuelos sin aeronave):

| anio | metodo | aeronave_familia | aeronave_modelo | movimientos |
|---|---|---|---|---|
| 2019 | dia | Embraer E190 | Embraer E190 | 1 |
| 2020 | vuelo | Embraer E190 | Embraer E190 | 268 |
| 2020 | dia | Embraer E190 | Embraer E190 | 80 |
| 2020 | vuelo | Boeing 737 | Boeing 737 | 19 |
| 2020 | vuelo | Boeing 737 | Boeing 737-700 | 5 |

## 3. Sin cruce posible con las fuentes actuales

| caso | movimientos_foco |
|---|---|
| Aeronave sin matrícula (2019–2025) | 9574 |
| Operador sin matrícula (2019–2025) | 20536 |
| Origen/destino en lugar apto denunciado (sin coordenadas) | 266 |
| Pasajeros sin dato | 0 |

Muestra (foco, 2 por segmento): operador sin dato y sin matrícula:

| segmento | fecha | hora_utc | tipo_movimiento | origen_destino | clase_vuelo | aeronave_modelo | pasajeros |
|---|---|---|---|---|---|---|---|
| charter_linea | 2024-02-11 | 10:21:00 | aterrizaje | FDO | no_regular | Fairchild Metro III/23 (SA227) | 0 |
| charter_linea | 2025-02-04 | 23:54:00 | despegue | FDO | no_regular | Fairchild Metro III/23 (SA227) | 0 |
| instruccion | 2022-09-04 | 14:53:00 | aterrizaje | MOR | vuelo_escuela | Cessna 150 | 0 |
| instruccion | 2025-08-02 | 14:39:00 | aterrizaje | MOR | vuelo_escuela | Cessna 152 | 0 |
| linea_regular | 2023-06-29 | 15:23:00 | despegue | DIL | regular |  | 0 |
| linea_regular | 2024-03-13 | 19:45:00 | aterrizaje | DIL | regular |  | 0 |
| oficial | 2021-08-26 | 09:51:00 | despegue | MDP | vuelo_oficial_nacional |  | 0 |
| oficial | 2025-03-13 | 15:37:00 | aterrizaje | MDP | vuelo_oficial_nacional |  | 0 |
| privado | 2021-07-23 | 17:51:00 | aterrizaje | FDO | vuelo_privado_con_matricula_nacional | Robinson R66 | 2 |
| privado | 2025-11-22 | 14:35:00 | aterrizaje | MOR | vuelo_privado_con_matricula_nacional | Tecnam Astore | 0 |
| taxi_aereo | 2021-04-03 | 20:53:00 | despegue | FDO | no_regular | Beechcraft King Air 200/B200 | 7 |
| taxi_aereo | 2025-10-14 | 00:30:00 | despegue | FDO | vuelo_privado_con_matricula_nacional | Cessna Citation Mustang (510) | 0 |
| trabajo_aereo | 2019-02-13 | 19:22:00 | despegue | MPP | trabajo_aereo | Cessna 182 | 0 |
| trabajo_aereo | 2021-01-18 | 19:58:00 | despegue | MPP | trabajo_aereo | Cessna 182 | 0 |

Muestra (foco, 2 por segmento): aeronave sin dato y sin matrícula:

| segmento | fecha | hora_utc | tipo_movimiento | origen_destino | clase_vuelo | aerolinea_nombre | pasajeros |
|---|---|---|---|---|---|---|---|
| charter_linea | 2024-05-30 | 18:44:00 | despegue | AER | no_regular | LADE | 2 |
| charter_linea | 2025-05-19 | 12:12:00 | despegue | BCA | no_regular | LADE | 24 |
| instruccion | 2020-01-19 | 14:45:00 | aterrizaje | MOR | vuelo_escuela | Sin dato | 0 |
| instruccion | 2020-02-01 | 23:10:00 | aterrizaje | BCA | vuelo_escuela | Sin dato | 0 |
| linea_regular | 2020-02-04 | 18:02:00 | despegue | AER | regular | Aerolíneas Argentinas | 96 |
| linea_regular | 2020-02-05 | 16:44:00 | aterrizaje | EZE | regular | Aerolíneas Argentinas | 64 |
| oficial | 2021-08-26 | 09:51:00 | despegue | MDP | vuelo_oficial_nacional | Sin dato | 0 |
| oficial | 2025-03-13 | 15:37:00 | aterrizaje | MDP | vuelo_oficial_nacional | Sin dato | 0 |
| privado | 2019-10-04 | 19:42:00 | despegue | MDB | vuelo_privado_con_matricula_nacional | Sin dato | 0 |
| privado | 2023-03-23 | 22:53:00 | despegue | FDO | vuelo_privado_con_matricula_extranjera | Treston Aviation | 9 |
| taxi_aereo | 2020-02-28 | 19:59:00 | despegue | MOR | no_regular | Sin dato | 0 |
| taxi_aereo | 2024-06-07 | 10:18:00 | despegue | HPV | no_regular | Omni Taxi Aereo | 8 |
| trabajo_aereo | 2020-02-12 | 16:32:00 | aterrizaje | MPP | trabajo_aereo | Sin dato | 0 |
| trabajo_aereo | 2020-02-12 | 16:55:00 | despegue | MPP | trabajo_aereo | Sin dato | 0 |
