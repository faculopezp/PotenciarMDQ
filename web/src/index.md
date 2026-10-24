---
title: Mar del Plata despega
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import * as Inputs from "@observablehq/inputs";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, CAT, OTRO, SEQ, DIV, SEGMENTOS, SEG_NOMBRE, SEG_COLOR, segColor,
  entero, pct, pct1, variacion, decimal1, compacto, MESES, DIAS, datos, ultimoAnioCompleto,
  veranosCompletos, topN, fechaLarga} from "./components/util.js";
```

```js
const anual = datos(FileAttachment("data/mdq_anual.json"));
const mensual = datos(FileAttachment("data/mdq_mensual.json"));
const diario = datos(FileAttachment("data/mdq_diario.json"));
const horaSemana = datos(FileAttachment("data/mdq_hora_semana.json"));
const aerolineas = datos(FileAttachment("data/mdq_aerolineas.json"));
const rutas = datos(FileAttachment("data/mdq_rutas.json"));
const destinos = datos(FileAttachment("data/mdq_destinos.json"));
const verano = datos(FileAttachment("data/mdq_verano.json"));
const rotaciones = datos(FileAttachment("data/mdq_rotaciones.json"));
const tramos = datos(FileAttachment("data/mdq_tramos.json"));
const pares = datos(FileAttachment("data/benchmark_pares.json"));
const serieLarga = datos(FileAttachment("data/mdq_serie_larga.json"));
const tendencia = datos(FileAttachment("data/mdq_tendencia.json"));
const turismo = datos(FileAttachment("data/mdq_turismo.json"));
const segMensual = datos(FileAttachment("data/mdq_segmentos_mensual.json"));
const segAnual = datos(FileAttachment("data/mdq_segmentos_anual.json"));
const avionTipico = datos(FileAttachment("data/mdq_avion_tipico.json"));
const aeronavesM = datos(FileAttachment("data/mdq_aeronaves.json"));
const historiaSeg = datos(FileAttachment("data/mdq_historia_segmentos.json"));
const ranking = datos(FileAttachment("data/ranking_nacional.json"));
const red = datos(FileAttachment("data/red_aeropuertos.json"));
const atipicos = datos(FileAttachment("data/mdq_dias_atipicos.json"));
const pronostico = datos(FileAttachment("data/mdq_pronostico.json"));
const paises = FileAttachment("data/sudamerica.json").json();
const hitos = FileAttachment("data/hitos.json").json();
const eventos = FileAttachment("data/eventos.json").json();
```

```js
const ref = ultimoAnioCompleto(anual);
const anios = anual.map((d) => d.anio);
const largaAnual = d3.rollups(serieLarga, (v) => ({pasajeros: d3.sum(v, (d) => d.pasajeros), movimientos: d3.sum(v, (d) => d.movimientos_comerciales), meses: v.length, fuente: v[0].fuente}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12);
const record = d3.greatest(largaAnual, (d) => d.pasajeros);
const turAnual = d3.rollups(turismo.filter((d) => d.llegados_aereos != null), (v) => ({turistas: d3.sum(v, (d) => d.turistas), llegados: d3.sum(v, (d) => d.llegados_aereos), meses: v.length}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v, share: v.llegados / v.turistas})).filter((d) => d.meses === 12);
const turRef = turAnual.find((d) => d.anio === ref.anio) ?? turAnual.at(-1);
const segRef = segAnual.filter((d) => d.anio === ref.anio);
const noLinea = d3.sum(segRef.filter((d) => !["linea_regular", "charter_linea"].includes(d.segmento)), (d) => d.movimientos);
const totalMovs = d3.sum(segRef, (d) => d.movimientos);
const primerAnio = d3.min(serieLarga, (d) => d.anio);
```

<div class="portada">
  <div>
    <span class="idx">PotenciarMDQ · Aeropuerto Astor Piazzolla</span>
    <h1>Mar del Plata <em>despega</em></h1>
    <p class="bajada">${new Date().getUTCFullYear() - primerAnio} años de vuelos, pasajeros, aviones y temporadas, con datos abiertos de la ANAC y del Municipio.</p>
  </div>
  <ol class="indice">
    <li><span>01</span><a href="#01">Un siglo XXI con altibajos</a></li>
    <li><span>02</span><a href="#02">El pulso diario</a></li>
    <li><span>03</span><a href="#03">Una ciudad de temporada</a></li>
    <li><span>04</span><a href="#04">Todo lo que vuela</a></li>
    <li><span>05</span><a href="#05">Asientos y ocupación</a></li>
    <li><span>06</span><a href="#06">A dónde se vuela (y el exterior)</a></li>
    <li><span>07</span><a href="#07">Quién vuela</a></li>
    <li><span>08</span><a href="#08">En qué aviones</a></li>
    <li><span>09</span><a href="#09">Un día en el aeropuerto</a></li>
    <li><span>10</span><a href="#10">Verano contra verano</a></li>
    <li><span>11</span><a href="#11">En el mapa del país</a></li>
    <li><span>12</span><a href="#12">Lo que viene</a></li>
  </ol>
</div>

<div class="cifras">
  <div><span class="rotulo">Pasajeros de línea ${ref.anio}</span><span class="valor">${compacto(ref.pasajeros_comerciales)}</span>
    <p class="nota">${pct(ref.pasajeros_comerciales / record.pasajeros)} del récord de ${record.anio}</p></div>
  <div><span class="rotulo">Movimientos totales ${ref.anio}</span><span class="valor">${entero(totalMovs)}</span>
    <p class="nota">${pct(noLinea / totalMovs)} no son vuelos de línea</p></div>
  <div><span class="rotulo">Turistas que llegan en avión</span><span class="valor">${pct1(turRef.share)}</span>
    <p class="nota">de ${compacto(turRef.turistas)} turistas en ${turRef.anio}</p></div>
  <div><span class="rotulo">Concentración de aerolíneas</span><span class="valor">${entero(ref.hhi_aerolineas)}</span>
    <p class="nota">índice HHI sobre 10.000 (10.000 = una sola)</p></div>
</div>

<h2 id="01" data-idx="01 — Desde 2001">Un siglo XXI con altibajos</h2>

Pasajeros de vuelos de línea por mes. La línea gruesa es la **tendencia**: lo que queda después de sacar el efecto del verano (descomposición estacional STL). Hasta ${d3.max(serieLarga.filter((d) => d.fuente !== "ANAC"), (d) => d.anio)} los datos son del Municipio; desde ${d3.min(serieLarga.filter((d) => d.fuente === "ANAC"), (d) => d.anio)}, de la ANAC.

```js
Plot.plot({
  width,
  height: 380,
  marginLeft: 55,
  y: {grid: true, label: "Pasajeros por mes", tickFormat: compacto},
  x: {label: null},
  marks: [
    Plot.areaY(serieLarga, {x: "periodo", y: "pasajeros", fill: TINTA, fillOpacity: 0.08, curve: "step"}),
    Plot.lineY(serieLarga, {x: "periodo", y: "pasajeros", stroke: TINTA_2, strokeWidth: 1, curve: "step"}),
    Plot.lineY(tendencia, {x: "periodo", y: "tendencia", stroke: ACENTO, strokeWidth: 2.5}),
    Plot.dot([d3.greatest(serieLarga, (d) => d.pasajeros)], {x: "periodo", y: "pasajeros", fill: ACENTO, r: 4}),
    Plot.text([d3.greatest(serieLarga, (d) => d.pasajeros)], {x: "periodo", y: "pasajeros", text: (d) => `Récord: ${entero(d.pasajeros)} (${MESES[d.mes - 1]} ${d.anio})`, dy: -10, textAnchor: "middle", fill: TINTA}),
    Plot.ruleY([0]),
    Plot.tip(serieLarga, Plot.pointerX({x: "periodo", y: "pasajeros",
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\n${entero(d.pasajeros)} pasajeros\nFuente: ${d.fuente}`}))
  ]
})
```

<div class="grid-2">
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: 220,
  marginLeft: 55,
  y: {grid: true, label: "Pasajeros de línea por año", tickFormat: compacto},
  x: {label: null, tickFormat: "d", ticks: 8},
  marks: [
    Plot.barY(largaAnual, {x: "anio", y: "pasajeros", fill: (d) => (d.anio === record.anio ? ACENTO : TINTA), fillOpacity: (d) => (d.fuente === "ANAC" ? 1 : 0.55), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${entero(d.pasajeros)} pasajeros (${d.fuente})`}),
    Plot.ruleY([0])
  ]
})
```

</div>
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: 220,
  marginLeft: 55,
  y: {grid: true, label: "Movimientos comerciales por año", tickFormat: compacto},
  x: {label: null, tickFormat: "d", ticks: 8},
  marks: [
    Plot.barY(largaAnual.filter((d) => d.movimientos > 0), {x: "anio", y: "movimientos", fill: TINTA, fillOpacity: (d) => (d.fuente === "ANAC" ? 1 : 0.55), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${entero(d.movimientos)} aterrizajes y despegues comerciales (${d.fuente})`}),
    Plot.ruleY([0])
  ]
})
```

</div>
</div>
<p class="fuente">Barras claras: Municipio de General Pueyrredon (2001–2018) · oscuras: ANAC (2019+). En 2019, año que cubren ambas fuentes, difieren menos de 4 % por mes. Movimientos comerciales = vuelos regulares y no regulares; antes de 2019 no hay detalle vuelo por vuelo completo (solo una muestra municipal 2015–2018, usada en la composición por segmento y flota).</p>

<h2 id="02" data-idx="02 — Día por día">El pulso diario</h2>

Cada punto es un día. La línea negra es el promedio de 7 días; la gris punteada, el mismo período del año anterior.

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {grid: true, label: "Pasajeros por día", tickFormat: entero},
  x: {label: null},
  marks: [
    Plot.dot(diario, {x: "fecha", y: "pasajeros", r: 1.3, fill: TINTA_2, fillOpacity: 0.35}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7_anio_anterior", stroke: OTRO, strokeDasharray: "3,3", strokeWidth: 1.5}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7", stroke: TINTA, strokeWidth: 1.8}),
    Plot.ruleY([0]),
    Plot.tip(diario, Plot.pointerX({x: "fecha", y: "pasajeros_ma7",
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\nPasajeros: ${entero(d.pasajeros)}\nPromedio 7 días: ${entero(d.pasajeros_ma7)}${d.var_ma7_interanual == null ? "" : `\nvs. año anterior: ${variacion(d.var_ma7_interanual)}`}`}))
  ]
})
```

### Días atípicos

Cada día comparado con lo esperable para ese día de la semana en esa época. Los marcados en bermellón se alejaron más de 3 desvíos: paros, temporales, feriados o vuelos extra.

```js
const ev = new Map(eventos.map((e) => [e.fecha, e]));
const at = atipicos.filter((d) => d.z != null).map((d) => ({...d, evento: ev.get(d.fecha.toISOString().slice(0, 10))}));
const marcados = at.filter((d) => d.es_atipico);
```

<div class="grid-2-1">
<div>

```js
Plot.plot({
  width: width * 0.62,
  height: 300,
  marginLeft: 45,
  y: {grid: true, label: "Desvío (z)", domain: [d3.min(at, (d) => d.z), d3.max(at, (d) => d.z)]},
  x: {label: null},
  marks: [
    Plot.ruleY([-3, 3], {stroke: ACENTO, strokeDasharray: "2,3"}),
    Plot.ruleY([0], {stroke: TINTA_2}),
    Plot.dot(at.filter((d) => !d.es_atipico), {x: "fecha", y: "z", r: 1.4, fill: TINTA_2, fillOpacity: 0.4}),
    Plot.dot(marcados, {x: "fecha", y: "z", r: 3.5, fill: ACENTO, tip: true,
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\n${entero(d.pasajeros)} pasajeros (esperado ${entero(d.esperado)})${d.evento ? `\n${d.evento.evento}` : ""}${d.condicion ? `\nClima: ${d.condicion}` : ""}`}),
    Plot.text(marcados.filter((d) => d.evento), {x: "fecha", y: "z", text: () => "paro", dy: 12, fontSize: 10, fill: ACENTO})
  ]
})
```

</div>
<div>

```js
html`<table class="editorial"><thead><tr><th>Día</th><th>Pasajeros</th><th>Esperado</th><th>Por qué</th></tr></thead><tbody>
${d3.sort(marcados, (d) => d.z).slice(0, 10).map((d) => html`<tr><td>${d.fecha.toLocaleDateString("es-AR", {timeZone: "UTC"})}</td><td>${entero(d.pasajeros)}</td><td>${entero(d.esperado)}</td><td style="text-align:left">${d.evento ? html`<a href=${d.evento.fuente} target="_blank" rel="noopener">${d.evento.evento}</a>` : d.feriado_nombre ?? (d.condicion && d.condicion !== "normal" ? `Clima: ${d.condicion}` : "—")}</td></tr>`)}
</tbody></table>`
```

</div>
</div>

```js
// Qué parte de los días con cada condición tuvo una caída fuerte (>20 % menos de lo esperado).
const porClima = d3.rollups(at.filter((d) => d.condicion && d.esperado > 0), (v) => ({dias: v.length, caidas: v.filter((d) => d.desvio_pct < -0.2).length}), (d) => d.condicion)
  .map(([condicion, v]) => ({condicion, ...v, share: v.caidas / v.dias})).sort((a, b) => b.share - a.share);
```

${porClima.length > 1 ? html`<p>Días con una caída de más de 20 % respecto de lo esperado, según el clima: ${porClima.map((d) => `${d.condicion} ${pct(d.share)} (${d.dias} días)`).join(" · ")}. Clima: Open-Meteo (reanálisis ERA5) en el aeropuerto.</p>` : ""}

<h2 id="03" data-idx="03 — Estacionalidad">Una ciudad de temporada</h2>

Cuanto más oscuro el cuadrado, más pasajeros ese día.

```js
const semana = (d) => d3.utcMonday.count(d3.utcYear(d.fecha), d.fecha);
const diaSemana = (d) => (d.fecha.getUTCDay() + 6) % 7;
const inicioMes = d3.range(12).map((m) => ({m, x: d3.utcMonday.count(new Date(Date.UTC(2025, 0, 1)), new Date(Date.UTC(2025, m, 1)))}));
```

```js
Plot.plot({
  width,
  height: 40 + 96 * new Set(diario.map((d) => d.anio)).size,
  padding: 0.08,
  x: {axis: "top", ticks: inicioMes.map((d) => d.x), tickFormat: (x) => MESES[inicioMes.find((d) => d.x === x)?.m] ?? "", tickSize: 0, label: null},
  y: {tickFormat: (i) => DIAS[i], tickSize: 0, label: null},
  fy: {tickFormat: "d", label: null},
  color: {type: "linear", range: [SEQ[0], SEQ[4]], legend: true, label: "Pasajeros por día", tickFormat: entero},
  marks: [
    Plot.cell(diario, {x: semana, y: diaSemana, fy: "anio", fill: "pasajeros", rx: 1, tip: true,
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\n${entero(d.pasajeros)} pasajeros`})
  ]
})
```

### El avión y los turistas

Turistas que llegan a Mar del Plata por cualquier medio (EMTURyC) y qué parte llega en avión.

<div class="grid-2">
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: 260,
  marginLeft: 45,
  y: {grid: true, label: "% de turistas que llegan en avión", tickFormat: (d) => pct1(d)},
  x: {label: null, tickFormat: "d"},
  marks: [
    Plot.lineY(turAnual, {x: "anio", y: "share", stroke: TINTA, strokeWidth: 2, marker: "circle-stroke"}),
    Plot.ruleY([0]),
    Plot.tip(turAnual, Plot.pointerX({x: "anio", y: "share", title: (d) => `${d.anio}\n${pct1(d.share)} en avión\n${entero(d.llegados)} de ${entero(d.turistas)}`}))
  ]
})
```

</div>
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: 260,
  marginLeft: 45,
  y: {grid: true, label: "Llegados − salidos por mes", tickFormat: entero},
  x: {label: null},
  marks: [
    Plot.rectY(mensual, {x1: "periodo", x2: (d) => d3.utcMonth.offset(d.periodo, 1), y: "balance_pasajeros", inset: 0.5,
      fill: (d) => (d.balance_pasajeros >= 0 ? DIV.pos : DIV.neg), tip: true,
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\nLlegaron ${entero(d.pasajeros_llegados)}\nSe fueron ${entero(d.pasajeros_salidos)}`}),
    Plot.ruleY([0])
  ]
})
```
<p class="fuente">Azul: llegó más gente de la que se fue · bermellón: al revés.</p>

</div>
</div>

<h2 id="04" data-idx="04 — Toda la actividad">Todo lo que vuela</h2>

El aeropuerto no es solo vuelos de línea: taxis aéreos, aviones privados, vuelos oficiales y militares y escuelas de vuelo usan la misma pista. Detalle por segmento en <a href="./aviacion-general">Toda la aviación</a>.

```js
// Grilla completa mes × segmento (los meses sin movimientos van en 0, si no el área se corta).
const periodosSeg = [...new Set(segMensual.map((d) => +d.periodo))].sort((a, b) => a - b);
const idxSeg = new Map(segMensual.map((d) => [`${+d.periodo}|${d.segmento}`, d]));
const segM = periodosSeg.flatMap((t) => SEGMENTOS.map((s) => {
  const d = idxSeg.get(`${t}|${s.id}`);
  const periodo = new Date(t);
  return {periodo, anio: periodo.getUTCFullYear(), mes: periodo.getUTCMonth() + 1, segmento: s.id, nombre: s.nombre, movimientos: d?.movimientos ?? 0};
}));
```

```js
Plot.plot({
  width,
  height: 320,
  marginLeft: 50,
  y: {grid: true, label: "Aterrizajes y despegues por mes", tickFormat: entero},
  x: {label: null},
  color: {...segColor, legend: true},
  marks: [
    Plot.areaY(segM, {x: "periodo", y: "movimientos", fill: "nombre", order: segColor.domain, curve: "step-after", tip: true,
      title: (d) => `${d.nombre} · ${MESES[d.mes - 1]} ${d.anio}\n${entero(d.movimientos)} movimientos`}),
    Plot.ruleY([0])
  ]
})
```

```js
html`<table class="editorial"><thead><tr><th>Segmento ${ref.anio}</th><th>Movimientos</th><th>% del total</th><th>Pasajeros</th><th>Pax por movimiento</th><th>Operadores</th><th>% vuelos locales</th><th>% finde/feriado</th></tr></thead><tbody>
${d3.sort(segRef, (d) => -d.movimientos).map((d) => html`<tr><td><span class="chip" style="background:${SEG_COLOR[d.segmento]}"></span>${SEG_NOMBRE[d.segmento] ?? d.segmento}</td><td>${entero(d.movimientos)}</td><td>${pct(d.share_movimientos)}</td><td>${entero(d.pasajeros)}</td><td>${decimal1(d.pax_por_movimiento)}</td><td>${d.operadores}</td><td>${pct(d.share_vuelos_locales)}</td><td>${pct(d.share_finde_feriado)}</td></tr>`)}
</tbody></table>`
```

### El avión típico de cada segmento

El modelo con más aterrizajes y despegues en ${ref.anio}. En taxi aéreo y privados se muestra además el **avión básico**: el turbohélice de 5 o más pasajeros más frecuente (el estándar del vuelo ejecutivo). El pistón más frecuente es aviación liviana y casi no lleva pasajeros.

```js
const tip = avionTipico.filter((d) => d.anio === ref.anio);
const fichas = SEGMENTOS.flatMap((s) => {
  const top = tip.find((d) => d.segmento === s.id && d.ranking === 1);
  const porPax = tip.find((d) => d.segmento === s.id && d.ranking_por_pasajeros === 1);
  const out = top ? [{...top, etiqueta: s.nombre}] : [];
  const basico = tip.find((d) => d.segmento === s.id && d.perfil === "turbohelice_basico" && d.ranking_en_perfil === 1);
  if (basico && ["taxi_aereo", "privado"].includes(s.id) && basico.aeronave_familia !== top?.aeronave_familia) out.push({...basico, etiqueta: `${s.nombre} · avión básico (turbohélice 5+ pax)`});
  if (porPax && top && porPax.aeronave_familia !== top.aeronave_familia && porPax.aeronave_familia !== basico?.aeronave_familia && porPax.pasajeros > 0) out.push({...porPax, etiqueta: `${s.nombre} · el que más pasajeros lleva`});
  return out;
});
```

```js
html`<div class="fichas">${fichas.map((f) => html`<div class="ficha">
  <span class="seg" style="color:${SEG_COLOR[f.segmento]}">${f.etiqueta}</span>
  <div class="modelo">${f.aeronave_familia}</div>
  <dl>
    <dt>Movimientos</dt><dd>${entero(f.movimientos)} (${pct(f.share_en_segmento)})</dd>
    <dt>Pasajeros promedio</dt><dd>${decimal1(f.pax_promedio)}</dd>
    <dt>Capacidad observada (p95)</dt><dd>${f.capacidad_observada_p95 ?? "—"}</dd>
    <dt>Tiempo en tierra (mediana)</dt><dd>${f.tiempo_en_tierra_mediano_min != null ? `${Math.round(f.tiempo_en_tierra_mediano_min)} min` : "—"}</dd>
    <dt>Duración de vuelo (mediana)</dt><dd>${f.duracion_vuelo_mediana_min != null ? `${Math.round(f.duracion_vuelo_mediana_min)} min` : "—"}</dd>
    <dt>Hora más frecuente</dt><dd>${f.hora_mas_frecuente}h</dd>
    <dt>Principales orígenes/destinos</dt><dd>${f.principales_origenes_destinos ?? "—"}</dd>
  </dl></div>`)}</div>`
```

### Desde 2015

Composición de la actividad por año. 2015–2018 sale de una muestra municipal de vuelos (≈ la mitad de los movimientos, sin vuelos oficiales ni escuelas), por eso se muestra en porcentaje.

```js
const hs = d3.rollups(historiaSeg, (v) => ({movimientos: d3.sum(v, (d) => d.movimientos), fuente: v[0].fuente}), (d) => d.anio, (d) => d.segmento)
  .flatMap(([anio, segs]) => segs.map(([segmento, v]) => ({anio, segmento, nombre: SEG_NOMBRE[segmento] ?? segmento, ...v})));
```

```js
Plot.plot({
  width,
  height: 260,
  marginLeft: 50,
  y: {percent: true, label: "% de los movimientos", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {...segColor, legend: true},
  marks: [
    Plot.barY(hs, Plot.stackY({x: "anio", y: "movimientos", fill: "nombre", order: segColor.domain, offset: "normalize", inset: 0.5, tip: true,
      title: (d) => `${d.nombre} ${d.anio}\n${entero(d.movimientos)} movimientos\nFuente: ${d.fuente}`})),
    Plot.ruleY([0])
  ]
})
```

<h2 id="05" data-idx="05 — Oferta">Asientos y ocupación</h2>

Vuelos de línea: pasajeros transportados y asientos ofrecidos (estimados) por mes. La distancia entre ambas líneas son asientos que volaron vacíos.

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {grid: true, label: "Por mes", tickFormat: entero},
  x: {label: null},
  color: {legend: true, domain: ["Asientos ofrecidos (est.)", "Pasajeros"], range: [OTRO, TINTA]},
  marks: [
    Plot.areaY(mensual, {x: "periodo", y: "asientos_estimados", fill: OTRO, fillOpacity: 0.15}),
    Plot.lineY(mensual, {x: "periodo", y: "asientos_estimados", stroke: () => "Asientos ofrecidos (est.)", strokeWidth: 2}),
    Plot.lineY(mensual, {x: "periodo", y: "pasajeros_comerciales", stroke: () => "Pasajeros", strokeWidth: 2}),
    Plot.ruleY([0]),
    Plot.tip(mensual, Plot.pointerX({x: "periodo", y: "pasajeros_comerciales",
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\nPasajeros: ${entero(d.pasajeros_comerciales)}\nAsientos (est.): ${entero(d.asientos_estimados)}\nOcupación: ${pct(d.lf_estimado)}`}))
  ]
})
```

<div class="note">La ANAC no publica asientos: se estiman con la capacidad típica observada de cada avión (ver <a href="./metodologia">metodología</a>).</div>

<h2 id="06" data-idx="06 — Conectividad">A dónde se vuela</h2>

La línea aérea conecta a Mar del Plata casi solo con el resto del país. Los vuelos al exterior existen, pero son de aviación general: jets ejecutivos, taxis aéreos, aviones privados y vuelos oficiales, sobre todo a Uruguay. Para verlos, elegí *Toda la aviación*.

```js
const anioMapa = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
const modoMapa = view(Inputs.radio(["Línea aérea (pasajeros)", "Toda la aviación (movimientos)"], {value: "Línea aérea (pasajeros)"}));
```

```js
const PAIS = (c) => c == null ? "Sin identificar" : c === "FK" ? "Islas Malvinas" : c === "AR" ? "Argentina" : new Intl.DisplayNames(["es"], {type: "region"}).of(c);
// Cono sur: Argentina, Chile, Uruguay, Paraguay y el sur de Brasil. Lo demás va en la lista.
const enSudamerica = (d) => d.lat >= -56 && d.lat <= -14 && d.lon >= -76 && d.lon <= -38;
const nombreDestino = (d) => d.codigo === "MDP" ? "Vuelos locales (ida y vuelta a MDQ)"
  : /mar del plata/i.test(d.ciudad ?? "") ? `${d.nombre ?? d.codigo}` : d.ciudad ?? d.nombre ?? d.codigo;
const esLinea = modoMapa.startsWith("Línea");
const numerico = (d) => /^\d+$/.test(d.codigo);
const puntos = esLinea
  ? rutas.filter((d) => d.anio === anioMapa && d.lat != null && d.pasajeros >= 50)
      .map((d) => ({...d, valor: d.pasajeros, internacional: d.clasificacion_vuelo === "internacional"}))
  : d3.rollups(destinos.filter((d) => d.anio === anioMapa), (v) => ({
      ...v[0], valor: d3.sum(v, (d) => d.movimientos), pasajeros: d3.sum(v, (d) => d.pasajeros),
      internacional: v.some((d) => d.clasificacion_vuelo === "internacional") && !numerico(v[0]),
      segmento: d3.greatest(d3.rollups(v, (g) => d3.sum(g, (d) => d.movimientos), (d) => d.segmento), (g) => g[1])[0]
    }), (d) => d.codigo).map(([, d]) => d);
const enMapa = puntos.filter((d) => d.lat != null && enSudamerica(d) && d.codigo !== "MDP");
const fueraMapa = puntos.filter((d) => d.lat != null && !enSudamerica(d));
const sinUbicar = puntos.filter((d) => d.lat == null);
const maxValor = d3.max(enMapa, (d) => d.valor);
const foco = rutas.find((d) => d.foco_lat != null);
const etiquetas = d3.sort(enMapa.filter((d) => Math.hypot(d.lon - foco.foco_lon, d.lat - foco.foco_lat) > 1.2), (d) => -d.valor)
  .filter((d, i, arr) => !arr.slice(0, i).some((o) => Math.hypot(o.lon - d.lon, o.lat - d.lat) < 2.2)).slice(0, 12);
const unidad = esLinea ? "pasajeros" : "movimientos";
```

<div class="grid-2-1 mapa">
<div>

```js
Plot.plot({
  width: 540, height: 700,
  projection: {type: "mercator", inset: 30,
    domain: {type: "MultiPoint", coordinates: [[foco.foco_lon, foco.foco_lat], [-68.3, -54.8], [-65.0, -22.0], ...enMapa.map((d) => [d.lon, d.lat])]}},
  r: {range: [2.5, 20]},
  color: {domain: ["Argentina", "Exterior"], range: [TINTA_2, ACENTO], legend: true},
  marks: [
    Plot.geo(paises, {fill: TINTA, fillOpacity: 0.05, stroke: TINTA, strokeOpacity: 0.25}),
    Plot.link(enMapa, {x1: () => foco.foco_lon, y1: () => foco.foco_lat, x2: "lon", y2: "lat",
      stroke: (d) => d.internacional ? "Exterior" : "Argentina", strokeOpacity: 0.45,
      strokeWidth: (d) => 0.6 + 7 * Math.sqrt(d.valor / maxValor)}),
    Plot.dot(enMapa, {x: "lon", y: "lat", r: "valor", fill: (d) => d.internacional ? "Exterior" : "Argentina",
      stroke: "var(--theme-background)", strokeWidth: 1.5, tip: true,
      title: (d) => `${nombreDestino(d)} (${d.codigo})${d.internacional ? ` · ${PAIS(d.pais)}` : ""}\n${entero(d.valor)} ${unidad}` +
        (esLinea ? `\n${decimal1(d.salidas_semanales_promedio)} salidas por semana` : `\nSobre todo: ${SEG_NOMBRE[d.segmento] ?? d.segmento}`)}),
    Plot.text(etiquetas, {x: "lon", y: "lat", text: nombreDestino, dy: -12, fontSize: 11, fill: TINTA, stroke: "var(--theme-background)", strokeWidth: 3}),
    Plot.dot([foco], {x: "foco_lon", y: "foco_lat", r: 6, fill: TINTA}),
    Plot.text([foco], {x: "foco_lon", y: "foco_lat", text: () => "Mar del Plata", dx: 10, textAnchor: "start", fontWeight: "bold"})
  ]
})
```

</div>
<div>

```js
html`<table class="editorial"><thead><tr><th>Destino</th><th>${esLinea ? "Pasajeros" : "Movim."}</th><th>${esLinea ? "Salidas/sem." : "Segmento principal"}</th></tr></thead><tbody>
${d3.sort(puntos, (d) => -d.valor).slice(0, 16).map((d) => html`<tr class=${d.internacional ? "foco" : ""}><td>${nombreDestino(d)}${d.internacional ? ` (${PAIS(d.pais)})` : ""} <span class="muted">${d.codigo}</span></td><td>${entero(d.valor)}</td><td>${esLinea ? decimal1(d.salidas_semanales_promedio) : SEG_NOMBRE[d.segmento] ?? d.segmento}</td></tr>`)}
</tbody></table>
<p class="fuente">${fueraMapa.length ? `Fuera del mapa: ${fueraMapa.map((d) => `${nombreDestino(d)} (${PAIS(d.pais)})`).join(", ")}. ` : ""}${sinUbicar.length ? `${entero(d3.sum(sinUbicar, (d) => d.valor))} ${unidad} a ${sinUbicar.length} lugares sin coordenadas públicas (en su mayoría lugares aptos denunciados).` : ""}</p>`
```

</div>
</div>

### Vuelos al exterior

```js
// Códigos numéricos = Lugares Aptos Denunciados (LAD): pistas registradas por denuncia, no
// aeródromos, sin coordenadas públicas. ANAC los marca como internacionales, pero están en el país.
const esNumerico = (d) => /^\d+$/.test(d.codigo);
const intl = destinos.filter((d) => d.clasificacion_vuelo === "internacional" && !esNumerico(d));
const numericos = destinos.filter((d) => d.anio === anioMapa && esNumerico(d));
const intlAnio = intl.filter((d) => d.anio === anioMapa);
const intlTotal = d3.sum(intlAnio, (d) => d.movimientos);
const intlLinea = d3.sum(intlAnio.filter((d) => d.es_linea), (d) => d.movimientos);
const paisesTop = d3.groupSort(intl.filter((d) => d.pais), (v) => -d3.sum(v, (d) => d.movimientos), (d) => d.pais).slice(0, 5);
const grupoPais = (d) => d.pais == null ? "Sin ubicar" : paisesTop.includes(d.pais) ? PAIS(d.pais) : "Otros países";
const ordenPais = [...paisesTop.map(PAIS), "Otros países", "Sin ubicar"];
```

<div class="cifras c3">
  <div><span class="rotulo">Movimientos al/desde el exterior · ${anioMapa}</span><span class="valor">${entero(intlTotal)}</span><div class="nota">${pct1(intlTotal / d3.sum(destinos.filter((d) => d.anio === anioMapa), (d) => d.movimientos))} de todos los movimientos del aeropuerto</div></div>
  <div><span class="rotulo">De línea aérea</span><span class="valor">${entero(intlLinea)}</span><div class="nota">el resto es aviación general y vuelos oficiales</div></div>
  <div><span class="rotulo">Países</span><span class="valor">${new Set(intlAnio.filter((d) => d.pais).map((d) => d.pais)).size}</span><div class="nota">${d3.groupSort(intlAnio.filter((d) => d.pais), (v) => -d3.sum(v, (d) => d.movimientos), (d) => d.pais).slice(0, 3).map(PAIS).join(", ")}</div></div>
</div>

<div class="grid-2">
<div>

```js
Plot.plot({
  title: "Movimientos internacionales por país",
  width: width / 2 - 40, height: 300, marginLeft: 50,
  x: {label: null, tickFormat: String}, y: {label: "Movimientos", grid: true},
  color: {domain: ordenPais, range: [...CAT.slice(0, paisesTop.length), OTRO, "#d6d3cb"], legend: true},
  marks: [
    Plot.barY(intl, Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: grupoPais, order: ordenPais, tip: true})),
    Plot.ruleY([0])
  ]
})
```

</div>
<div>

```js
Plot.plot({
  title: `Quién vuela al exterior · ${anioMapa}`,
  width: width / 2 - 40, height: 300, marginLeft: 150,
  x: {label: "Movimientos", grid: true}, y: {label: null},
  marks: [
    Plot.barX(intlAnio, Plot.groupY({x: "sum"}, {y: (d) => SEG_NOMBRE[d.segmento] ?? d.segmento, x: "movimientos",
      fill: (d) => SEG_COLOR[d.segmento] ?? OTRO, sort: {y: "-x"}, tip: true})),
    Plot.ruleX([0])
  ]
})
```

</div>
</div>

<p class="fuente">Fuente: ANAC, clase y clasificación de cada vuelo. Ubicación de cada código: lista oficial de aeródromos y helipuertos de la ANAC y OurAirports (código local, OACI e IATA). Se excluyen ${entero(d3.sum(numericos, (d) => d.movimientos))} movimientos de ${anioMapa} hacia o desde <b>lugares aptos denunciados</b> (LAD, código numérico): superficies aptas para aterrizar registradas por su dueño ante la ANAC, que no son aeródromos (art. 25 del Código Aeronáutico) y no tienen coordenadas públicas. La ANAC los marca como internacionales, pero están en el país.</p>

<h2 id="07" data-idx="07 — Mercado">Quién vuela</h2>

```js
const comerciales = aerolineas.filter((d) => d.aerolinea_nombre !== "Sin dato");
const aer = topN(comerciales, "aerolinea_nombre", "pasajeros", 5);
```

```js
Plot.plot({
  width,
  height: 280,
  marginLeft: 50,
  y: {percent: true, label: "% de pasajeros de línea", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...aer.top, "Otras"], range: [...CAT.slice(0, aer.top.length), OTRO]},
  marks: [
    Plot.barY(comerciales, Plot.groupX({y: "sum"}, {x: "anio", y: "share_pasajeros", fill: aer.label, inset: 1, tip: true})),
    Plot.ruleY([0])
  ]
})
```

<h2 id="08" data-idx="08 — Flota">En qué aviones</h2>

Familias de aviones en los vuelos de línea, por año. 2015–2018 sale de la muestra municipal. En 2019–2020 la ANAC no informa el avión: se infiere por operador y pasajeros a bordo (por ejemplo, Aerolíneas con más de 96 pasajeros solo puede ser un 737, porque el E190 tiene 96 asientos). Lo que no se puede inferir queda como "Sin dato".

```js
const flotaHist = historiaSeg.filter((d) => d.anio < 2019 && ["linea_regular", "charter_linea"].includes(d.segmento))
  .map((d) => ({anio: d.anio, familia: d.aeronave_familia, movimientos: d.movimientos}));
