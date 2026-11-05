# Micros: cobertura y validación

Fuente: CNRT vía Yvera, "Conectividad terrestre interurbana". Regular = líneas con horario; turismo = servicios DUT (contratados).

## 1. Rango de cada archivo

| servicio | archivo | desde | hasta | filas |
|---|---|---|---|---|


Fuente usada por servicio y año:

| servicio | anio | fuente | filas |
|---|---|---|---|


## 2. Base por viaje ↔ archivo anual por ruta

El anual solo trae rutas con al menos un viaje semanal: tiene que dar igual o menos que la base. Misma ruta y sentido.

| servicio | anio | rutas_anual | rutas_en_base | mismos_viajes | mismos_pasajeros | pasajeros_anual | pasajeros_base_mismas_rutas | pasajeros_base_total |
|---|---|---|---|---|---|---|---|---|


## 3. Pares con Mar del Plata sin sentido reconocido

| servicio | filas |
|---|---|
| regular | 0 |
| regular (con sentido) | 0 |
| turismo | 0 |
| turismo (con sentido) | 0 |

## 4. Nombres unificados (misma localidad escrita distinto)

| extremo_clave | escrituras | servicios |
|---|---|---|


Localidades con más de una provincia en las bases (se toma la más frecuente):

| clave | provincias |
|---|---|


## 5. Rutas con más pasajeros que asientos

Pasa en servicios largos con paradas: el archivo no dice si cuenta pasajeros por tramo. La ocupación por ruta no se publica; la total se informa con esta salvedad.

| servicio | anio | rutas | rutas_pax_mayor_asientos | pct_pasajeros_en_esas_rutas |
|---|---|---|---|---|


Las 10 más desbalanceadas (todos los años):

| servicio | anio | sentido | extremo_crudo | viajes | asientos | pasajeros | pax_por_asiento |
|---|---|---|---|---|---|---|---|


Viajes sueltos con más pasajeros que asientos (bases por viaje):

| servicio | viajes | viajes_pax_mayor_asientos | pct |
|---|---|---|---|


## 6. Llegadas por año y servicio

| servicio | anio | fuente | llegadas | salidas | localidades |
|---|---|---|---|---|---|


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
| 2019 | 8063025.0 | 8063024.0 | 185601.0 | 186574 | 1188677.0 |  | 212717.0 | 425067 |
| 2020 | 3639343.0 | 3639343.0 | 53109.0 | 52980 | 596947.0 |  | 113478.0 | 235036 |
| 2021 | 6644442.0 | 6644442.0 | 41486.0 | 41796 | 354465.0 |  | 366021.0 | 738603 |
| 2022 | 8860018.0 | 8860018.0 | 132906.0 | 133430 | 934890.0 |  | 447469.0 | 903148 |
| 2023 | 9281513.0 | 9281017.0 | 147988.0 | 150087 | 1096722.0 |  | 385359.0 | 828973 |
| 2024 | 8508365.0 | 8508365.0 | 140304.0 | 142599 | 842919.0 |  | 312413.0 | 661775 |
| 2025 | 8264293.0 | 8264293.0 | 145047.0 | 146116 | 888511.0 |  | 252433.0 | 532496 |

## 8. EVyTH: viajes de residentes con destino Mar del Plata

Casos encuestados (sin expandir) por año y tipo de visitante, y medio informado:

| anio | trimestres | casos_turistas | casos_excursionistas | turistas_expandidos |
|---|---|---|---|---|


| medio | medio_detalle | casos | expandidos |
|---|---|---|---|


Peso de los casos más grandes (turistas): si pocos casos explican mucho, el reparto de ese año es volátil.

| anio | casos | pct_top10 | pondera_media_auto | pondera_media_omnibus | pondera_media_tren |
|---|---|---|---|---|---|

