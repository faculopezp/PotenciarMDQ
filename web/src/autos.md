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
const medios = (await FileAttachment("data/mdq_arribos_medio.json").json()).map((d) => ({...d, periodo: new Date(`${d.periodo}T00:00:00Z`)}));
```

```js
// Turistas que llegan en auto según el EMTUR (por mes, desde 2013).
const autoAnual = d3.rollups(medios, (v) => ({auto: d3.sum(v, (d) => d.auto), total: d3.sum(v, (d) => d.total_medios), meses: v.length}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v, share: v.auto / v.total})).sort((a, b) => a.anio - b.anio);
const ref = autoAnual.filter((d) => d.meses === 12).at(-1);
const prev = autoAnual.find((d) => d.anio === ref.anio - 1 && d.meses === 12);
// Meses sin publicar como hueco (null), no como línea que los une.
const porMes = new Map(medios.map((d) => [+d.periodo, d]));
const serie = d3.utcMonth.range(medios[0].periodo, d3.utcMonth.offset(medios.at(-1).periodo, 1))
  .map((p) => porMes.get(+p) ?? {periodo: p, auto: null, total_medios: null});
const [c0, c1] = conteos.slice().sort((a, b) => a.desde.localeCompare(b.desde)).slice(-2);
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · rutas 2, 11 y 226</p><h1>Autos: <em>la mayoría</em>, sin conteos abiertos</h1></div>
  <p class="bajada">Ocho de cada diez turistas llegan en auto. El municipio lo estima mes a mes, pero nadie publica el tránsito de las rutas como datos abiertos. Esto es lo que se puede decir con lo que hay.</p>
</div>

<div class="cifras c3">
  <div><span class="rotulo">Llegaron en auto en ${ref.anio}</span><span class="valor">${compacto(ref.auto)}</span><p class="nota">${prev ? `${variacion(ref.auto / prev.auto - 1)} contra ${prev.anio} · ` : ""}EMTUR</p></div>
  <div><span class="rotulo">De cada 100 turistas</span><span class="valor">${Math.round(ref.share * 100)}</span><p class="nota">llegaron en auto en ${ref.anio}; entre ${pct(d3.min(autoAnual.filter((d) => d.meses === 12), (d) => d.share))} y ${pct(d3.max(autoAnual.filter((d) => d.meses === 12), (d) => d.share))} desde ${autoAnual[0].anio}</p></div>
  <div><span class="rotulo">Hacia la costa, ${c1?.periodo ?? "—"}</span><span class="valor">${c1 ? compacto(c1.vehiculos) : "—"}</span><p class="nota">${c0 && c1 ? `vehículos en las cabinas de AUBASA · ${variacion(c1.vehiculos / c0.vehiculos - 1)} contra ${c0.periodo.slice(-4)}` : ""}</p></div>
</div>

### Mes por mes

```js
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  y: {grid: true, label: "Turistas que llegaron en auto por mes (EMTUR)", tickFormat: compacto},
  x: {label: null, type: "utc"},
  marks: [
    Plot.areaY(serie, {x: "periodo", y: "auto", fill: TINTA_2, fillOpacity: 0.12}),
    Plot.lineY(serie, {x: "periodo", y: "auto", stroke: TINTA_2, strokeWidth: 1.5}),
    Plot.dot(medios, {x: "periodo", y: "auto", r: 0, tip: true,
      title: (d) => `${d.periodo.toLocaleDateString("es-AR", {month: "long", year: "numeric", timeZone: "UTC"})}\n${entero(d.auto)} en auto (${pct1(d.auto / d.total_medios)} de los turistas)`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Estimación del EMTUR, publicada en el portal de datos de Mar del Plata. Abril a noviembre de 2020 no se publicaron. En el resto de las vías el EMTUR usa conteos (ANAC, CNRT); el auto es la parte que estima, y no publica cómo (ver <a href="/llegadas">Cómo llega la gente</a>).</p>

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
  <p><b>Qué falta.</b> AUBASA cuenta cada vehículo en sus cabinas de peaje (rutas 2 y 11), pero solo difunde cifras sueltas en temporada. Vialidad Nacional publica el tránsito medio diario anual de la Ruta 226, que es el acceso desde el interior, no desde Buenos Aires.</p>
  <p><b>Otra mirada.</b> La encuesta de hogares del Ministerio de Turismo (EVyTH) da menos auto, porque mide solo a residentes de grandes ciudades: ver <a href="/llegadas">Cómo llega la gente</a>.</p>
  <p><b>Cómo mejorarlo.</b> Un pedido de acceso a la información a AUBASA (conteos por cabina, día y sentido) permitiría una serie como la de aviación. Ver <a href="/llegadas">Cómo llega la gente</a>.</p>
</div>
