# Micros: cobertura y validación

Fuente: CNRT vía Yvera, "Conectividad terrestre interurbana". Regular = líneas con horario; turismo = servicios DUT (contratados).

## 1. Rango de cada archivo

| servicio | archivo | desde | hasta | filas |
|---|---|---|---|---|
| regular | anual por ruta (foco) | 2019 | 2024 | 200 |
| regular | base por viaje (foco) | 2019-01-01 | 2024-11-30 | 161273 |
| regular | total país por día | 2019-01-01 | 2024-11-30 | 1985 |
| turismo | anual por ruta (foco) | 2019 | 2024 | 150 |
| turismo | base por viaje (foco) | 2019-04-01 | 2024-09-30 | 69342 |
| turismo | total país por día | 2019-04-01 | 2024-09-30 | 2010 |

Fuente usada por servicio y año:

| servicio | anio | fuente | filas |
|---|---|---|---|
| regular | 2019 | base_por_viaje | 317 |
| regular | 2020 | anual_por_ruta | 30 |
| regular | 2021 | base_por_viaje | 38 |
| regular | 2022 | base_por_viaje | 42 |
| regular | 2023 | base_por_viaje | 42 |
| regular | 2024 | base_por_viaje | 46 |
| turismo | 2019 | base_por_viaje | 640 |
| turismo | 2020 | base_por_viaje | 459 |
| turismo | 2021 | base_por_viaje | 441 |
| turismo | 2022 | base_por_viaje | 794 |
| turismo | 2023 | base_por_viaje | 731 |
| turismo | 2024 | base_por_viaje | 452 |

## 2. Base por viaje ↔ archivo anual por ruta

El anual solo trae rutas con al menos un viaje semanal: tiene que dar igual o menos que la base. Misma ruta y sentido.

| servicio | anio | rutas_anual | rutas_en_base | mismos_viajes | mismos_pasajeros | pasajeros_anual | pasajeros_base_mismas_rutas | pasajeros_base_total |
|---|---|---|---|---|---|---|---|---|
| regular | 2019 | 36 | 36 | 36 | 36 | 1429334 | 1429334 | 1470135 |
| regular | 2020 | 30 | 30 | 30 | 30 | 531299 | 531299 | 532601 |
| regular | 2021 | 31 | 31 | 31 | 31 | 489029 | 489029 | 490904 |
| regular | 2022 | 35 | 35 | 35 | 35 | 1164742 | 1164742 | 1164931 |
| regular | 2023 | 32 | 32 | 32 | 32 | 1354639 | 1354639 | 1356876 |
| regular | 2024 | 34 | 34 | 34 | 34 | 892825 | 892825 | 895949 |
| turismo | 2019 | 17 | 17 | 17 | 17 | 296027 | 296027 | 401669 |
| turismo | 2020 | 19 | 19 | 19 | 19 | 199137 | 199137 | 275657 |
| turismo | 2021 | 15 | 15 | 14 | 14 | 153049 | 153211 | 215302 |
| turismo | 2022 | 37 | 37 | 35 | 35 | 624482 | 624818 | 760022 |
| turismo | 2023 | 37 | 37 | 36 | 36 | 574527 | 574588 | 701624 |
| turismo | 2024 | 25 | 25 | 23 | 23 | 339974 | 340094 | 413126 |

## 3. Pares con Mar del Plata sin sentido reconocido

| servicio | filas |
|---|---|
| regular | 200 |
| regular (con sentido) | 200 |
| turismo | 151 |
| turismo (con sentido) | 150 |

## 4. Nombres unificados (misma localidad escrita distinto)

| extremo_clave | escrituras | servicios |
|---|---|---|
| ciudad autonoma de buenos aires | Caba · Ciudad Autónoma De Buenos Aires · Ciudad Autonoma De Buenos Aires | 2 |
| cordoba | Córdoba · Cordoba | 2 |
| neuquen | Neuquén · Neuquen | 2 |
| parana | Paraná · Parana | 2 |
| san miguel de tucuman | San Miguel De Tucuman · San Miguel De Tucumán | 2 |

