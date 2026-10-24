---
title: Metodología y fuentes
---

# Metodología y fuentes

## De dónde salen los datos

| Dato | Fuente | Cobertura |
|---|---|---|
| Cada aterrizaje y despegue (fecha, hora, aerolínea, avión, origen/destino, pasajeros) | ANAC — "Aterrizajes y despegues procesados por la ANAC", Portal de Datos Abiertos de Transporte | 2019 → hoy, se actualiza mensualmente |
| Coordenadas y nombres de aeropuertos | OurAirports (dominio público) | — |
| Feriados nacionales | Calendario oficial (paquete `holidays`) | — |
| Hitos históricos | Notas de prensa y fuentes secundarias, marcadas como tales | — |

Los datos se descargan y procesan automáticamente una vez por mes. El código es abierto.

## Cómo se cuenta

- **Movimiento:** un aterrizaje o un despegue en Mar del Plata. Un vuelo de ida y vuelta son dos movimientos acá.
- **Pasajeros:** los que bajan más los que suben en Mar del Plata (estándar internacional de aeropuertos). No hay doble conteo.
- **Vuelos comerciales:** regulares y no regulares (charter, taxi aéreo). El resto (privados, escuela, oficiales) se muestra aparte.
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
