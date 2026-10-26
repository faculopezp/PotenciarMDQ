---
title: Cruceros
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, OTRO, SIN_DATO, entero, MESES} from "./components/util.js";
```

```js
const cruceros = (await FileAttachment("data/cruceros.json").json())
  .map((d) => ({...d, fecha: new Date(`${d.fecha}T00:00:00Z`)}))
  .sort((a, b) => a.fecha - b.fecha);
const realizadas = cruceros.filter((d) => d.estado === "realizada");
const proximas = cruceros.filter((d) => d.estado === "programada");
const ESTADOS = [
  {id: "realizada", nombre: "Realizada", color: ACENTO},
  {id: "programada", nombre: "Programada", color: TINTA_2},
  {id: "cancelada", nombre: "Cancelada", color: OTRO},
  {id: "denegada", nombre: "No autorizada", color: SIN_DATO}
];
const NOMBRE = Object.fromEntries(ESTADOS.map((e) => [e.id, e.nombre]));
const fechaTxt = (d) => d.precision === "dia"
  ? d.fecha.toLocaleDateString("es-AR", {day: "numeric", month: "long", year: "numeric", timeZone: "UTC"})
  : `${MESES[d.fecha.getUTCMonth()]} ${d.fecha.getUTCFullYear()} (aprox.)`;
const paxTxt = (d) => d.pasajeros ? entero(d.pasajeros) : d.pasajeros_min ? `${entero(d.pasajeros_min)}–${entero(d.pasajeros_max)}` : "—";
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · puerto</p><h1>Cruceros: <em>pocos</em> y espaciados</h1></div>
  <p class="bajada">Mar del Plata tiene terminal de cruceros desde 2012, pero las recaladas se cuentan con los dedos: escalas sueltas de buques chicos y de expedición. Acá están todas las que encontramos, una por una.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Recaladas registradas</span><span class="valor">${realizadas.length}</span><p class="nota">desde la inauguración de la terminal</p></div>
  <div><span class="rotulo">Pasajeros, la mayor</span><span class="valor">${entero(d3.max(realizadas, (d) => d.pasajeros ?? d.pasajeros_max))}</span><p class="nota">un crucero grande lleva más de 3.000</p></div>
  <div><span class="rotulo">Próximas anunciadas</span><span class="valor">${proximas.length}</span><p class="nota">${proximas.map((d) => d.operador).filter((v, i, a) => a.indexOf(v) === i).join(" · ")}</p></div>
</div>

```js
Plot.plot({
  width,
  height: 180,
  marginLeft: 20,
  marginRight: 20,
  x: {label: null, type: "utc", domain: [new Date("2017-01-01"), new Date("2028-01-01")]},
  y: {axis: null, domain: [0, 1]},
  color: {domain: ESTADOS.map((e) => e.nombre), range: ESTADOS.map((e) => e.color), legend: true},
  marks: [
    Plot.ruleY([0.35], {stroke: "#d6d3cb"}),
    Plot.ruleX([new Date()], {stroke: TINTA, strokeDasharray: "2,3"}),
    Plot.text([new Date()], {x: (d) => d, y: 0.95, text: () => "hoy", fill: TINTA_2, fontSize: 11}),
    Plot.dot(cruceros, {x: "fecha", y: 0.35, r: (d) => d.estado === "realizada" ? 8 : 6, fill: (d) => NOMBRE[d.estado], stroke: "white", tip: true,
      title: (d) => `${d.buque} · ${d.operador}\n${fechaTxt(d)}\n${NOMBRE[d.estado]}${d.pasajeros || d.pasajeros_min ? `\n${paxTxt(d)} pasajeros` : ""}`}),
    // Rótulo solo para las realizadas (las demás, en el tooltip): sin superposiciones.
    Plot.text(realizadas.filter((d, i) => i % 2 === 0), {x: "fecha", y: 0.62, text: (d) => `${d.buque} · ${d.fecha.getUTCFullYear()}`, fill: TINTA, fontSize: 12}),
    Plot.text(realizadas.filter((d, i) => i % 2 === 1), {x: "fecha", y: 0.08, text: (d) => `${d.buque} · ${d.fecha.getUTCFullYear()}`, fill: TINTA, fontSize: 12})
  ]
})
```

### Una por una

```js
html`<table class="editorial texto"><thead><tr><th>Fecha</th><th>Estado</th><th>Buque</th><th>Naviera</th><th>Pasajeros</th><th>Recorrido</th><th>Detalle</th><th>Fuente</th></tr></thead><tbody>
${cruceros.slice().reverse().map((d) => html`<tr><td>${fechaTxt(d)}</td><td>${NOMBRE[d.estado]}</td><td>${d.buque}</td><td>${d.operador}</td><td>${paxTxt(d)}</td><td>${[d.origen, d.destino].filter(Boolean).join(" → ") || "—"}</td><td class="nota">${d.nota ?? ""}</td><td>${d.fuentes.map((f, i) => html`<a href=${f} target="_blank" rel="noopener">[${i + 1}]</a> `)}</td></tr>`)}
</tbody></table>`
```

<div class="leyenda-grid">
  <p><b>Por qué hay tan pocos.</b> El puerto es ante todo pesquero y de carga; el calado y el largo de los muelles no permiten recibir buques grandes, y el dragado pendiente se discute cada vez que llega uno.</p>
  <p><b>Qué llega.</b> Cruceros chicos (300 pasajeros) o de expedición (menos de 200) que usan Mar del Plata como escala camino a Ushuaia o la Antártida, a veces sin programar.</p>
  <p><b>De dónde sale.</b> No hay datos abiertos de cruceros: el Consorcio Portuario no publica series. Es un registro armado con notas de prensa, con la fuente de cada fila; cuando las notas difieren se muestra el rango.</p>
</div>
