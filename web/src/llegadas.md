---
title: Cómo llega la gente
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, CAT, OTRO, entero, pct, pct1, variacion, compacto, MESES, ALTO, ejeAnios} from "./components/util.js";
```

```js
const turismo = await FileAttachment("data/mdq_turismo.json").json();
const medios = await FileAttachment("data/mdq_arribos_medio.json").json();
const procedencia = await FileAttachment("data/mdq_procedencia.json").json();
const evyth = await FileAttachment("data/evyth_medio.json").json();
```

```js
// Turistas (EMTUR) por año: solo años con los 12 meses.
const turAnual = d3.rollups(turismo, (v) => ({turistas: d3.sum(v, (d) => d.turistas), meses: v.filter((d) => d.turistas > 0).length}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12).sort((a, b) => a.anio - b.anio);
const tur = turAnual.at(-1);

// EMTUR por medio de transporte, por año.
const VIAS = [
  {id: "auto", nombre: "Auto", color: TINTA_2},
  {id: "omnibus", nombre: "Ómnibus", color: TINTA},
  {id: "tren", nombre: "Tren", color: CAT[2]},
  {id: "avion", nombre: "Avión", color: ACENTO}
];
const VIA_NOMBRE = Object.fromEntries(VIAS.map((v) => [v.id, v.nombre]));
const medAnual = d3.rollups(medios, (v) => ({
    meses: v.length,
    ...Object.fromEntries(VIAS.map((x) => [x.id, d3.sum(v, (d) => d[x.id])])),
    total: d3.sum(v, (d) => d.total_medios),
    avion_anac: d3.sum(v, (d) => d.avion_anac ?? NaN),
    micro_cnrt: d3.sum(v, (d) => d.micro_cnrt ?? NaN),
    tren_cnrt: d3.sum(v, (d) => d.tren_cnrt_ida_vuelta ?? NaN),
    meses_anac: v.filter((d) => d.avion_anac != null).length,
    meses_micro: v.filter((d) => d.micro_cnrt != null).length,
    meses_tren: v.filter((d) => d.tren_cnrt_ida_vuelta != null).length
  }), (d) => d.anio).map(([anio, v]) => ({anio, ...v})).sort((a, b) => a.anio - b.anio);
const ref = medAnual.filter((d) => d.meses === 12).at(-1);
const share = (d, id) => d[id] / d.total;
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · todas las vías</p><h1>Cómo llega <em>la gente</em></h1></div>
  <p class="bajada">Mar del Plata recibe más de ocho millones de turistas por año. El municipio (EMTUR) los estima mes a mes y por medio de transporte; acá se muestra ese reparto, de dónde vienen y qué tan cerca está cada vía de lo que se cuenta.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Turistas en ${ref.anio}</span><span class="valor">${compacto(ref.total)}</span><p class="nota">${(() => { const p = medAnual.find((d) => d.anio === ref.anio - 1 && d.meses === 12); return p ? `${variacion(ref.total / p.total - 1)} contra ${p.anio} · ` : ""; })()}EMTUR</p></div>
  <div><span class="rotulo">Llegaron en auto</span><span class="valor">${pct(share(ref, "auto"))}</span><p class="nota">${compacto(ref.auto)} turistas en ${ref.anio}</p></div>
  <div><span class="rotulo">Ómnibus · tren · avión</span><span class="valor">${pct(share(ref, "omnibus"))} · ${pct(share(ref, "tren"))} · ${pct(share(ref, "avion"))}</span><p class="nota">${compacto(ref.omnibus)} · ${compacto(ref.tren)} · ${compacto(ref.avion)} en ${ref.anio}</p></div>
</div>

### Por qué vía llegan

```js
const largo = medAnual.flatMap((d) => VIAS.map((v) => ({anio: d.anio, via: v.nombre, orden: VIAS.indexOf(v), valor: d[v.id], share: d[v.id] / d.total, meses: d.meses})));
display(Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Turistas por año (EMTUR)", tickFormat: compacto},
  x: ejeAnios,
  color: {domain: VIAS.map((v) => v.nombre), range: VIAS.map((v) => v.color), legend: true},
  marks: [
    Plot.barY(largo, {x: "anio", y: "valor", fill: "via", order: "orden", fillOpacity: (d) => (d.meses === 12 ? 1 : 0.45), inset: 1.5, tip: true,
      title: (d) => `${d.anio} · ${d.via}\n${entero(d.valor)} turistas (${pct1(d.share)})${d.meses === 12 ? "" : `\nsolo ${d.meses} meses publicados`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Barra clara: 2020, con solo enero a marzo y diciembre publicados. El auto es la vía de siempre: entre ${pct(d3.min(medAnual.filter((d) => d.meses === 12), (d) => share(d, "auto")))} y ${pct(d3.max(medAnual.filter((d) => d.meses === 12), (d) => share(d, "auto")))} de los turistas cada año desde ${medAnual[0].anio}.</p>

### La temporada, vía por vía

```js
const mesesRef = medios.filter((d) => d.anio === ref.anio);
const forma = VIAS.flatMap((v) => {
  const m = d3.mean(mesesRef, (d) => d[v.id]);
  return mesesRef.map((d) => ({mes: d.mes, via: v.nombre, valor: d[v.id] / m, crudo: d[v.id]}));
});
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  y: {grid: true, label: "Respecto del mes promedio de cada vía", tickFormat: (v) => `${Math.round(v * 100)} %`},
  x: {label: null, domain: d3.range(1, 13), tickFormat: (m) => MESES[m - 1], type: "point"},
  color: {domain: VIAS.map((v) => v.nombre), range: VIAS.map((v) => v.color), legend: true},
  marks: [
    Plot.ruleY([1], {stroke: "#d6d3cb"}),
    Plot.lineY(forma, {x: "mes", y: "valor", stroke: "via", strokeWidth: 2}),
    Plot.dot(forma, {x: "mes", y: "valor", fill: "via", r: 2.5, tip: true,
      title: (d) => `${d.via} · ${MESES[d.mes - 1]} ${ref.anio}\n${entero(d.crudo)} turistas (${Math.round(d.valor * 100)} % del mes promedio)`})
  ]
}));
```

<p class="leyenda">Año ${ref.anio}. 100 % = el mes promedio de cada vía: se comparan formas, no tamaños. ${(() => { const pico = VIAS.map((v) => ({v: v.nombre, p: d3.max(forma.filter((d) => d.via === v.nombre), (d) => d.valor)})).sort((a, b) => b.p - a.p); return `El mes más alto llega a ${pico.map((x) => `${Math.round(x.p * 100)} % en ${x.v.toLowerCase()}`).join(", ")} del mes promedio.`; })()}</p>

### De dónde vienen

```js
const REGIONES = ["CABA", "Conurbano", "Resto de la provincia", "Resto del país", "Exterior"];
const REG_COLOR = [TINTA, TINTA_2, CAT[2], CAT[1], ACENTO];
const procAnual = d3.rollups(procedencia.filter((d) => d.turistas != null), (v) => ({turistas: d3.sum(v, (d) => d.turistas), meses: new Set(v.map((d) => d.mes)).size}), (d) => d.anio, (d) => d.region)
  .flatMap(([anio, regs]) => {
    const tot = d3.sum(regs, ([, v]) => v.turistas);
    return regs.map(([region, v]) => ({anio, region, turistas: v.turistas, share: v.turistas / tot, meses: v.meses, orden: REGIONES.indexOf(region)}));
  });
const procUlt = d3.max(procAnual.filter((d) => d.meses === 12), (d) => d.anio);
const procRef = procAnual.filter((d) => d.anio === procUlt);
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Turistas según su lugar de residencia", tickFormat: (v) => `${Math.round(v * 100)} %`, domain: [0, 1]},
  x: ejeAnios,
  color: {domain: REGIONES, range: REG_COLOR, legend: true},
  marks: [
    Plot.barY(procAnual, {x: "anio", y: "share", fill: "region", order: "orden", fillOpacity: (d) => (d.meses === 12 ? 1 : 0.45), inset: 1, tip: true,
      title: (d) => `${d.anio} · ${d.region}\n${pct1(d.share)} (≈ ${compacto(d.turistas)} turistas)${d.meses === 12 ? "" : `\n${d.meses} meses publicados`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Cada mes, el % de cada región por la cantidad de turistas del mes. En ${procUlt}: ${procRef.sort((a, b) => b.share - a.share).map((d) => `${d.region} ${pct(d.share)}`).join(", ")}. Barras claras: años con meses sin publicar. ${procAnual.some((d) => d.anio === 2014) ? "La planilla de 2014 no está enlazada en el portal (repite la de 2013); se baja directo del servidor." : "Falta 2014: el portal enlaza la planilla de 2013 en su lugar."} "Exterior" no se publica todos los años.</p>

### Cómo arma el EMTUR estos números

```js
const val = medAnual.filter((d) => d.meses_anac === 12 || d.meses_micro === 12 || d.meses_tren === 12);
const dif = (a, b) => (Number.isFinite(a) && Number.isFinite(b) && b ? variacion(a / b - 1) : "—");
display(html`<table class="editorial"><thead><tr><th>Año</th><th>Avión EMTUR</th><th>ANAC (aterrizajes)</th><th>Dif.</th><th>Ómnibus EMTUR</th><th>CNRT (llegadas)</th><th>Dif.</th><th>Tren EMTUR</th><th>CNRT ÷ 2</th><th>Dif.</th></tr></thead><tbody>
${val.map((d) => html`<tr><td>${d.anio}</td>
  <td>${entero(d.avion)}</td><td>${d.meses_anac === 12 ? entero(d.avion_anac) : "—"}</td><td>${d.meses_anac === 12 ? dif(d.avion, d.avion_anac) : "—"}</td>
  <td>${entero(d.omnibus)}</td><td>${d.meses_micro === 12 ? entero(d.micro_cnrt) : "—"}</td><td>${d.meses_micro === 12 ? dif(d.omnibus, d.micro_cnrt) : "—"}</td>
  <td>${entero(d.tren)}</td><td>${d.meses_tren === 12 ? entero(d.tren_cnrt / 2) : "—"}</td><td>${d.meses_tren === 12 ? dif(d.tren, d.tren_cnrt / 2) : "—"}</td></tr>`)}
</tbody></table>`);
```

<p class="leyenda">Cada vía del EMTUR contra lo que se cuenta, en los años con los 12 meses de las dos fuentes. El avión coincide casi exacto con los pasajeros que aterrizan (ANAC): el EMTUR los toma de ahí. El tren queda cerca de la mitad de los pasajeros de la CNRT, con diferencias de hasta 11 %. En ómnibus la diferencia con la CNRT va de −10 % a +15 %: el EMTUR no dice qué fuente usa. El auto no tiene conteo: es la parte estimada del total.</p>

### Lo que responden los turistas

```js
const evAnios = [...new Set(evyth.map((d) => d.anio))].sort().slice(-3);
const evPool = evyth.filter((d) => evAnios.includes(d.anio));
const evShare = (medio) => d3.sum(evPool.filter((d) => d.medio === medio), (d) => d.turistas) / d3.sum(evPool, (d) => d.turistas);
const evRango = evAnios.length ? `${evAnios[0]}–${evAnios.at(-1)}` : "—";
const MEDIOS = [
  {id: "Auto", color: TINTA_2}, {id: "Ómnibus", color: TINTA}, {id: "Tren", color: CAT[2]},
  {id: "Avión", color: ACENTO}, {id: "Otros", color: OTRO}
];
const evRows = evyth.map((d) => ({...d, orden: MEDIOS.findIndex((m) => m.id === d.medio)}));
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Turistas residentes que viajaron a Mar del Plata", tickFormat: (v) => `${Math.round(v * 100)} %`, domain: [0, 1]},
  x: ejeAnios,
  color: {domain: MEDIOS.map((m) => m.id), range: MEDIOS.map((m) => m.color), legend: true},
  marks: [
    Plot.barY(evRows, {x: "anio", y: "share", fill: "medio", order: "orden", fillOpacity: (d) => (d.anio_completo ? 1 : 0.45), inset: 1, tip: true,
      title: (d) => `${d.anio} · ${d.medio}\n${pct1(d.share)} de los turistas (≈ ${compacto(d.turistas)})\n${entero(d.n)} encuestados${d.n < 30 ? " · muestra chica, estimación poco precisa" : ""}${d.anio_completo ? "" : `\nsolo ${d.trimestres} trimestres`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Otra fuente, otra pregunta: la Encuesta de Viajes y Turismo de los Hogares (EVyTH, Ministerio de Turismo) pregunta a residentes de los grandes aglomerados con qué medio llegaron. En ${evRango}, juntos: ${pct(evShare("Auto"))} en auto, ${pct(evShare("Ómnibus"))} en ómnibus, ${pct(evShare("Tren"))} en tren, ${pct(evShare("Avión"))} en avión. Da menos auto que el EMTUR: mide otra población (solo residentes de grandes aglomerados, solo turistas) y cada año se apoya en unos cientos de casos, así que un año suelto puede saltar (2021, 2023).</p>

<div class="leyenda-grid">
  <p><b>Turistas.</b> Estimación mensual del EMTUR (Ente Municipal de Turismo y Cultura) por medio de transporte, publicada en el portal de datos de Mar del Plata desde 2013. La suma de las cuatro vías es el total de turistas del mes.</p>
  <p><b>Procedencia.</b> % de turistas por región de residencia, por mes, también del EMTUR (desde 2007). Las cantidades por región son ese % por el total del mes.</p>
  <p><b>Qué incluye.</b> El EMTUR cuenta pasajeros que llegan, sin distinguir si viven en la ciudad: avión y tren salen de los conteos oficiales. Detalle en <a href="/metodologia">Metodología</a>.</p>
</div>