const flotaAnac = aeronavesM.filter((d) => d.es_linea)
  .map((d) => ({anio: d.anio, familia: d.aeronave_familia_inferida, movimientos: d.movimientos, inferida: d.aeronave_inferida}));
const flota = [...flotaHist, ...flotaAnac];
const fam = topN(flota.filter((d) => d.familia !== "Sin dato"), "familia", "movimientos", 6);
const famLabel = (d) => d.familia === "Sin dato" ? "Sin dato" : fam.label(d);
const pctInferido = d3.rollup(flotaAnac, (v) => d3.sum(v.filter((d) => d.inferida), (d) => d.movimientos) / d3.sum(v, (d) => d.movimientos), (d) => d.anio);
```

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {percent: true, label: "% de movimientos de línea", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...fam.top, "Otras", "Sin dato"], range: [...CAT.slice(0, fam.top.length), OTRO, "#d6d3cb"]},
  marks: [
    Plot.barY(flota, Plot.stackY(Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: famLabel, order: [...fam.top, "Otras", "Sin dato"], offset: "normalize", inset: 1, tip: true}))),
    Plot.text([2019, 2020].filter((a) => pctInferido.get(a) > 0), {x: (a) => a, frameAnchor: "top", dy: -4, text: (a) => `${pct(pctInferido.get(a))} inferido`, fontSize: 10, fill: TINTA_2}),
    Plot.ruleY([0])
  ]
})
```

