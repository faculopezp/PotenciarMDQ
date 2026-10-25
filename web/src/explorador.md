---
title: Explorador
---


```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import * as Inputs from "@observablehq/inputs";
import {ACENTO, entero, MESES, DIAS, CATEGORIAS, CATEGORIA_COLOR, SEGMENTOS, SEG_NOMBRE, SEG_COLOR, segColor, columnas} from "./components/util.js";
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
  movimiento: Inputs.radio(["Ambos", "aterrizaje", "despegue"], {label: "Movimiento", value: "Ambos", format: (d) => ({Ambos: "Ambos", aterrizaje: "Aterrizajes", despegue: "Despegues"})[d]}),
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
// Categoría de cada familia según los vuelos con avión informado (2019–2020 vienen inferidos, sin categoría).
const colorFamilia = new Map(d3.rollups(base.filter((d) => d.aeronave_categoria !== "sin_dato"), (v) => d3.greatest(d3.rollups(v, (g) => g.length, (d) => d.aeronave_categoria), (x) => x[1])[0], (d) => d.aeronave_familia));
const total = d3.sum(f, (d) => d[m]);
// Movimientos sin modelo de avión: se muestran aparte, con el desglose de por qué faltan.
const sinModelo = f.filter((d) => d.aeronave_familia === "Sin dato");
const porSegmento = d3.rollups(sinModelo, (v) => d3.sum(v, (d) => d.movimientos), (d) => d.segmento).sort((a, b) => b[1] - a[1]);
const sinModeloNota = sinModelo.length ? html`<p class="leyenda">Además, ${entero(d3.sum(sinModelo, (d) => d.movimientos))} movimientos sin avión informado (${porSegmento.slice(0, 3).map(([s, n]) => `${SEGMENTOS.find((x) => x.id === s)?.nombre ?? s} ${entero(n)}`).join(" · ")}).</p>` : "";
```

<div class="card"><h2>Total con estos filtros</h2><span class="big">${entero(total)}</span> <span class="muted">${m === "movimientos" ? "aterrizajes y despegues" : "pasajeros"}</span></div>

<div class="grid grid-cols-3">
  <div class="card">${resize((width) => Plot.plot({
    title: "Por mes", width, height: 300, marginLeft: 50,
    x: {domain: d3.range(1, 13), tickFormat: (i) => MESES[i - 1], label: null},
    y: {grid: true, tickFormat: entero, label: null},
    color: segColor,
    marks: [Plot.barY(f, Plot.groupX({y: "sum"}, {x: "mes", y: m, fill: (d) => SEG_NOMBRE[d.segmento], order: segColor.domain, inset: 1, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Por día de la semana", width, height: 300, marginLeft: 50,
    x: {domain: d3.range(1, 8), tickFormat: (i) => DIAS[i - 1], label: null},
    y: {grid: true, tickFormat: entero, label: null},
    color: segColor,
    marks: [Plot.barY(f, Plot.groupX({y: "sum"}, {x: "dia_semana", y: m, fill: (d) => SEG_NOMBRE[d.segmento], order: segColor.domain, inset: 1, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Por hora local", width, height: 300, marginLeft: 50,
    x: {domain: d3.range(0, 24), tickFormat: (h) => (h % 3 === 0 ? `${h}h` : ""), label: null},
    y: {grid: true, tickFormat: entero, label: null},
    color: segColor,
    marks: [Plot.barY(f.filter((d) => d.hora_local != null), Plot.groupX({y: "sum"}, {x: "hora_local", y: m, fill: (d) => SEG_NOMBRE[d.segmento], order: segColor.domain, inset: 0.5, tip: true})), Plot.ruleY([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Por segmento", width, height: 300, marginLeft: 130,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f, Plot.groupY({x: "sum"}, {y: (d) => SEG_NOMBRE[d.segmento], x: m, fill: (d) => SEG_COLOR[d.segmento], sort: {y: "-x"}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Orígenes y destinos (top 12)", width, height: 300, marginLeft: 60,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f.filter((d) => d.origen_destino), Plot.groupY({x: "sum"}, {y: "origen_destino", x: m, fill: ACENTO, sort: {y: "-x", limit: 12}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}</div>
  <div class="card">${resize((width) => Plot.plot({
    title: "Aviones (top 12)", width, height: 300, marginLeft: 170,
    x: {grid: true, tickFormat: entero, label: null},
    y: {label: null},
    marks: [Plot.barX(f.filter((d) => d.aeronave_familia !== "Sin dato"), Plot.groupY({x: "sum", fill: "mode"}, {y: "aeronave_familia", x: m, fill: (d) => CATEGORIA_COLOR[d.aeronave_categoria === "sin_dato" ? colorFamilia.get(d.aeronave_familia) : d.aeronave_categoria] ?? "#a3a29c", sort: {y: "-x", limit: 12}, inset: 1, tip: true})), Plot.ruleX([0])]
  }))}${sinModeloNota}</div>
</div>

<div class="leyenda-colores">${SEGMENTOS.map((s) => html`<span><i style="background:${SEG_COLOR[s.id]}"></i>${s.nombre}</span>`)}</div>
<p class="leyenda">Colores de los aviones: azul oscuro jet ejecutivo · azul turbohélice · ámbar pistón · verde helicóptero · gris aviones de línea.</p>
</div>

<p class="leyenda">Códigos de origen/destino: AER = Aeroparque, EZE = Ezeiza, CBA = Córdoba, DOZ = Mendoza, BCA = Bahía Blanca, FDO = San Fernando, MOR = Morón. Los últimos meses pueden cambiar con la actualización mensual.</p>