Localidades con más de una provincia en las bases (se toma la más frecuente):

| clave | provincias |
|---|---|
| 25 de mayo | Buenos Aires (44) · Santiago Del Estero (1) |
| aimogasta | La Rioja (17) · Catamarca (2) |
| alvear | Corrientes (1) · Mendoza (1) |
| andalgala | Santiago Del Estero (1) · Catamarca (2) |
| aristobulo del valle | Misiones (1) · Tucumán (1) |
| arroyito | Córdoba (22) · Santa Fe (1) |
| avellaneda | Buenos Aires (77) · Santa Fe (4) · Entre Ríos (1) |
| bandera | Santiago Del Estero (1) · Buenos Aires (2) |
| bella vista | Corrientes (3) · Buenos Aires (6) |
| capital | Buenos Aires (8) · San Juan (10) · Santiago Del Estero (5) · Tucumán (2) · Entre Ríos (1) |
| catrilo | Buenos Aires (1) · La Pampa (37) |
| chanar ladeado | Córdoba (1) · Santa Fe (2) |
| chubut | Chubut (2) · Buenos Aires (1) |
| cipolletti | Neuquén (1) · Río Negro (35) |
| ciudad | Mendoza (11) · San Juan (1) · San Luis (3) |
| ciudad autonoma de buenos aires | Buenos Aires (369) · Ciudad Autónoma De Buenos Aires (105498) |
| de omnibus | Santiago Del Estero (1) · Mendoza (3) |
| el bolson | Neuquén (1) · Río Negro (17) |
| el calafate | Santa Cruz (18) · Río Negro (1) |
| el trebol | Córdoba (1) · Santa Fe (10) |
| federacion | Entre Ríos (215) · Misiones (1) · Santiago Del Estero (1) · Buenos Aires (1) |
| flores | Buenos Aires (188) · Salta (1) |
| general alvear | Buenos Aires (1) · Mendoza (2) |
| general gelly | Santa Fe (199) · Santa Cruz (1) · Buenos Aires (2) |
| general roca | Río Negro (35) · Neuquén (1) |
| general san martin | Buenos Aires (3) · Chaco (1) · La Pampa (15) |
| ituzaingo | Corrientes (19) · Buenos Aires (31) |
| jacinto arauz | Buenos Aires (3) · La Pampa (22) |
| juan jose castelli | Buenos Aires (4) · Chaco (6) |
| la pampa | Buenos Aires (1) · Santa Fe (1) · La Pampa (7) |
| la paz | Entre Ríos (8) · Córdoba (2) |
| lavalle | Mendoza (1) · Tucumán (1) |
| libertador general san martin | Jujuy (70) · Entre Ríos (1) |
| lujan | Buenos Aires (35) · San Luis (1) |
| maipu | Buenos Aires (4) · Mendoza (21) |
| malvinas argentinas | Buenos Aires (8) · Córdoba (1) |
| marco juarez | Córdoba (1) · Santa Fe (1) |
| mercedes | Buenos Aires (67) · Corrientes (14) |
| merlo | Buenos Aires (76) · San Luis (390) |
| miramar | Buenos Aires (11) · Córdoba (1) |
| misiones | Corrientes (1) · Misiones (3) |
| piedritas | Buenos Aires (1) · La Pampa (1) |
| recreo | Catamarca (2) · Santa Fe (3) |
| rio colorado | Buenos Aires (5) · Tucumán (4) · Río Negro (170) |
| rio cuarto | Córdoba (90) · Tucumán (1) |
| rio hondo | Buenos Aires (1) · Santiago Del Estero (37) |
| rio negro | Río Negro (2) · Neuquén (1) |
| roca | La Pampa (1) · Río Negro (1) |
| roldan | Córdoba (1) · Santa Fe (6) |
| san andres | Buenos Aires (3) · Tucumán (2) |
| san bernardo | Chaco (1) · Buenos Aires (8) |
| san carlos | Santa Fe (1) · Mendoza (4) |
| san fernando | Buenos Aires (31) · Chaco (2) · Catamarca (2) |
| san javier | Córdoba (1) · Misiones (2) |
| san jose | Misiones (1) · Entre Ríos (7) |
| san justo | Buenos Aires (83) · Santa Fe (12) |
| san lorenzo | Corrientes (1) · Santa Fe (91) |
| san martin | Buenos Aires (27) · Mendoza (16) · Chaco (1) · La Pampa (4) |
| san miguel | Buenos Aires (9047) · Tucumán (23) |
| san nicolas | Buenos Aires (56) · Santa Fe (2) |
| san pedro | Jujuy (8) · Buenos Aires (54) · Salta (1) |
| san vicente | Misiones (2) · Buenos Aires (2) |
| santa ana | Misiones (1) · Córdoba (1) · Tucumán (2) |
| santo tome | Santa Fe (9) · Corrientes (8) |
| suipacha | Mendoza (1) · Buenos Aires (2) |
| vila gobernador galvez | Entre Ríos (1) · Santa Fe (15) |
| villa constitucion | Santa Fe (195) · Buenos Aires (3) |
| villa union | La Rioja (10) · San Juan (2) |