### Modelo por modelo

Las denominaciones de la ANAC se estandarizan: `BO-737-800`, `BO-B737-800` y `BO-737-8SH` son el mismo Boeing 737-800, y `BO-737-8` / `BO-B737-8MAX` son el 737 MAX 8 (verificado por matrícula contra la flota publicada de Aerolíneas).

```js
const modelosLinea = aeronavesM.filter((d) => d.es_linea && d.anio >= 2021 && d.aeronave_familia !== "Sin dato");
const mod = topN(modelosLinea, "aeronave_modelo", "movimientos", 6);
```

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {label: "Movimientos de línea", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...mod.top, "Otras"], range: [...CAT.slice(0, mod.top.length), OTRO]},
  marks: [
    Plot.barY(modelosLinea, Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: mod.label, order: [...mod.top, "Otras"], inset: 1, tip: true})),
    Plot.ruleY([0])
  ]
})
```

<h2 id="09" data-idx="09 — Operación">Un día en el aeropuerto</h2>

Aterrizajes y despegues de línea promedio por semana, según día y hora.

```js
const anioHora = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
```

```js
Plot.plot({
  width,
  height: 250,
  padding: 0.06,
  x: {label: "Hora local", tickFormat: (h) => `${h}h`},
  y: {domain: d3.range(1, 8), tickFormat: (i) => DIAS[i - 1], label: null},
  color: {type: "linear", range: [SEQ[0], SEQ[4]], legend: true, label: "Movimientos por semana"},
  marks: [
    Plot.cell(horaSemana.filter((d) => d.anio === anioHora), {x: "hora_local", y: "dia_semana", fill: "movimientos_por_semana", rx: 1, tip: true,
      title: (d) => `${d.dia_semana_nombre} ${d.hora_local}h\n${decimal1(d.movimientos_por_semana)} movimientos por semana`})
  ]
})
```

```js
const rotAnio = rotaciones.filter((d) => d.anio === ref.anio && d.tipo_rotacion === "rotacion");
const rotFam = d3.rollups(rotAnio, (v) => ({n: d3.sum(v, (d) => d.rotaciones), med: d3.median(v, (d) => d.mediana_min)}), (d) => d.aeronave_familia)
  .filter(([, v]) => v.n >= 100).sort((a, b) => b[1].n - a[1].n).slice(0, 2);
