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
| neuquen | Neuquen · Neuquén | 2 |
| parana | Parana · Paraná | 2 |
| san miguel de tucuman | San Miguel De Tucuman · San Miguel De Tucumán | 2 |

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


Meses duplicados (mismo servicio, año y mes más de una vez):

| anio | mes | servicio | filas |
|---|---|---|---|

