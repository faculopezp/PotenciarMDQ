---
title: Autos
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, OTRO, entero, pct, pct1, variacion, compacto, ALTO, ejeAnios} from "./components/util.js";
```

```js
const conteos = await FileAttachment("data/autos.json").json();
const findes = await FileAttachment("data/mdq_findes_largos.json").json();
const turismo = await FileAttachment("data/mdq_turismo.json").json();
const bus = await FileAttachment("data/bus_anual.json").json();
const tren = await FileAttachment("data/tren_anual.json").json();
const evyth = await FileAttachment("data/evyth_medio.json").json();
```

```js
// Lo que no explican avión, micro ni tren: turistas (EMTUR) menos pasajeros que llegaron por esas vías,
// en los años con todo medido (misma cuenta que en "Cómo llega la gente").
const turAnual = d3.rollups(turismo, (v) => ({turistas: d3.sum(v, (d) => d.turistas), avion: d3.sum(v, (d) => d.llegados_aereos ?? 0),
    anac: v.every((d) => d.fuente_llegados === "ANAC"), meses: v.length}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12 && d.anac);
const resto = turAnual.map((t) => {
  const b = bus.filter((d) => d.anio === t.anio);
  if (b.length < 2 || !b.every((d) => d.anio_completo)) return null;
  const tr = tren.find((d) => d.anio === t.anio && d.anio_completo);
  if (!tr) return null;
  const micro = d3.sum(b, (d) => d.pasajeros_llegada);
  return {anio: t.anio, turistas: t.turistas, resto: t.turistas - t.avion - micro - tr.pasajeros / 2};
}).filter(Boolean);
const r = resto.at(-1);
// Tres años juntos: un año suelto de la encuesta es volátil (ver Cómo llega la gente).
const evAnios = [...new Set(evyth.map((d) => d.anio))].sort().slice(-3);
const evPool = evyth.filter((d) => evAnios.includes(d.anio));
const evAutoPool = d3.sum(evPool.filter((d) => d.medio === "Auto"), (d) => d.turistas) / d3.sum(evPool, (d) => d.turistas);
const evRango = evAnios.length ? `${evAnios[0]}–${evAnios.at(-1)}` : "—";
const evAuto = evyth.filter((d) => d.medio === "Auto");
const [c0, c1] = conteos.slice().sort((a, b) => a.desde.localeCompare(b.desde)).slice(-2);
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · rutas 2, 11 y 226</p><h1>Autos: <em>la mayoría</em>, sin datos abiertos</h1></div>
  <p class="bajada">La mayor parte de los turistas llega en auto, pero nadie publica el tránsito de las rutas como datos abiertos. Esto es lo que se puede decir con lo que hay.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Llegaron en auto, ${evRango}</span><span class="valor">${evAnios.length ? pct(evAutoPool) : "—"}</span><p class="nota">de los turistas residentes (EVyTH); en enero de 2018 el EMTUR estimó 77 % (<a href="https://nulan.mdp.edu.ar/id/eprint/3911/1/roldan-etal-2023.pdf" target="_blank" rel="noopener">vía UNMdP</a>)</p></div>
  <div><span class="rotulo">Turistas sin avión, micro ni tren, ${r?.anio ?? "—"}</span><span class="valor">${r ? pct(r.resto / r.turistas) : "—"}</span><p class="nota">${r ? `${compacto(r.resto)} de ${compacto(r.turistas)}: auto y otros` : ""}</p></div>
  <div><span class="rotulo">Hacia la costa, ${c1?.periodo ?? "—"}</span><span class="valor">${c1 ? compacto(c1.vehiculos) : "—"}</span><p class="nota">${c0 && c1 ? `vehículos en las cabinas de AUBASA · ${variacion(c1.vehiculos / c0.vehiculos - 1)} contra ${c0.periodo.slice(-4)}` : ""}</p></div>
</div>

### En auto, año por año

```js
display(Plot.plot({
  width,
  height: 260,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Turistas residentes que llegaron en auto (EVyTH)", tickFormat: (v) => `${Math.round(v * 100)} %`, domain: [0, 1]},
  x: ejeAnios,
  marks: [
    Plot.barY(evAuto, {x: "anio", y: "share", fill: TINTA, fillOpacity: (d) => (d.anio_completo ? 1 : 0.45), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${pct1(d.share)} en auto\n${entero(d.n)} encuestados${d.anio_completo ? "" : `\nsolo ${d.trimestres} trimestres`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Proporción de los turistas residentes en grandes aglomerados que viajaron a Mar del Plata y llegaron en auto propio. Un año suelto de la encuesta puede saltar por pocos casos con mucho peso. El resto, en <a href="/llegadas">Cómo llega la gente</a>.</p>

### Fines de semana largos

```js
const FERIADOS = d3.groupSort(findes, (v) => -d3.sum(v, (d) => d.visitantes), (d) => d.feriado).slice(0, 6);
const ultimos = findes.filter((d) => FERIADOS.includes(d.feriado));
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Visitantes en el fin de semana largo (EMTUR)", tickFormat: compacto},
  x: ejeAnios,
  color: {legend: true, domain: FERIADOS},
  marks: [
    Plot.lineY(ultimos, {x: "anio", y: "visitantes", stroke: "feriado", strokeWidth: 1.75}),
    Plot.dot(ultimos, {x: "anio", y: "visitantes", fill: "feriado", r: 2.5, tip: true,
      title: (d) => `${d.feriado} ${d.anio}\n${entero(d.visitantes)} visitantes`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Los fines de semana largos se viajan sobre todo en auto: es la mejor señal del tránsito que hay en datos abiertos. Visitantes estimados por el EMTUR, por feriado (los seis con más visitantes en la serie).</p>

### Lo que informó AUBASA

```js
html`<table class="editorial texto"><thead><tr><th>Período</th><th>Tramo</th><th>Sentido</th><th>Vehículos</th><th>Detalle</th><th>Fuente</th></tr></thead><tbody>
${conteos.map((d) => html`<tr><td>${d.periodo}</td><td>${d.tramo}</td><td>${d.sentido}</td><td>${entero(d.vehiculos)}</td><td class="nota">${d.nota ?? ""}</td><td>${d.fuentes.map((f, i) => html`<a href=${f} target="_blank" rel="noopener">[${i + 1}]</a> `)}</td></tr>`)}
</tbody></table>`
```

<div class="leyenda-grid">
  <p><b>Qué falta.</b> AUBASA cuenta cada vehículo en sus cabinas de peaje, pero solo difunde cifras sueltas en temporada. Vialidad Nacional publicó el tránsito medio diario de la Ruta 226 hasta 2017.</p>
  <p><b>El resto no medido.</b> Turistas del EMTUR menos los que llegaron en avión, micro y tren (la mitad de los pasajeros del servicio). Es una aproximación: los pasajeros incluyen marplatenses que vuelven.</p>
  <p><b>Cómo mejorarlo.</b> Un pedido de acceso a la información a AUBASA (conteos por cabina, día y sentido) permitiría una serie como la de aviación. Ver <a href="/llegadas">Cómo llega la gente</a>.</p>
</div>