## 5. Rutas con más pasajeros que asientos

Pasa en servicios largos con paradas: el archivo no dice si cuenta pasajeros por tramo. La ocupación por ruta no se publica; la total se informa con esta salvedad.

| servicio | anio | rutas | rutas_pax_mayor_asientos | pct_pasajeros_en_esas_rutas |
|---|---|---|---|---|
| regular | 2019 | 317 | 36 | 15.9 |
| regular | 2020 | 30 | 13 | 42.5 |
| regular | 2021 | 38 | 6 | 13.8 |
| regular | 2022 | 42 | 14 | 23.5 |
| regular | 2023 | 42 | 16 | 23.9 |
| regular | 2024 | 46 | 9 | 20.7 |
| turismo | 2019 | 640 | 20 | 0.4 |
| turismo | 2020 | 459 | 39 | 1.5 |
| turismo | 2021 | 441 | 14 | 0.5 |
| turismo | 2022 | 794 | 43 | 0.7 |
| turismo | 2023 | 731 | 39 | 1.1 |
| turismo | 2024 | 452 | 25 | 0.4 |

Las 10 más desbalanceadas (todos los años):

| servicio | anio | sentido | extremo_crudo | viajes | asientos | pasajeros | pax_por_asiento |
|---|---|---|---|---|---|---|---|
| turismo | 2022 | salida | Paternal | 1 | 58 | 114 | 1.97 |
| turismo | 2023 | salida | Concorida | 1 | 64 | 122 | 1.91 |
| turismo | 2019 | llegada | El Arenal | 1 | 60 | 113 | 1.88 |
| turismo | 2023 | llegada | La Cruz | 1 | 60 | 109 | 1.82 |
| turismo | 2020 | llegada | Lavalle | 1 | 37 | 65 | 1.76 |
| turismo | 2024 | llegada | San Justo | 1 | 62 | 102 | 1.65 |
| regular | 2019 | llegada | Clorinda | 243 | 14174 | 21912 | 1.55 |
| turismo | 2021 | llegada | Malvinas Argentinas | 1 | 58 | 89 | 1.53 |
| regular | 2020 | llegada | Clorinda | 520 | 30506 | 46131 | 1.51 |
| regular | 2019 | salida | Clorinda | 235 | 13712 | 19598 | 1.43 |

Viajes sueltos con más pasajeros que asientos (bases por viaje):

| servicio | viajes | viajes_pax_mayor_asientos | pct |
|---|---|---|---|
| regular | 161273 | 32242 | 20.0 |
| turismo | 69342 | 4758 | 6.9 |

## 6. Llegadas por año y servicio

