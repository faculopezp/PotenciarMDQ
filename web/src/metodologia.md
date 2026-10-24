---
title: Metodología y fuentes
---

# Metodología y fuentes

## De dónde salen los datos

| Dato | Fuente | Cobertura |
|---|---|---|
| Cada aterrizaje y despegue (fecha, hora, aerolínea, avión, origen/destino, pasajeros) | ANAC — "Aterrizajes y despegues procesados por la ANAC", Portal de Datos Abiertos de Transporte | 2019 → hoy, se actualiza mensualmente |
| Pasajeros y movimientos mensuales del aeropuerto, por ruta | Municipio de General Pueyrredon — datos.mardelplata.gob.ar | 2001–2020 (se usa hasta 2018) |
| Vuelos individuales (muestra, sin pasajeros) | Municipio de General Pueyrredon | 2015–2018 (≈ 52 % de los movimientos) |
| Turistas arribados, estadía, fines de semana largos | EMTURyC vía datos.mardelplata.gob.ar | 2007–2025 |
| Clima diario en el aeropuerto | Open-Meteo (reanálisis ERA5) | 2019 → hoy |
| Coordenadas y nombres de aeropuertos | OurAirports (dominio público) | — |
| Feriados nacionales | Calendario oficial (paquete `holidays`) | — |
| Hitos históricos | Notas de prensa y fuentes secundarias, marcadas como tales | — |

Los datos se descargan y procesan automáticamente una vez por mes. El código es abierto.

## Cómo se cuenta

- **Movimiento:** un aterrizaje o un despegue en Mar del Plata. Un vuelo de ida y vuelta son dos movimientos acá.
- **Pasajeros:** los que bajan más los que suben en Mar del Plata (estándar internacional de aeropuertos). No hay doble conteo.
- **Segmentos:** cada movimiento se clasifica según la clase de vuelo que informa la ANAC: *línea regular*; *charter de línea* (no regular con avión u operador de línea); *taxi aéreo* (el resto de los no regulares: jets y turbohélices ejecutivos, avionetas, helicópteros); *privado*; *oficial y militar*; *escuelas de vuelo*; *trabajo aéreo*. Ningún movimiento queda sin segmento.
- **Lugares aptos denunciados (LAD):** los orígenes/destinos con código numérico son superficies aptas registradas por denuncia ante la ANAC, que no son aeródromos (art. 25 del Código Aeronáutico). No tienen coordenadas públicas: no aparecen en el mapa ni se cuentan como vuelos al exterior, aunque la ANAC los clasifique como internacionales.
- **Modelo de avión:** las denominaciones de la ANAC se estandarizan a un modelo con designador ICAO (ej. `BO-737-800`, `BO-B737-800` y `BO-737-8SH` son el Boeing 737-800). Validado contra OpenSky por matrícula (95 % de coincidencia).
- **Operadores:** variantes del mismo nombre (`LADE` / `L.A.D.E.`, `S.A.` / `SA`) se unifican.
- **Taxi aéreo a pistón:** cuenta como taxi solo con 6 plazas o más (piloto + 5 pasajeros); si no, se analiza como privado.
- **Modelo de avión faltante:** la ANAC no informa el modelo en 2019 y en parte de 2020, y en ~20 % de los movimientos posteriores (sobre todo vuelos oficiales y militares). En vuelos de Aerolíneas se infiere por pasajeros a bordo: hasta 96 → E190 (acierta 93 % en 2021+), 97–128 → 737 sin variante, más de 128 → 737-800/MAX 8 (95 %). Avian 2019 → ATR 72-600; Flyest → CRJ200. Lo inferido se marca como tal.
- **Serie larga:** hasta 2018 se usan los datos municipales y desde 2019 los de la ANAC. En 2019, año que cubren ambas fuentes, difieren menos de 4 % por mes. Desde 2021 el Municipio publica pasajeros de un solo sentido, por eso no se usa.
- **Datos provisorios:** la ANAC marca como provisorios los últimos meses; pueden cambiar.
- **Hora local:** hora UTC − 3.

## Métricas estimadas (leer con cuidado)

| Métrica | Cómo se calcula | Por qué es una estimación |
|---|---|---|
| Asientos ofrecidos | Capacidad típica de cada avión = percentil 95 de los pasajeros observados en ese modelo (y aerolínea) en todo el país | ANAC no publica asientos |
| Ocupación (load factor) | Pasajeros ÷ asientos estimados | Hereda la estimación de asientos; tiende a sobrestimar unos puntos |
| Duración de vuelo | Se une el despegue en el origen con el aterrizaje en destino del mismo avión | ANAC no publica número de vuelo; se empareja por aerolínea y modelo (y matrícula desde 2026) |
| Tiempo en tierra (turnaround) | Aterrizaje → siguiente despegue del mismo avión en MDQ | Igual que arriba; validado contra matrícula en 2026 (medianas 51 vs 52 min) |
| Hora pico de diseño | 30.ª hora con más pasajeros del año (Standard Busy Rate) | — |
| Concentración (HHI) | Suma de las cuotas de mercado al cuadrado × 10.000 | — |
| Tendencia | Descomposición estacional STL (período 12) de los pasajeros mensuales | Suaviza; los extremos se revisan con cada dato nuevo |
| Días atípicos | Desvío respecto de la mediana del mismo día de la semana ±3 semanas, en desvíos robustos (MAD); atípico si supera 3 | Los paros se rotulan solo con fuente de prensa |
| Pronóstico | Holt-Winters (log, tendencia amortiguada, estacionalidad anual) sobre la serie pospandemia; banda = 80 % de 2.000 simulaciones | No anticipa rutas nuevas ni cambios de aerolíneas |
| Peso en la red | PageRank de la red de vuelos de cabotaje reconstruidos | — |
| Avión típico | Familia con más movimientos por segmento; "capacidad observada" = p95 de pasajeros de ese modelo en ese segmento en todo el país | En aviación general es pasajeros llevados, no asientos |

## Lo que no se puede medir con estos datos

- Puntualidad y cancelaciones (no hay horarios programados).
- Tarifas.
- Origen de los turistas (los pasajeros no tienen nacionalidad ni residencia en este dataset).

## Descargar los datos

```js
const archivos = [
  ["Serie anual", FileAttachment("data/mdq_anual.json")],
  ["Serie mensual", FileAttachment("data/mdq_mensual.json")],
  ["Serie diaria", FileAttachment("data/mdq_diario.json")],
  ["Rutas", FileAttachment("data/mdq_rutas.json")],
  ["Aerolíneas", FileAttachment("data/mdq_aerolineas.json")],
  ["Aeropuertos pares", FileAttachment("data/benchmark_pares.json")]
];
```

```js
html`<ul>${archivos.map(([n, f]) => html`<li><a href=${f.href} download=${f.name}>${n}</a> (JSON)</li>`)}</ul>`
```

```js
import {html} from "htl";
```
