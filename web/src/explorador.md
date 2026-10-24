---
title: Explorador
---


```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import * as Inputs from "@observablehq/inputs";
import {FOCO, entero, MESES, DIAS, CATEGORIAS, CLASES, SEGMENTOS, columnas} from "./components/util.js";
import {html} from "htl";
```

# Explorador

Filtrá los aterrizajes y despegues del Aeropuerto de Mar del Plata como en la vieja consulta interactiva de la ANAC: por año, tipo de vuelo, aerolínea y tipo de avión.

```js
const base = columnas(FileAttachment("data/mdq_explorador.json"));
```

```js
const anios = [...new Set(base.map((d) => d.anio))].sort();
const aerolineasLista = d3.rollups(base, (v) => d3.sum(v, (d) => d.movimientos), (d) => d.aerolinea_nombre)
  .sort((a, b) => b[1] - a[1]).map(([a]) => a);
const categoriasLista = [...new Set(base.map((d) => d.aeronave_categoria))];
```

```js
const filtros = view(Inputs.form({
  anios: Inputs.checkbox(anios, {label: "Años", value: anios, format: String}),
  segmentos: Inputs.checkbox(SEGMENTOS, {label: "Segmentos", format: (s) => s.nombre, value: SEGMENTOS}),
  aerolinea: Inputs.select(["Todas", ...aerolineasLista], {label: "Aerolínea"}),
  categoria: Inputs.select(["Todas", ...categoriasLista], {label: "Tipo de avión", format: (c) => CATEGORIAS[c] ?? c}),
  movimiento: Inputs.radio(["Ambos", "aterrizaje", "despegue"], {label: "Movimiento", value: "Ambos"}),
  metrica: Inputs.radio(new Map([["Movimientos", "movimientos"], ["Pasajeros", "pasajeros"]]), {label: "Medir", value: "movimientos"})
}));
```

```js
const f = base.filter((d) =>
  filtros.anios.includes(d.anio)
  && filtros.segmentos.some((s) => s.id === d.segmento)
  && (filtros.aerolinea === "Todas" || d.aerolinea_nombre === filtros.aerolinea)
  && (filtros.categoria === "Todas" || d.aeronave_categoria === filtros.categoria)
  && (filtros.movimiento === "Ambos" || d.tipo_movimiento === filtros.movimiento));
const m = filtros.metrica;
const total = d3.sum(f, (d) => d[m]);
```

<div class="card"><h2>Total con estos filtros</h2><span class="big">${entero(total)}</span> <span class="muted">${m === "movimientos" ? "aterrizajes y despegues" : "pasajeros"}</span></div>

<div class="grid grid-cols-2">
  <div class="card">${resize((width) => Plot.plot({
    title: "Por mes", width, height: 240, marginLeft: 50,
    x: {domain: d3.range(1, 13), tickFormat: (i) => MESES[i - 1], label: null},
    y: {grid: true, tickFormat: entero, label: null},
    marks: [Plot.barY(f, Plot.groupX({y: "sum"}, {x: "mes", y: m, fill: FOCO, inset: 1, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Por día de la semana", width, height: 240, marginLeft: 50,
    x: {domain: d3.range(1, 8), tickFormat: (i) => DIAS[i - 1], label: null},
    y: {grid: true, tickFormat: entero, label: null},
    marks: [Plot.barY(f, Plot.groupX({y: "sum"}, {x: "dia_semana", y: m, fill: FOCO, inset: 1, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Por hora local", width, height: 240, marginLeft: 50,
    x: {domain: d3.range(0, 24), tickFormat: (h) => (h % 3 === 0 ? `${h}h` : ""), label: null},
    y: {grid: true, tickFormat: entero, label: null},
    marks: [Plot.barY(f.filter((d) => d.hora_local != null), Plot.groupX({y: "sum"}, {x: "hora_local", y: m, fill: FOCO, inset: 1, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Tipo de vuelo", width, height: 240, marginLeft: 170,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f, Plot.groupY({x: "sum"}, {y: (d) => CLASES[d.clase_vuelo] ?? d.clase_vuelo, x: m, fill: FOCO, sort: {y: "-x"}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Orígenes y destinos (top 12)", width, height: 300, marginLeft: 60,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f.filter((d) => d.origen_destino), Plot.groupY({x: "sum"}, {y: "origen_destino", x: m, fill: FOCO, sort: {y: "-x", limit: 12}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Aviones (top 12)", width, height: 300, marginLeft: 170,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f, Plot.groupY({x: "sum"}, {y: "aeronave_familia", x: m, fill: FOCO, sort: {y: "-x", limit: 12}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}</div>
</div>

<p class="muted">Los códigos de origen/destino son los de ANAC (AER = Aeroparque, CBA = Córdoba, DOZ = Mendoza, BCA = Bahía Blanca...). Datos provisorios en los últimos meses.</p>
