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
const bus = await FileAttachment("data/bus_anual.json").json();
const busMensual = await FileAttachment("data/bus_mensual.json").json();
const cruceros = await FileAttachment("data/cruceros.json").json();
const tren = await FileAttachment("data/tren_anual.json").json();
const trenMensual = await FileAttachment("data/tren_mensual.json").json();
const evyth = await FileAttachment("data/evyth_medio.json").json();
const evythOrigen = await FileAttachment("data/evyth_origen.json").json();
```

```js
// Turistas (EMTUR) y llegadas en avión (ANAC, aterrizajes de línea) por año: solo años con 12 meses.
const turAnual = d3.rollups(turismo, (v) => ({
    turistas: d3.sum(v, (d) => d.turistas),
    avion: d3.sum(v, (d) => d.llegados_aereos ?? 0),
    avion_anac: v.every((d) => d.fuente_llegados === "ANAC"),
    meses: v.filter((d) => d.turistas > 0).length
  }), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12).sort((a, b) => a.anio - b.anio);
const tur = turAnual.at(-1);

// Micros: llegadas por año y servicio; solo años que el archivo cubre entero.
const busAnio = d3.rollups(bus, (v) => ({
    regular: d3.sum(v.filter((d) => d.servicio === "regular"), (d) => d.pasajeros_llegada),
    turismo: d3.sum(v.filter((d) => d.servicio === "turismo"), (d) => d.pasajeros_llegada),
    completo: v.find((d) => d.servicio === "regular")?.anio_completo && v.find((d) => d.servicio === "turismo")?.anio_completo
  }), (d) => d.anio).map(([anio, v]) => ({anio, ...v}));
const crucerosAnio = d3.rollup(cruceros.filter((d) => d.estado === "realizada"), (v) => d3.sum(v, (d) => d.pasajeros ?? d.pasajeros_max ?? 0), (d) => +d.fecha.slice(0, 4));

// Años con todas las vías medidas (avión de ANAC y micros completos).
const comunes = turAnual.filter((t) => t.avion_anac && busAnio.find((b) => b.anio === t.anio && b.completo))
  .map((t) => {
    const b = busAnio.find((x) => x.anio === t.anio);
    // Tren: la CNRT da los pasajeros del servicio en los dos sentidos; llegadas ≈ la mitad.
    const tr = tren.find((x) => x.anio === t.anio && x.anio_completo);
    const trenLleg = tr ? Math.round(tr.pasajeros / 2) : 0;
    const medidas = t.avion + b.regular + b.turismo + trenLleg + (crucerosAnio.get(t.anio) ?? 0);
    return {...t, micro_regular: b.regular, micro_turismo: b.turismo, tren: trenLleg, crucero: crucerosAnio.get(t.anio) ?? 0, medidas};
  });
const ultimo = comunes.at(-1);
// EVyTH: un año suelto es volátil (pocos casos con factores de expansión muy distintos), así que
// la cifra principal agrupa los últimos tres años con datos.
const evAnios = [...new Set(evyth.map((d) => d.anio))].sort().slice(-3);
const evPool = evyth.filter((d) => evAnios.includes(d.anio));
const evShare = (medio) => d3.sum(evPool.filter((d) => d.medio === medio), (d) => d.turistas) / d3.sum(evPool, (d) => d.turistas);
const evRango = evAnios.length ? `${evAnios[0]}–${evAnios.at(-1)}` : "—";
const VIAS = [
  {id: "avion", nombre: "Avión (ANAC)", color: ACENTO},
  {id: "micro_regular", nombre: "Micro regular (CNRT)", color: TINTA},
  {id: "micro_turismo", nombre: "Micro de turismo (CNRT)", color: CAT[1]},
  {id: "tren", nombre: "Tren (CNRT, estimado)", color: CAT[2]},
  {id: "crucero", nombre: "Crucero", color: CAT[0]}
];
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · todas las vías</p><h1>Cómo llega <em>la gente</em></h1></div>
  <p class="bajada">Mar del Plata recibe millones de turistas por año. Acá se cruzan los turistas que estima el municipio con los pasajeros que llegan en avión, micro y barco, para ver qué parte explica cada vía.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Turistas en ${tur.anio}</span><span class="valor">${compacto(tur.turistas)}</span><p class="nota">EMTUR, todas las vías</p></div>
  <div><span class="rotulo">Llegaron en avión, micro, tren o barco en ${ultimo?.anio ?? "—"}</span><span class="valor">${ultimo ? compacto(ultimo.medidas) : "—"}</span><p class="nota">${ultimo ? `${pct(ultimo.medidas / ultimo.turistas)} de los turistas de ese año` : ""}</p></div>
  <div><span class="rotulo">En auto, según la encuesta</span><span class="valor">${evAnios.length ? pct(evShare("Auto")) : "—"}</span><p class="nota">de los turistas residentes, ${evRango} (EVyTH) · ómnibus ${pct(evShare("Ómnibus"))} · tren ${pct(evShare("Tren"))} · avión ${pct(evShare("Avión"))}</p></div>
</div>

### Turistas por año

