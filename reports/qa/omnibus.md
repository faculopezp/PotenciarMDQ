# Micros: cobertura y validación

Fuente: CNRT vía Yvera, "Conectividad terrestre interurbana". Regular = líneas con horario; turismo = servicios DUT (contratados).

## 1. Rango de cada archivo

| servicio | archivo | desde | hasta | filas |
|---|---|---|---|---|
| regular | anual por ruta (foco) | 2019 | 2024 | 200 |
| regular | total país por día | 2019-01-01 | 2024-11-30 | 1985 |
| turismo | anual por ruta (foco) | 2019 | 2024 | 150 |
| turismo | cada servicio (foco) | 2019-04-01 | 2024-09-30 | 69342 |
| turismo | total país por día | 2019-04-01 | 2024-09-30 | 2010 |

## 2. Turismo: base de servicios ↔ archivo anual por ruta

El anual solo trae rutas con al menos un viaje semanal: tiene que dar igual o menos que la base. Misma ruta y sentido.

| anio | rutas_anual | rutas_en_base | mismos_viajes | mismos_pasajeros | pasajeros_anual | pasajeros_base_mismas_rutas | pasajeros_base_total |
|---|---|---|---|---|---|---|---|
| 2019 | 17 | 17 | 17 | 17 | 296027 | 296027 | 401669 |
| 2020 | 19 | 19 | 19 | 19 | 199137 | 199137 | 275657 |
| 2021 | 15 | 15 | 14 | 14 | 153049 | 153211 | 215302 |
| 2022 | 37 | 37 | 35 | 35 | 624482 | 624818 | 760022 |
| 2023 | 37 | 37 | 36 | 36 | 574527 | 574588 | 701624 |
| 2024 | 25 | 25 | 23 | 23 | 339974 | 340094 | 413126 |

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
| parana | Parana · Paraná | 2 |
| san miguel de tucuman | San Miguel De Tucumán · San Miguel De Tucuman | 2 |

## 5. Rutas con más pasajeros que asientos

Pasa en servicios largos con paradas: el archivo no dice si cuenta pasajeros por tramo. La ocupación por ruta no se publica; la total se informa con esta salvedad.

| servicio | anio | rutas | rutas_pax_mayor_asientos | pct_pasajeros_en_esas_rutas |
|---|---|---|---|---|
| regular | 2019 | 38 | 8 | 16.2 |
| regular | 2020 | 30 | 13 | 42.5 |
| regular | 2021 | 31 | 6 | 13.9 |
| regular | 2022 | 35 | 14 | 23.5 |
| regular | 2023 | 32 | 14 | 24.0 |
| regular | 2024 | 34 | 9 | 20.8 |
| turismo | 2019 | 17 | 0 |  |
| turismo | 2020 | 19 | 0 |  |
| turismo | 2021 | 15 | 0 |  |
| turismo | 2022 | 37 | 0 |  |
| turismo | 2023 | 37 | 0 |  |
| turismo | 2024 | 25 | 0 |  |

Las 10 más desbalanceadas (todos los años):

| servicio | anio | par | viajes | asientos | pasajeros | pax_por_asiento |
|---|---|---|---|---|---|---|
| regular | 2019 | Clorinda-Mar Del Plata | 243 | 14174 | 21912 | 1.55 |
| regular | 2020 | Clorinda-Mar Del Plata | 520 | 30506 | 46131 | 1.51 |
| regular | 2019 | Mar Del Plata-Clorinda | 235 | 13712 | 19598 | 1.43 |
| regular | 2022 | Mar Del Plata-Santa Rosa | 179 | 8296 | 11683 | 1.41 |
| regular | 2023 | Clorinda-Mar Del Plata | 447 | 26364 | 36643 | 1.39 |
| regular | 2023 | Mar Del Plata-Santa Rosa | 349 | 16235 | 22510 | 1.39 |
| regular | 2022 | San Juan-Mar Del Plata | 382 | 20730 | 28740 | 1.39 |
| regular | 2023 | Comodoro Rivadavia-Mar Del Plata | 361 | 21201 | 28821 | 1.36 |
| regular | 2024 | Mar Del Plata-Santa Rosa | 334 | 15409 | 20934 | 1.36 |
| regular | 2022 | Clorinda-Mar Del Plata | 396 | 23286 | 31582 | 1.36 |

## 6. Llegadas por año y servicio

| servicio | anio | llegadas | salidas | localidades |
|---|---|---|---|---|
| regular | 2019 | 760300 | 669034 | 19 |
| regular | 2020 | 264904 | 266395 | 15 |
| regular | 2021 | 253887 | 235142 | 16 |
| regular | 2022 | 587967 | 576775 | 18 |
| regular | 2023 | 675436 | 679203 | 16 |
| regular | 2024 | 442197 | 450628 | 17 |
| turismo | 2019 | 163396 | 132631 | 13 |
| turismo | 2020 | 130438 | 68699 | 13 |
| turismo | 2021 | 90207 | 62842 | 11 |
| turismo | 2022 | 357754 | 266728 | 27 |
| turismo | 2023 | 334201 | 240326 | 26 |
| turismo | 2024 | 193450 | 146524 | 16 |
