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
| ciudad autonoma de buenos aires | Ciudad Autónoma De Buenos Aires · Ciudad Autonoma De Buenos Aires · Caba | 2 |
| cordoba | Córdoba · Cordoba | 2 |
| neuquen | Neuquén · Neuquen | 2 |
| parana | Parana · Paraná | 2 |
| san miguel de tucuman | San Miguel De Tucumán · San Miguel De Tucuman | 2 |

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

Meses duplicados (mismo servicio, año y mes más de una vez):

| anio | mes | servicio | filas |
|---|---|---|---|
| 2012 | 1 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 2 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 3 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 4 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 5 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 6 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 7 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 8 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 9 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2012 | 10 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2014 | 12 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 1 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 2 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 3 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 4 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 5 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 6 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 7 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 8 | P. Constitución-Mar del Plata (Buenos Aires) | 2 |
| 2015 | 9 | P. Constitución-Bahía Blanca (Buenos Aires) | 2 |

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