| servicio | anio | fuente | llegadas | salidas | localidades |
|---|---|---|---|---|---|
| regular | 2019 | base_por_viaje | 791206 | 678929 | 241 |
| regular | 2020 | anual_por_ruta | 264904 | 266395 | 15 |
| regular | 2021 | base_por_viaje | 254913 | 235991 | 21 |
| regular | 2022 | base_por_viaje | 588031 | 576900 | 22 |
| regular | 2023 | base_por_viaje | 677116 | 679760 | 22 |
| regular | 2024 | base_por_viaje | 444416 | 451533 | 25 |
| turismo | 2019 | base_por_viaje | 238584 | 163085 | 520 |
| turismo | 2020 | base_por_viaje | 181975 | 93682 | 341 |
| turismo | 2021 | base_por_viaje | 131497 | 83805 | 345 |
| turismo | 2022 | base_por_viaje | 448735 | 311287 | 610 |
| turismo | 2023 | base_por_viaje | 418380 | 283244 | 558 |
| turismo | 2024 | base_por_viaje | 230512 | 182614 | 340 |

## 7. Tren (CNRT, pasajeros pagos)

Servicios que se toman como de Mar del Plata y meses con dato por año:

| servicio | operador | jurisdiccion | desde | hasta | meses | pasajeros |
|---|---|---|---|---|---|---|
| P. Constitución-Mar del Plata-Miramar (Buenos Aires) | FERROBAIRES | Provincial | 2008 | 2011 | 48 | 1950344 |
| P. Constitución-Mar del Plata (Buenos Aires) | SOFSE | Nacional | 2011 | 2025 | 99 | 4051738 |
| P. Constitución-Mar del Plata (Buenos Aires) | FERROBAIRES | Nacional | 2012 | 2012 | 12 | 280629 |
| P. Constitución-Mar del Plata (Buenos Aires) | FERROBAIRES | Provincial | 2013 | 2016 | 39 | 290424 |
| P. Constitución-Mar del Plata (Buenos Aires) | SOFSE | Provincial | 2024 | 2025 | 12 | 626506 |
| P. Constitución-Mar del Plata (Buenos Aires) | SOFSA | Nacional | 2025 | 2026 | 18 | 767780 |

Meses repetidos (mismo servicio, operador, año y mes más de una vez; dos operadores en el mismo mes no es repetición: se suman):

| anio | mes | servicio | operador | filas |
|---|---|---|---|---|


Meses del foco con más de un operador:

| anio | operadores | meses |
|---|---|---|
| 2011 | SOFSE · FERROBAIRES | 6 |
| 2012 | SOFSE · FERROBAIRES | 10 |
| 2014 | FERROBAIRES · SOFSE | 1 |
| 2015 | SOFSE · FERROBAIRES | 8 |

## 9. EMTUR por medio de transporte contra los conteos

Suma de los cuatro medios contra el total de turistas del EMTUR, y cada medio contra lo medido (avión: ANAC; micro: CNRT; tren: CNRT, ida y vuelta).

| anio | emtur_medios | emtur_turistas | emtur_avion | anac_aterrizajes_linea | emtur_omnibus | cnrt_micro_llegadas | emtur_tren | cnrt_tren_ida_vuelta |
|---|---|---|---|---|---|---|---|---|
| 2013 | 8475341.0 | 8476928.0 | 70763.0 |  | 1492555.0 |  | 64895.0 | 132813 |
| 2014 | 8437644.0 | 8437644.0 | 67714.0 |  | 1465398.0 |  | 46644.0 | 98029 |
| 2015 | 8846314.0 | 8846314.0 | 96272.0 |  | 1446630.0 |  | 89611.0 | 200940 |
| 2016 | 7622961.0 | 8452695.0 | 102009.0 |  | 1392975.0 |  | 0.0 | 10303 |
| 2017 | 8570979.0 | 8570980.0 | 138192.0 |  | 1323507.0 |  | 67834.0 | 132480 |
| 2018 | 8355934.0 | 8355935.0 | 222685.0 |  | 1299786.0 |  | 155383.0 | 314527 |
| 2019 | 8063025.0 | 8063024.0 | 185601.0 | 186574 | 1188677.0 | 1029790 | 212717.0 | 425067 |
| 2020 | 3639343.0 | 3639343.0 | 53109.0 | 52980 | 596947.0 | 442522 | 113478.0 | 235036 |
| 2021 | 6644442.0 | 6644442.0 | 41486.0 | 41796 | 354465.0 | 386410 | 366021.0 | 738603 |
| 2022 | 8860018.0 | 8860018.0 | 132906.0 | 133430 | 934890.0 | 1036766 | 447469.0 | 903148 |
| 2023 | 9281513.0 | 9281017.0 | 147988.0 | 150087 | 1096722.0 | 1095496 | 385359.0 | 828973 |
| 2024 | 8508365.0 | 8508365.0 | 140304.0 | 142599 | 842919.0 | 674928 | 312413.0 | 661775 |
| 2025 | 8264293.0 | 8264293.0 | 145047.0 | 146116 | 888511.0 |  | 252433.0 | 532496 |