const aep = tramos.filter((d) => d.anio === ref.anio && d.origen === "AER" && d.destino === "MDP");
```

<div class="cifras">
  <div><span class="rotulo">Hora pico de diseño</span><span class="valor">${entero(ref.pax_hora_sbr30)}</span><p class="nota">pasajeros en la 30.ª hora más cargada de ${ref.anio}</p></div>
  ${rotFam.map(([f, v]) => html`<div><span class="rotulo">En tierra · ${f}</span><span class="valor">${Math.round(v.med)} min</span><p class="nota">mediana entre aterrizar y volver a despegar</p></div>`)}
  <div><span class="rotulo">Aeroparque → MDQ</span><span class="valor">${aep.length ? Math.round(d3.median(aep, (d) => d.duracion_mediana_min)) : "—"} min</span><p class="nota">de pista a pista (mediana)</p></div>
</div>

<h2 id="10" data-idx="10 — Temporadas">Verano contra verano</h2>

Pasajeros por destino en los últimos tres veranos completos (diciembre a febrero), destinos con más de 1.000 pasajeros en alguna temporada.

```js
const completos = veranosCompletos(mensual).slice(-3);
const ver = verano.filter((d) => completos.includes(d.verano_anio) && d.ciudad);
const topDest = d3.rollups(ver, (v) => d3.max(v, (d) => d.pasajeros), (d) => d.ciudad)
  .filter(([, max]) => max >= 1000).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([c]) => c);