```js
Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Turistas por año (EMTUR)", tickFormat: compacto},
  x: ejeAnios,
  marks: [
    Plot.barY(turAnual, {x: "anio", y: "turistas", fill: (d) => (d.anio === tur.anio ? ACENTO : TINTA), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${entero(d.turistas)} turistas`}),
    Plot.ruleY([0])
  ]
})
```

### Qué parte llega por cada vía

```js
const largo = comunes.flatMap((d) => VIAS.map((v) => ({anio: d.anio, via: v.nombre, valor: d[v.id], share: d[v.id] / d.turistas})));
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Pasajeros que llegaron por año", tickFormat: compacto},
  x: ejeAnios,
  color: {domain: VIAS.map((v) => v.nombre), range: VIAS.map((v) => v.color), legend: true},
  marks: [
    Plot.barY(largo, {x: "anio", y: "valor", fill: "via", inset: 1.5, tip: true,
      title: (d) => `${d.anio} · ${d.via}\n${entero(d.valor)} pasajeros (${pct1(d.share)} de los turistas)`}),
    Plot.ruleY([0])
  ]
}));
```

```js
html`<table class="editorial"><thead><tr><th>Año</th><th>Turistas (EMTUR)</th>${VIAS.map((v) => html`<th>${v.nombre}</th>`)}<th>Medidas / turistas</th></tr></thead><tbody>
${comunes.map((d) => html`<tr><td>${d.anio}</td><td>${entero(d.turistas)}</td>${VIAS.map((v) => html`<td>${entero(d[v.id])}</td>`)}<td>${pct(d.medidas / d.turistas)}</td></tr>`)}
</tbody></table>`
```

<p class="leyenda">Conteos de pasajeros contra turistas estimados: solo los años en que todas las vías medidas tienen el año entero. Tren: la CNRT informa los pasajeros pagos del servicio en los dos sentidos y con estaciones intermedias; se toma la mitad como estimación de llegadas. Para el auto no hay series abiertas: el último reparto publicado por el municipio (enero de 2018) daba 77 % en auto, 18 % en micro, 2,4 % en avión y 2,3 % en tren (<a href="https://nulan.mdp.edu.ar/id/eprint/3911/1/roldan-etal-2023.pdf" target="_blank" rel="noopener">citado por la UNMdP</a>).</p>

### Lo que responden los turistas

```js
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

<p class="leyenda">Encuesta de Viajes y Turismo de los Hogares (EVyTH, Ministerio de Turismo): residentes de los grandes aglomerados urbanos que viajaron a Mar del Plata y pasaron al menos una noche, según el medio con que llegaron. Es una encuesta: cada año se apoya en unos cientos de casos y algunos pesan mucho más que otros, así que un año suelto puede saltar (2021, 2023). Para una cifra, mejor varios años juntos: en ${evRango}, ${pct(evShare("Auto"))} en auto, ${pct(evShare("Ómnibus"))} en ómnibus, ${pct(evShare("Tren"))} en tren y ${pct(evShare("Avión"))} en avión. Barras claras: año con menos de cuatro trimestres.</p>

### La temporada, vía por vía

```js
// Cada serie como % de su propio promedio mensual, en el último año con las tres: así se comparan
// formas y no tamaños.
const mesesTur = turismo.filter((d) => d.anio === ultimo?.anio);
const mesesBus = d3.rollups(busMensual.filter((d) => d.anio === ultimo?.anio), (v) => d3.sum(v, (d) => d.pasajeros_llegada), (d) => d.mes)
  .map(([mes, pasajeros_llegada]) => ({mes, pasajeros_llegada})).sort((a, b) => a.mes - b.mes);
const mesesTren = trenMensual.filter((d) => d.anio === ultimo?.anio);
const indice = (rows, campo, nombre) => {
  const m = d3.mean(rows, (d) => d[campo]);
  return rows.map((d) => ({mes: d.mes, serie: nombre, valor: d[campo] / m, crudo: d[campo]}));
};
const forma = [
  ...indice(mesesTur, "turistas", "Turistas (EMTUR)"),
  ...indice(mesesTur, "llegados_aereos", "Avión"),
  ...(mesesBus.length === 12 ? indice(mesesBus, "pasajeros_llegada", "Micro") : []),
  ...(mesesTren.length === 12 ? indice(mesesTren, "pasajeros", "Tren") : [])
];
const SERIES = [{n: "Turistas (EMTUR)", c: TINTA_2}, {n: "Avión", c: ACENTO}, {n: "Micro", c: TINTA}, {n: "Tren", c: CAT[2]}];
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  y: {grid: true, label: "Respecto del mes promedio", tickFormat: (v) => `${Math.round(v * 100)} %`},
  x: {label: null, domain: d3.range(1, 13), tickFormat: (m) => MESES[m - 1], type: "point"},
  color: {domain: SERIES.map((s) => s.n), range: SERIES.map((s) => s.c), legend: true},
  marks: [
    Plot.ruleY([1], {stroke: "#d6d3cb"}),
    Plot.lineY(forma, {x: "mes", y: "valor", stroke: "serie", strokeWidth: 2}),
    Plot.dot(forma, {x: "mes", y: "valor", fill: "serie", r: 2.5, tip: true,
      title: (d) => `${d.serie} · ${MESES[d.mes - 1]} ${ultimo.anio}\n${entero(d.crudo)} (${Math.round(d.valor * 100)} % del mes promedio)`})
  ]
}));
```

<p class="leyenda">${ultimo ? `Año ${ultimo.anio}.` : ""} 100 % = el mes promedio de cada serie. Micro: regular y turismo juntos; tren: pasajeros del servicio.</p>

<div class="leyenda-grid">
  <p><b>Turistas.</b> Estimación mensual del EMTUR (Ente Municipal de Turismo y Cultura) de turistas arribados, por todas las vías. Es un modelo, no un conteo.</p>
  <p><b>Pasajeros.</b> Avión: aterrizajes de línea en el aeropuerto (ANAC). Micro: servicios de jurisdicción nacional con destino Mar del Plata (CNRT). Tren: mitad de los pasajeros pagos del servicio Constitución–Mar del Plata (CNRT). Crucero: recaladas registradas.</p>
  <p><b>Por qué no cierra.</b> Los pasajeros incluyen a marplatenses que vuelven a casa y los turistas incluyen a quienes llegan en auto, que no se miden. La relación entre ambas es una aproximación, no un reparto exacto.</p>
</div>
