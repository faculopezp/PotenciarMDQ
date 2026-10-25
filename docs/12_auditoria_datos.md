# Auditoría de datos faltantes (2026-10-25)

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

Descartados por no aportar: aeronave por matrícula (0: los aviones sin modelo nunca lo informan),
OpenSky (1: son matrículas no civiles), pasajeros por el otro extremo (0: nunca faltan).

## Validación de la inferencia por pasajeros contra el avión real (municipal 2019)

- ≤ 96 pasajeros → E190: 97,7 % de acierto. Se mantiene.
- 97–128 → 737: 70 % (30 % eran E190). **Regla eliminada.**
- > 128 → 737-800/MAX 8: 95 % en 2021+. Se mantiene.

## Lo que no se recupera con las fuentes actuales y qué haría falta

| Faltante (MDQ) | Movimientos | Qué haría falta |
|---|---|---|
| Aeronave sin matrícula, 2019–2025 | ~15.700 | Matrícula de cada movimiento antes de 2026 (pedido de acceso a la información a ANAC, Ley 27.275) |
| Operador sin matrícula, 2019–2025 | ~20.500 | Ídem |
| Aeronave y operador de vuelos oficiales con matrícula no civil (PA-, 2-H-, etc.) | ~600 en 2026 | Registro de aeronaves públicas (Fuerzas / Prefectura); ANAC no las publica |
| Lugares aptos denunciados (código numérico) | 266 | Registro de LAD con coordenadas (pedido a ANAC) |
| Asientos ofrecidos | todo | Configuración de cabina por matrícula (registro ANAC o aerolíneas) |
