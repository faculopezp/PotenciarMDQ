# Auditoría de datos faltantes (2026-10-26)

Reporte vivo: `reports/qa/auditoria.md` (se regenera en cada corrida del CI).

## Qué falta (MDQ, 2021+)

| Segmento | Sin operador | Sin aeronave |
|---|---|---|
| Línea regular | 0,3 % | 2 % |
| Privado | 93 % | 6 % |
| Oficial y militar | 86 % | 90 % |
| Taxi aéreo | 84 % | 11 % |
| Escuelas | 90 % | 0,2 % |

Pasajeros, hora y origen/destino: completos. Matrícula: solo desde 2026.

## Recuperado con cruces exactos (aplicado en la BD)

| Cruce | MDQ | Resto del país |
|---|---|---|
| Operador por matrícula (todos los vuelos del avión con el mismo operador, ≥ 2) | 431 | 20.229 |
| Operador por el otro extremo del mismo vuelo (matrícula, un solo candidato) | 22 | 526 |
| Aeronave 2019 del portal municipal (1 a 1 por día, hora, movimiento, origen/destino, aerolínea) | 1.356 | — |

Agregados el 2026-10-26 (cifras de MDQ 2019–2026, corrida del CI):

| Recuperación | MDQ | Validación |
|---|---|---|
| Operador por el otro extremo del vuelo **sin matrícula** (aeropuertos cruzados, movimiento opuesto, 10 min–10 h, avión/operador compatibles, candidato único de cada lado) | 643 | 98,8 % de coincidencia en operador, 96,0 % en avión (escondiendo el dato en vuelos que lo traen) |
| Operador de aeronaves del Estado por prefijo (`config/estatales.yaml`: FAA, Ejército, Armada, Gendarmería, Prefectura, PFA) | 319 | FAA 99 %, Ejército 99 %, Gendarmería 91 %; Prefectura 78 % y Armada 0 % porque ANAC carga "Fuerza Aérea" en aviones que fuentes públicas identifican de esas fuerzas |
| Modelo de aeronaves del Estado por serie con identificación pública (T-94/T-95 ERJ-140, T-99 737-700, TC-53 F28, PA-40/41/43 Dauphin) | 439 | Fuente por serie en `config/estatales.yaml` |
| Asientos publicados por aerolínea y modelo (`config/cabinas.yaml`) | 8.567 de línea | Coinciden con el p95 observado: E190 96 = 96, 737-800 Flybondi 189 = 189, MAX 8 170 vs 172, ERJ-145 50 = 50, 737-700 Andes 142 = 142 |

Lugares aptos denunciados: quedan como LAD (sin coordenadas, fuera del mapa).

Reclasificación: todo vuelo **privado en jet o turbohélice ejecutivo** se analiza como taxi aéreo
(`segmento_reclasificado`). En MDQ, de los que traen operador o matrícula, 363 de 366 (2019–2026) son
de operadores o aviones que también vuelan como no regular (posicionamientos).

Descartados por no aportar: aeronave por matrícula (0: los aviones sin modelo nunca lo informan),
OpenSky (1: son matrículas no civiles), pasajeros por el otro extremo (0: nunca faltan).

## Validación de la inferencia por pasajeros contra el avión real (municipal 2019)

- ≤ 96 pasajeros → E190: 97,7 % de acierto. Se mantiene.
- 97–128 → 737: 70 % (30 % eran E190). **Regla eliminada.**
- > 128 → 737-800/MAX 8: 95 % en 2021+. Se mantiene.

Nota: ~4 % de los vuelos con cabina publicada informan más pasajeros que asientos (E190: 11.128 de
283.168). Es un error de carga de ANAC (o incluye infantes); el load factor de esos vuelos supera 100 %.

## Lo que no se recupera con las fuentes actuales y qué haría falta

| Faltante | Qué haría falta |
|---|---|
| Aeronave y operador sin matrícula, 2019–2025 (sobre todo privados, escuelas y oficiales) | Matrícula de cada movimiento antes de 2026 (pedido de acceso a la información a ANAC, Ley 27.275) |
| Modelo de aeronaves del Estado sin identificación pública (PA-22, PG-380, 1-G-50, TC-64/66…) | Registro de aeronaves de las Fuerzas / Prefectura, o fuentes por serie |
| Asientos de Aerolíneas 737-800 y 737-700, Andes 737-800, F28 | Fuente que resuelva la contradicción (170 vs 186–189; 128 vs 137; 62 vs 65); mientras tanto, p95 |
| Lugares aptos denunciados | Se dejan como LAD |
