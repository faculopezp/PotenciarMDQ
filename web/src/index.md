---
title: PotenciarMDQ
toc: false
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, OTRO, entero, pct, pct1, compacto, variacion, datos, ultimoAnioCompleto} from "./components/util.js";
```

```js
const anual = datos(FileAttachment("data/mdq_anual.json"));
const turismo = datos(FileAttachment("data/mdq_turismo.json"));
const bus = FileAttachment("data/bus_anual.json").json();
const tren = FileAttachment("data/tren_anual.json").json();
```

```js
// Turistas (EMTUR) por año, solo años con los 12 meses.
const turAnual = d3.rollups(turismo, (v) => ({turistas: d3.sum(v, (d) => d.turistas), aereos: d3.sum(v, (d) => d.llegados_aereos ?? 0), meses: v.filter((d) => d.turistas > 0).length}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12).sort((a, b) => a.anio - b.anio);
const tur = turAnual.at(-1);
const turPrev = turAnual.find((d) => d.anio === tur.anio - 1);
const av = ultimoAnioCompleto(anual);
const avPrev = anual.find((d) => d.anio === av.anio - 1);
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · datos abiertos</p><h1>Cómo se llega a <em>Mar del Plata</em></h1></div>
  <p class="bajada">Avión, micro, tren, auto y barco: cuánta gente llega por cada vía, cuándo y desde dónde. Todo con datos públicos, explicados y con su cobertura a la vista.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Turistas en ${tur.anio}</span><span class="valor">${compacto(tur.turistas)}</span><p class="nota">${turPrev ? `${variacion(tur.turistas / turPrev.turistas - 1)} contra ${turPrev.anio} · ` : ""}EMTUR</p></div>
  <div><span class="rotulo">Pasajeros aéreos en ${av.anio}</span><span class="valor">${compacto(av.pasajeros_comerciales)}</span><p class="nota">${avPrev ? `${variacion(av.pasajeros_comerciales / avPrev.pasajeros_comerciales - 1)} contra ${avPrev.anio} · ` : ""}ANAC</p></div>
  <div><span class="rotulo">Llegan en avión</span><span class="valor">${pct1(tur.aereos / tur.turistas)}</span><p class="nota">de los turistas de ${tur.anio} (estimado)</p></div>
</div>

```js
const modos = [
  {path: "/llegadas", titulo: "Cómo llega la gente", estado: "listo", texto: "Turistas por mes desde 2007 y qué parte llega por cada vía.",
   serie: turAnual.map((d) => ({x: d.anio, y: d.turistas}))},
  {path: "/aviacion/", titulo: "Aviación", estado: "listo", texto: "Cada aterrizaje y despegue desde 2019: aerolíneas, rutas, aviones, ocupación y toda la aviación general.",
   serie: anual.map((d) => ({x: d.anio, y: d.pasajeros_comerciales}))},
  {path: "/omnibus", titulo: "Ómnibus", estado: bus.length ? "listo" : "preparación", texto: "Micros de larga distancia desde 2019: cuántos llegan, desde dónde y en qué época (CNRT vía Yvera).",
   serie: bus.length ? d3.rollups(bus, (v) => (v.every((d) => d.anio_completo) ? d3.sum(v, (d) => d.pasajeros_llegada) : null), (d) => d.anio).filter(([, y]) => y).map(([x, y]) => ({x, y})).sort((a, b) => a.x - b.x) : null},
  {path: "/tren", titulo: "Tren", estado: tren.length ? "listo" : "preparación", texto: "El servicio Constitución–Mar del Plata: pasajeros por mes desde 2007 (CNRT).",
   serie: tren.length ? tren.filter((d) => d.anio_completo && d.pasajeros > 0).map((d) => ({x: d.anio, y: d.pasajeros})) : null},
  {path: "/autos", titulo: "Autos", estado: "listo", texto: "La vía de la mayoría, sin datos abiertos: lo que se sabe del tránsito por las rutas 2, 11 y 226."},
  {path: "/cruceros", titulo: "Cruceros", estado: "listo", texto: "Las pocas recaladas de cruceros en el puerto, una por una, con su fuente."}
];
const spark = (serie) => Plot.plot({width: 220, height: 48, axis: null, margin: 2,
  marks: [Plot.areaY(serie, {x: "x", y: "y", fill: ACENTO, fillOpacity: 0.12}), Plot.lineY(serie, {x: "x", y: "y", stroke: ACENTO, strokeWidth: 1.5})]});
```

```js
html`<div class="modos">${modos.map((m) => html`<a class=${`modo ${m.estado}`} href=${m.path}>
  <span class="modo-titulo">${m.titulo}</span>
  <p>${m.texto}</p>
  ${m.serie ? spark(m.serie) : m.estado === "listo" ? html`<span class="etiqueta">Ver</span>` : html`<span class="etiqueta">En preparación</span>`}
</a>`)}</div>`
```

<p class="leyenda">Fuentes: ANAC, CNRT, Yvera (Ministerio de Turismo), EMTUR y Municipio de General Pueyrredon. Cómo se arma cada número y qué tan completo es cada dato: <a href="/metodologia">Metodología</a>.</p>