## 8. EVyTH: viajes de residentes con destino Mar del Plata

Casos encuestados (sin expandir) por año y tipo de visitante, y medio informado:

| anio | trimestres | casos_turistas | casos_excursionistas | turistas_expandidos |
|---|---|---|---|---|
| 2012 | 4 | 1301 | 113 | 1893178.0 |
| 2013 | 4 | 1202 | 63 | 1866850.0 |
| 2014 | 4 | 1134 | 34 | 1777323.0 |
| 2015 | 4 | 1126 | 172 | 1539510.0 |
| 2016 | 4 | 1160 | 59 | 2051264.0 |
| 2017 | 4 | 1255 | 23 | 1971392.0 |
| 2018 | 4 | 1249 | 40 | 1814071.0 |
| 2019 | 4 | 1070 | 37 | 1668083.0 |
| 2020 | 4 | 434 | 41 | 708141.0 |
| 2021 | 4 | 502 | 15 | 490640.0 |
| 2022 | 4 | 836 | 41 | 1347418.0 |
| 2023 | 4 | 938 | 68 | 1372083.0 |
| 2024 | 2 | 685 | 32 | 1148346.0 |

| medio | medio_detalle | casos | expandidos |
|---|---|---|---|
| Auto | Automóvil o similar (propio) | 8798 | 13486785.0 |
| Ómnibus | Omnibus | 3966 | 6317377.0 |
| Tren | Tren | 355 | 971879.0 |
| Avión | Avión | 467 | 400144.0 |
| Otros | Otro (auto alquilado, motocicleta, bicicleta, a pie, a "dedo", etc.) | 32 | 80911.0 |
| Otros | Ns./ Nr. | 5 | 4906.0 |
| Otros | Embarcación | 5 | 3370.0 |
| Otros | Taxi o remís | 2 | 358.0 |

Peso de los casos más grandes (turistas): si pocos casos explican mucho, el reparto de ese año es volátil.

| anio | casos | pct_top10 | pondera_media_auto | pondera_media_omnibus | pondera_media_tren |
|---|---|---|---|---|---|
| 2012 | 1301 | 4.6 | 1450.0 | 1442.0 | 1851.0 |
| 2013 | 1202 | 5.2 | 1560.0 | 1439.0 | 4713.0 |
| 2014 | 1134 | 5.3 | 1599.0 | 1535.0 | 1767.0 |
| 2015 | 1126 | 7.6 | 1313.0 | 1508.0 | 1541.0 |
| 2016 | 1160 | 6.1 | 1734.0 | 1987.0 |  |
| 2017 | 1255 | 8.4 | 1640.0 | 1439.0 | 2770.0 |
| 2018 | 1249 | 8.6 | 1436.0 | 1491.0 | 2741.0 |
| 2019 | 1070 | 7.7 | 1555.0 | 1591.0 | 2671.0 |
| 2020 | 434 | 17.2 | 1829.0 | 1115.0 | 3603.0 |
| 2021 | 502 | 34.0 | 795.0 | 542.0 | 4012.0 |
| 2022 | 836 | 15.0 | 1682.0 | 1227.0 | 3183.0 |
| 2023 | 938 | 14.3 | 1118.0 | 2354.0 | 1766.0 |
| 2024 | 685 | 15.8 | 1671.0 | 1599.0 | 2193.0 |
