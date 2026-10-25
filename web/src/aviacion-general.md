---
title: Toda la aviación
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import * as Inputs from "@observablehq/inputs";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, OTRO, SEQ, SEGMENTOS, SEG_NOMBRE, SEG_COLOR, segColor, entero, pct, decimal1,
  MESES, DIAS, CATEGORIAS, PERFILES, PERFIL_NOMBRE, perfilColor, datos, columnas, ALTO, ejeAnios, fechaEje} from "./components/util.js";
```

```js
const segMensual = datos(FileAttachment("data/mdq_segmentos_mensual.json"));
const segAnual = datos(FileAttachment("data/mdq_segmentos_anual.json"));
const avionTipico = datos(FileAttachment("data/mdq_avion_tipico.json"));
const operadores = datos(FileAttachment("data/mdq_operadores.json"));
const historiaSeg = datos(FileAttachment("data/mdq_historia_segmentos.json"));
const perfilAero = datos(FileAttachment("data/mdq_perfil_aeronave.json"));
const base = columnas(FileAttachment("data/mdq_explorador.json"));
```

<div class="portada" style="padding-top:6vh">
  <div>
    <span class="idx">Más allá de las aerolíneas</span>
    <h1>Toda la <em>aviación</em></h1>
    <p class="bajada">Taxis aéreos, aviones privados, vuelos oficiales y militares, escuelas de vuelo y trabajo aéreo: la otra mitad de la pista.</p>
  </div>
  <div>

```js
const aniosDisp = [...new Set(segAnual.map((d) => d.anio))].sort();
const anioSel = view(Inputs.select(aniosDisp.slice().reverse(), {label: "Año", format: String, value: aniosDisp.filter((a) => segAnual.filter((d) => d.anio === a).length >= 5).at(-2) ?? aniosDisp.at(-1)}));
```

```js
const opciones = SEGMENTOS.filter((s) => !["linea_regular"].includes(s.id));
const segSel = view(Inputs.radio(opciones, {label: "Segmento", format: (s) => s.nombre, value: opciones[0]}));
```

  </div>
</div>

```js
const perfil = segAnual.find((d) => d.anio === anioSel && d.segmento === segSel.id);
const totalAnio = d3.sum(segAnual.filter((d) => d.anio === anioSel), (d) => d.movimientos);
```

<h2 data-idx="Perfil del segmento">${segSel.nombre} en ${anioSel}</h2>

```js
perfil ? html`<div class="cifras">
  <div><span class="rotulo">Movimientos</span><span class="valor">${entero(perfil.movimientos)}</span><p class="nota">${pct(perfil.movimientos / totalAnio)} de la pista</p></div>
  <div><span class="rotulo">Pasajeros</span><span class="valor">${entero(perfil.pasajeros)}</span><p class="nota">${decimal1(perfil.pax_por_movimiento)} por movimiento</p></div>
  <div><span class="rotulo">Operadores distintos</span><span class="valor">${perfil.operadores}</span><p class="nota">${perfil.origenes_destinos} orígenes/destinos distintos</p></div>
  <div><span class="rotulo">Vuelos locales</span><span class="valor">${pct(perfil.share_vuelos_locales)}</span><p class="nota">despegan y aterrizan en MDQ</p></div>
</div>
<div class="cifras c3">
  <div><span class="rotulo">Fin de semana o feriado</span><span class="valor">${pct(perfil.share_finde_feriado)}</span></div>
  <div><span class="rotulo">En temporada de verano</span><span class="valor">${pct(perfil.share_temporada_verano)}</span></div>
  <div><span class="rotulo">Hora más frecuente</span><span class="valor">${perfil.hora_mas_frecuente}h</span></div>
</div>` : html`<p class="muted">Sin movimientos de este segmento en ${anioSel}.</p>`
```

### Mes a mes

```js
const serie = segMensual.filter((d) => d.segmento === segSel.id);
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 45,
  y: {grid: true, label: "Movimientos por mes", tickFormat: entero},
  x: {label: null, tickFormat: fechaEje},
  marks: [
    Plot.rectY(serie, {x1: "periodo", x2: (d) => d3.utcMonth.offset(d.periodo, 1), y: "movimientos", fill: SEG_COLOR[segSel.id], inset: 0.5, tip: true,
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\n${entero(d.movimientos)} movimientos\n${entero(d.movimientos_locales)} locales`}),
    Plot.ruleY([0])
  ]
})
```

### Con qué vuela

<p class="intro-ancha">De más pesado a más liviano: jets ejecutivos (Learjet, Citation), turbohélices (King Air, Caravan: el <b>avión básico</b> del taxi aéreo), pistones de 6 o más plazas (Seneca, Navajo, Baron) y pistones livianos, los de los privados y las escuelas de vuelo.</p>

```js
const perfAnio = perfilAero.filter((d) => d.anio === anioSel && ["taxi_aereo", "privado", "instruccion", "oficial"].includes(d.segmento));
const perfSeg = perfilAero.filter((d) => d.anio === anioSel && d.segmento === segSel.id);
const share = (id) => d3.sum(perfSeg.filter((d) => d.perfil === id), (d) => d.share_en_segmento);
```

```js
perfSeg.length ? html`<div class="cifras">
  <div><span class="rotulo">Jet ejecutivo</span><span class="valor">${pct(share("jet_ejecutivo"))}</span><p class="nota">de los movimientos del segmento</p></div>
  <div><span class="rotulo">Turbohélice</span><span class="valor">${pct(share("turbohelice"))}</span><p class="nota">el avión básico del taxi aéreo</p></div>
  <div><span class="rotulo">Pistón</span><span class="valor">${pct(share("piston_6") + share("piston_liviano"))}</span><p class="nota">${pct(share("piston_6"))} de 6+ plazas · ${pct(share("piston_liviano"))} liviano</p></div>
  <div><span class="rotulo">Modelo desconocido</span><span class="valor">${pct(share("sin_dato"))}</span><p class="nota">vuelos sin avión informado</p></div>
</div>` : ""
```

```js
Plot.plot({
  title: `Perfil de aeronave por segmento · ${anioSel}`,
  width, height: ALTO.medio, marginLeft: 140,
  x: {label: "% de los movimientos del segmento", tickFormat: "%", domain: [0, 1]},
  y: {label: null, domain: ["Taxi aéreo", "Privado", "Escuelas de vuelo", "Oficial y militar"]},
  color: {...perfilColor, legend: true},
  marks: [
    Plot.barX(perfAnio, {y: (d) => SEG_NOMBRE[d.segmento], x: "share_en_segmento", fill: (d) => PERFIL_NOMBRE[d.perfil] ?? d.perfil,
      order: perfilColor.domain, tip: true,
      title: (d) => `${SEG_NOMBRE[d.segmento]} · ${PERFIL_NOMBRE[d.perfil]}\n${entero(d.movimientos)} movimientos (${pct(d.share_en_segmento)})\n${decimal1(d.pax_promedio ?? 0)} pax promedio`})
  ]
})
```

### El avión típico

Las familias de aviones con más movimientos en ${anioSel}. Resaltado, el avión básico.

```js
const tipicos = avionTipico.filter((d) => d.anio === anioSel && d.segmento === segSel.id).sort((a, b) => a.ranking - b.ranking);
```

```js
tipicos.length ? html`<table class="editorial"><thead><tr><th>Familia</th><th>Tipo</th><th>Perfil</th><th>Movimientos</th><th>% del segmento</th><th>Pasajeros</th><th>Pax prom.</th><th>Lleva hasta</th><th>En tierra</th><th>Vuelo</th><th>Hora</th><th>Orígenes/destinos</th></tr></thead><tbody>
${tipicos.map((d) => html`<tr class=${d.perfil === "turbohelice" && d.ranking_en_perfil === 1 ? "foco" : ""}><td>${d.aeronave_familia}</td><td>${CATEGORIAS[d.aeronave_categoria] ?? d.aeronave_categoria}</td><td>${PERFIL_NOMBRE[d.perfil] ?? "—"}</td><td>${entero(d.movimientos)}</td><td>${pct(d.share_en_segmento)}</td><td>${entero(d.pasajeros)}</td><td>${decimal1(d.pax_promedio)}</td><td>${d.capacidad_observada_p95 ?? "—"}</td><td>${d.tiempo_en_tierra_mediano_min != null ? `${Math.round(d.tiempo_en_tierra_mediano_min)} min` : "—"}</td><td>${d.duracion_vuelo_mediana_min != null ? `${Math.round(d.duracion_vuelo_mediana_min)} min` : "—"}</td><td>${d.hora_mas_frecuente}h</td><td>${d.principales_origenes_destinos ?? "—"}</td></tr>`)}
</tbody></table>` : html`<p class="muted">Sin datos de aeronave para este segmento.</p>`
```

### Quién vuela y desde dónde

```js
const ops = operadores.filter((d) => d.anio === anioSel && d.segmento === segSel.id);
```

<div class="grid-2">
<div>

```js
Plot.plot({
  title: "Operadores",
  width: width / 2 - 20,
  height: ALTO.medio,
  marginLeft: 220,
  x: {grid: true, label: "Movimientos", tickFormat: entero},
  y: {label: null},
  marks: [Plot.barX(ops.filter((d) => d.dimension === "operador" && d.valor !== "Sin dato"), {x: "movimientos", y: "valor", sort: {y: "-x"}, fill: SEG_COLOR[segSel.id], inset: 1, tip: true}), Plot.ruleX([0])]
})
```

```js
const sinOp = d3.sum(ops.filter((d) => d.dimension === "operador" && d.valor === "Sin dato"), (d) => d.movimientos);
const totOp = perfil?.movimientos ?? d3.sum(ops.filter((d) => d.dimension === "operador"), (d) => d.movimientos);
```

${sinOp ? html`<p class="leyenda">Además, ${entero(sinOp)} movimientos (${pct(sinOp / totOp)}) sin operador informado.</p>` : ""}

</div>
<div>

```js
Plot.plot({
  title: "Orígenes y destinos",
  width: width / 2 - 20,
  height: ALTO.medio,
  marginLeft: 220,
  x: {grid: true, label: "Movimientos", tickFormat: entero},
  y: {label: null},
  marks: [Plot.barX(ops.filter((d) => d.dimension === "origen_destino"), {x: "movimientos", y: "valor", sort: {y: "-x"}, fill: SEG_COLOR[segSel.id], inset: 1, tip: true}), Plot.ruleX([0])]
})
```

</div>
</div>

### Cuándo vuela

```js
const celdas = d3.rollups(base.filter((d) => d.anio === anioSel && d.segmento === segSel.id && d.hora_local != null), (v) => d3.sum(v, (d) => d.movimientos), (d) => d.dia_semana, (d) => d.hora_local)
  .flatMap(([dia, hs]) => hs.map(([hora, movimientos]) => ({dia, hora, movimientos})));
```

```js
Plot.plot({
  width,
  height: ALTO.medio,
  padding: 0.06,
  x: {label: "Hora local", tickFormat: (h) => `${h}h`, domain: d3.range(0, 24)},
  y: {domain: d3.range(1, 8), tickFormat: (i) => DIAS[i - 1], label: null},
  color: {type: "linear", range: [SEQ[0], SEQ[4]], legend: true, label: `Movimientos en ${anioSel}`},
  marks: [Plot.cell(celdas, {x: "hora", y: "dia", fill: "movimientos", rx: 1, tip: true, title: (d) => `${DIAS[d.dia - 1]} ${d.hora}h: ${entero(d.movimientos)}`})]
})
```

<h2 data-idx="Comparación">Todos los segmentos, año por año</h2>

```js
const comp = segAnual.map((d) => ({...d, nombre: SEG_NOMBRE[d.segmento] ?? d.segmento}));
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 50,
  marginBottom: 45,
  y: {grid: true, label: "Movimientos por año", tickFormat: entero},
  x: ejeAnios,
  color: {...segColor, legend: true},
  marks: [
    Plot.barY(comp, Plot.stackY({x: "anio", y: "movimientos", fill: "nombre", order: segColor.domain, inset: 0.5, tip: true,
      title: (d) => `${d.nombre} ${d.anio}\n${entero(d.movimientos)} movimientos (${pct(d.share_movimientos)})`})),
    Plot.ruleY([0])
  ]
})
```

<p class="leyenda">Cómo se arma cada segmento y qué se hace con los datos incompletos: <a href="./metodologia">Metodología</a>.</p>