const verTop = ver.filter((d) => topDest.includes(d.ciudad));
```

```js
completos.length < 2
  ? html`<p class="muted">Hacen falta al menos dos temporadas completas.</p>`
  : Plot.plot({
      width,
      height: 60 + 34 * topDest.length,
      marginLeft: 170,
      x: {grid: true, label: "Pasajeros en la temporada", tickFormat: entero},
      y: {domain: topDest, label: null},
      color: {legend: true, type: "ordinal", domain: completos, range: SEQ.slice(-completos.length), tickFormat: (y) => `Verano ${y}`},
      marks: [
        Plot.link(d3.groups(verTop, (d) => d.ciudad), {x1: ([, v]) => d3.min(v, (d) => d.pasajeros), x2: ([, v]) => d3.max(v, (d) => d.pasajeros), y1: ([c]) => c, y2: ([c]) => c, stroke: OTRO, strokeWidth: 2}),
        Plot.dot(verTop, {x: "pasajeros", y: "ciudad", fill: "verano_anio", r: 6, stroke: "var(--theme-background)", strokeWidth: 2, tip: true,
          title: (d) => `${d.ciudad} · verano ${d.verano_anio}\n${entero(d.pasajeros)} pasajeros`})
      ]
    })
```

<h2 id="11" data-idx="11 — Contexto nacional">En el mapa del país</h2>

```js
const rankRef = ranking.filter((d) => d.anio === ref.anio).sort((a, b) => a.ranking_pasajeros - b.ranking_pasajeros);
const mdqRank = rankRef.find((d) => d.es_foco);
const redRef = red.filter((d) => d.anio === ref.anio);
const mdqRed = redRef.find((d) => d.es_foco);
const top25 = rankRef.filter((d) => d.ranking_pasajeros <= 25 || d.es_foco);
```

Mar del Plata fue el aeropuerto **n.º ${mdqRank?.ranking_pasajeros}** del país por pasajeros de línea en ${ref.anio} y el **n.º ${mdqRed?.ranking}** en importancia dentro de la red de vuelos de cabotaje (PageRank: cuenta cuántos vuelos llegan y desde qué aeropuertos).

<div class="grid-2-1">
<div>

```js
Plot.plot({
  width: width * 0.6,
  height: 22 * top25.length + 40,
  marginLeft: 160,
  x: {type: "log", grid: true, label: "Pasajeros de línea (escala logarítmica)", tickFormat: compacto},
  y: {domain: top25.map((d) => d.ciudad ?? d.codigo), label: null},
  marks: [
    Plot.barX(top25, {x1: 10000, x2: "pasajeros_linea", y: (d) => d.ciudad ?? d.codigo, fill: (d) => (d.es_foco ? ACENTO : d.es_par ? TINTA : OTRO), inset: 2, tip: true,
      title: (d) => `n.º ${d.ranking_pasajeros} · ${d.ciudad}\n${entero(d.pasajeros_linea)} pasajeros`})
  ]
})
```

</div>
<div>

```js
const paresRef = pares.filter((d) => d.anio === ref.anio);
```

```js
html`<table class="editorial"><thead><tr><th>Aeropuerto</th><th>Pico ÷ valle</th><th>% verano</th><th>Destinos</th></tr></thead><tbody>
${d3.sort(paresRef, (d) => -d.ratio_pico_valle).map((d) => html`<tr class=${d.es_foco ? "foco" : ""}><td>${d.ciudad}</td><td>${decimal1(d.ratio_pico_valle)}</td><td>${pct(d.share_pax_temporada_verano)}</td><td>${d.destinos_regulares}</td></tr>`)}
</tbody></table>`
```
<p class="fuente">Comparación con aeropuertos pares: cuánto más vuela el mes pico que el mes más flojo, qué parte del año cae en verano y cuántos destinos directos tiene.</p>

</div>
</div>

<h2 id="12" data-idx="12 — Pronóstico">Lo que viene</h2>

Proyección de pasajeros de línea a 6 meses (Holt-Winters sobre la serie pospandemia). La banda marca el rango donde cae el 80 % de las simulaciones. No incluye anuncios de rutas nuevas ni cambios de aerolíneas.

```js
const obs = pronostico.filter((d) => d.tipo === "observado");
const fut = pronostico.filter((d) => d.tipo === "pronostico");
```

```js
Plot.plot({
  width,
  height: 280,
  marginLeft: 50,
  y: {grid: true, label: "Pasajeros por mes", tickFormat: compacto},
  x: {label: null},
  marks: [
    Plot.areaY(fut, {x: "periodo", y1: "p10", y2: "p90", fill: ACENTO, fillOpacity: 0.15}),
    Plot.lineY(obs.slice(-30), {x: "periodo", y: "pasajeros", stroke: TINTA, strokeWidth: 1.8}),
    Plot.lineY([obs.at(-1), ...fut], {x: "periodo", y: "pasajeros", stroke: ACENTO, strokeWidth: 2, strokeDasharray: "4,3"}),
    Plot.ruleY([0]),
    Plot.tip(fut, Plot.pointerX({x: "periodo", y: "pasajeros", title: (d) => `${MESES[d.periodo.getUTCMonth()]} ${d.periodo.getUTCFullYear()}\n${entero(d.pasajeros)} (rango ${entero(d.p10)}–${entero(d.p90)})`}))
  ]
})
```

<h2 data-idx="Línea de tiempo">Hitos</h2>

```js
html`<table class="editorial"><tbody>${hitos.map((h) => html`<tr><td style="width:7rem">${h.fecha}</td><td style="text-align:left">${h.titulo}</td><td><a href=${h.fuente} target="_blank" rel="noopener">${h.tipo_fuente === "prensa" ? "prensa" : "fuente"}</a></td></tr>`)}</tbody></table>`
```

<h2 data-idx="Síntesis">Lo que muestran los datos</h2>

```js
const delAnio = mensual.filter((d) => d.anio === ref.anio).sort((a, b) => b.pasajeros - a.pasajeros);
const rutasRef = rutas.filter((d) => d.anio === ref.anio).sort((a, b) => b.pasajeros - a.pasajeros);
const shareTop = rutasRef[0].pasajeros / d3.sum(rutasRef, (d) => d.pasajeros);
```

- **Lejos del récord:** ${ref.anio} cerró con ${pct(ref.pasajeros_comerciales / record.pasajeros)} de los pasajeros de ${record.anio}.
- **Una temporada fuerte:** el mes pico (${MESES[delAnio[0].mes - 1]}) movió ${decimal1(ref.ratio_pico_valle)} veces más gente que el más flojo (${MESES[delAnio.at(-1).mes - 1]}).
- **Un puente con Buenos Aires:** ${pct(shareTop)} de los pasajeros de vuelos regulares viajaron entre Mar del Plata y ${rutasRef[0].ciudad}.
- **Más que aerolíneas:** ${pct(noLinea / totalMovs)} de los movimientos son taxis aéreos, privados, oficiales o escuelas.
- **El avión es minoritario para el turismo:** ${pct1(turRef.share)} de los turistas llegaron en avión en ${turRef.anio}.
