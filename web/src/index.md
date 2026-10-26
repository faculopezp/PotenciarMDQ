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
  veranosCompletos, topN, fechaLarga, ALTO, ejeAnios, fechaEje, notaCobertura} from "./components/util.js";
```

```js
const anual = datos(FileAttachment("data/mdq_anual.json"));
const mensual = datos(FileAttachment("data/mdq_mensual.json"));
const diario = datos(FileAttachment("data/mdq_diario.json"));
const horaSemana = datos(FileAttachment("data/mdq_hora_semana.json"));
const aerolineas = datos(FileAttachment("data/mdq_aerolineas.json"));
const rutas = datos(FileAttachment("data/mdq_rutas.json"));
const destinos = datos(FileAttachment("data/mdq_destinos.json"));
const exoticos = datos(FileAttachment("data/mdq_vuelos_exoticos.json"));
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
const cob = datos(FileAttachment("data/mdq_cobertura.json"));
const historiaSeg = datos(FileAttachment("data/mdq_historia_segmentos.json"));
const ranking = datos(FileAttachment("data/ranking_nacional.json"));
const red = datos(FileAttachment("data/red_aeropuertos.json"));
const atipicos = datos(FileAttachment("data/mdq_dias_atipicos.json"));
const pronostico = datos(FileAttachment("data/mdq_pronostico.json"));
const paises = FileAttachment("data/sudamerica.json").json();
const eventos = FileAttachment("data/eventos.json").json();
```

```js
const ref = ultimoAnioCompleto(anual);
const anios = anual.map((d) => d.anio);
const largaAnual = d3.rollups(serieLarga, (v) => ({pasajeros: d3.sum(v, (d) => d.pasajeros), movimientos: d3.sum(v, (d) => d.movimientos_comerciales), meses: v.length, fuente: v[0].fuente}), (d) => d.anio)
  .map(([anio, v]) => ({anio, ...v})).filter((d) => d.meses === 12);
const record = d3.greatest(largaAnual, (d) => d.pasajeros);
const recordMovs = d3.greatest(largaAnual, (d) => d.movimientos);
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
    <li><span>02</span><a href="#02">En el mapa del país</a></li>
    <li><span>03</span><a href="#03">Una ciudad de temporada</a></li>
    <li><span>04</span><a href="#04">Verano contra verano</a></li>
    <li><span>05</span><a href="#05">El pulso diario</a></li>
    <li><span>06</span><a href="#06">Un día en el aeropuerto</a></li>
    <li><span>07</span><a href="#07">A dónde se vuela</a></li>
    <li><span>08</span><a href="#08">Quién vuela</a></li>
    <li><span>09</span><a href="#09">Asientos y ocupación</a></li>
    <li><span>10</span><a href="#10">En qué aviones</a></li>
    <li><span>11</span><a href="#11">Todo lo que vuela</a></li>
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

Pasajeros de vuelos de línea por mes desde ${primerAnio}. La línea bermellón es la **tendencia**: lo que queda después de sacar el efecto del verano. El récord fue en ${record.anio}; la pandemia vació el aeropuerto en 2020 y la recuperación se estabilizó en torno a dos tercios de aquel pico.

```js
Plot.plot({
  width,
  height: ALTO.serie,
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
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\n${entero(d.pasajeros)} pasajeros`}))
  ]
})
```

<div class="grid-2">
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Pasajeros de línea por año", tickFormat: compacto},
  x: ejeAnios,
  marks: [
    Plot.barY(largaAnual, {x: "anio", y: "pasajeros", fill: (d) => (d.anio === record.anio ? ACENTO : TINTA), fillOpacity: (d) => (d.fuente === "ANAC" ? 1 : 0.55), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${entero(d.pasajeros)} pasajeros`}),
    Plot.ruleY([0])
  ]
})
```

</div>
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Movimientos comerciales por año", tickFormat: compacto},
  x: ejeAnios,
  marks: [
    Plot.barY(largaAnual.filter((d) => d.movimientos > 0), {x: "anio", y: "movimientos", fill: (d) => (d.anio === recordMovs.anio ? ACENTO : TINTA), fillOpacity: (d) => (d.fuente === "ANAC" ? 1 : 0.55), inset: 1.5, tip: true,
      title: (d) => `${d.anio}: ${entero(d.movimientos)} aterrizajes y despegues comerciales`}),
    Plot.ruleY([0])
  ]
})
```

</div>
</div>
<p class="leyenda">En ambos gráficos: tono claro 2001–2018, oscuro desde 2019; en bermellón, el año récord. Movimientos comerciales = aterrizajes y despegues de vuelos regulares y no regulares.</p>

<h2 id="02" data-idx="02 — Contexto nacional">En el mapa del país</h2>

```js
const rankRef = ranking.filter((d) => d.anio === ref.anio).sort((a, b) => a.ranking_pasajeros - b.ranking_pasajeros);
const mdqRank = rankRef.find((d) => d.es_foco);
const redRef = red.filter((d) => d.anio === ref.anio);
const mdqRed = redRef.find((d) => d.es_foco);
const top25 = rankRef.filter((d) => d.ranking_pasajeros <= 25 || d.es_foco);
```

Mar del Plata fue el aeropuerto **n.º ${mdqRank?.ranking_pasajeros}** del país por pasajeros de línea en ${ref.anio} y el **n.º ${mdqRed?.ranking}** por su peso en la red de vuelos de cabotaje. Al lado, cómo se compara con otros destinos turísticos.

<div class="grid-2-1">
<div>

```js
Plot.plot({
  width: width * 0.6,
  height: 22 * top25.length + 40,
  marginLeft: 215,
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
<p class="leyenda">Pico ÷ valle: cuántas veces más pasajeros mueve el mes más fuerte que el más flojo. % verano: parte del año que cae entre diciembre y febrero.</p>

</div>
</div>

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

Qué parte de los turistas que llegan a Mar del Plata lo hace en avión, y si en cada mes llegó más gente de la que se fue.

<div class="grid-2">
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: ALTO.medio,
  marginLeft: 45,
  marginBottom: 45,
  y: {grid: true, label: "% de turistas que llegan en avión", tickFormat: (d) => pct1(d)},
  x: ejeAnios,
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
  height: ALTO.medio,
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
<p class="leyenda">Azul: llegó más gente de la que se fue · bermellón: al revés.</p>

</div>
</div>

<h2 id="04" data-idx="04 — Temporadas">Verano contra verano</h2>

```js
const completos = veranosCompletos(mensual).slice(-3);
const ver = verano.filter((d) => completos.includes(d.verano_anio) && d.ciudad);
const aep = ver.filter((d) => d.codigo === "AER").sort((x, y) => x.verano_anio - y.verano_anio);
const resto = ver.filter((d) => d.codigo !== "AER");
const topCod = d3.rollups(resto, (v) => d3.max(v, (d) => d.pasajeros), (d) => d.codigo)
  .filter(([, max]) => max >= 1000).sort((x, y) => y[1] - x[1]).slice(0, 8).map(([c]) => c);
const nombreCod = new Map(resto.map((d) => [d.codigo, d.ciudad]));
// Cada destino con las tres temporadas (0 si ese verano no hubo vuelos).
const verTop = topCod.flatMap((c) => completos.map((a) => ({codigo: c, ciudad: nombreCod.get(c), verano_anio: a,
  pasajeros: d3.sum(resto.filter((d) => d.codigo === c && d.verano_anio === a), (d) => d.pasajeros)})));
```

Pasajeros de línea por destino en los últimos tres veranos completos (diciembre a febrero). **Aeroparque**, la ruta principal, movió ${aep.map((d) => `${compacto(d.pasajeros)} (${d.verano_anio})`).join(" → ")}; el resto, abajo.

```js
completos.length < 2
  ? html`<p class="muted">Hacen falta al menos dos temporadas completas.</p>`
  : Plot.plot({
      width,
      height: 70 + 40 * topCod.length,
      marginLeft: 170,
      x: {grid: true, label: "Pasajeros en la temporada", tickFormat: entero},
      y: {domain: topCod.map((c) => nombreCod.get(c)), label: null},
      color: {legend: true, type: "ordinal", domain: completos, range: SEQ.slice(-completos.length), tickFormat: (y) => `Verano ${y}`},
      marks: [
        Plot.link(d3.groups(verTop, (d) => d.ciudad), {x1: ([, v]) => d3.min(v, (d) => d.pasajeros), x2: ([, v]) => d3.max(v, (d) => d.pasajeros), y1: ([c]) => c, y2: ([c]) => c, stroke: OTRO, strokeWidth: 2}),
        Plot.dot(verTop, {x: "pasajeros", y: "ciudad", fill: "verano_anio", r: 7, stroke: "var(--theme-background)", strokeWidth: 2, tip: true,
          title: (d) => `${d.ciudad} · verano ${d.verano_anio}\n${d.pasajeros ? `${entero(d.pasajeros)} pasajeros` : "sin vuelos de línea"}`}),
        Plot.ruleX([0])
      ]
    })
```

<h2 id="05" data-idx="05 — Día por día">El pulso diario</h2>

Cada punto es un día. La línea negra es el promedio de 7 días; la gris punteada, el mismo período del año anterior.

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 50,
  y: {grid: true, label: "Pasajeros por día", tickFormat: entero},
  x: {label: null, tickFormat: fechaEje},
  marks: [
    Plot.dot(diario, {x: "fecha", y: "pasajeros", r: 1.6, fill: TINTA_2, fillOpacity: 0.35}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7_anio_anterior", stroke: OTRO, strokeDasharray: "3,3", strokeWidth: 1.5}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7", stroke: TINTA, strokeWidth: 1.8}),
    Plot.ruleY([0]),
    Plot.tip(diario, Plot.pointerX({x: "fecha", y: "pasajeros_ma7",
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\nPasajeros: ${entero(d.pasajeros)}\nPromedio 7 días: ${entero(d.pasajeros_ma7)}${d.var_ma7_interanual == null ? "" : `\nvs. año anterior: ${variacion(d.var_ma7_interanual)}`}`}))
  ]
})
```

### Días atípicos

Paros, temporales y feriados dejan su marca en la serie diaria.

```js
const ev = new Map(eventos.map((e) => [e.fecha, e]));
const at = atipicos.filter((d) => d.z != null).map((d) => ({...d, evento: ev.get(d.fecha.toISOString().slice(0, 10))}));
const marcados = at.filter((d) => d.es_atipico);
```

```js
// Qué parte de los días con cada condición tuvo una caída fuerte (>20 % menos de lo esperado).
const porClima = d3.rollups(at.filter((d) => d.condicion && d.esperado > 0), (v) => ({dias: v.length, caidas: v.filter((d) => d.desvio_pct < -0.2).length}), (d) => d.condicion)
  .map(([condicion, v]) => ({condicion, ...v, share: v.caidas / v.dias})).sort((a, b) => b.share - a.share);
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 45,
  y: {grid: true, label: "Desvío respecto de lo esperable (z)", domain: [d3.min(at, (d) => d.z), d3.max(at, (d) => d.z)]},
  x: {label: null, tickFormat: fechaEje},
  marks: [
    Plot.ruleY([-3, 3], {stroke: ACENTO, strokeDasharray: "2,3"}),
    Plot.ruleY([0], {stroke: TINTA_2}),
    Plot.dot(at.filter((d) => !d.es_atipico), {x: "fecha", y: "z", r: 1.6, fill: TINTA_2, fillOpacity: 0.4}),
    Plot.dot(marcados, {x: "fecha", y: "z", r: 4, fill: ACENTO, tip: true,
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\n${entero(d.pasajeros)} pasajeros (esperado ${entero(d.esperado)})${d.evento ? `\n${d.evento.evento}` : ""}${d.condicion && d.condicion !== "normal" ? `\nClima: ${d.condicion}` : ""}`}),
    Plot.text(marcados.filter((d) => d.evento), {x: "fecha", y: "z", text: () => "paro", dy: 14, fontSize: 11, fill: ACENTO})
  ]
})
```

<div class="leyenda-grid">
  <p><b>Cómo leerlo.</b> Cada punto es un día comparado con lo que suele pasar ese mismo día de la semana en esa época del año. Los puntos bermellón se alejaron más de 3 desvíos: casi siempre caídas fuertes.</p>
  <p><b>Paros.</b> ${marcados.filter((d) => d.evento).map((d) => html`<a href=${d.evento.fuente} target="_blank" rel="noopener">${d.fecha.toLocaleDateString("es-AR", {timeZone: "UTC"})}</a>`).reduce((acc, x, i) => i ? [...acc, " · ", x] : [x], [])} — los días con cero vuelos coinciden con paros generales o aeronáuticos.</p>
  <p><b>Clima.</b> ${porClima.length > 1 ? porClima.map((d) => `${d.condicion}: ${pct(d.share)} de los días con caída de más de 20 %`).join(" · ") : "Sin datos de clima."}</p>
</div>

<h2 id="06" data-idx="06 — Operación">Un día en el aeropuerto</h2>

Aterrizajes y despegues de línea promedio por semana, según día y hora.

```js
const anioHora = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
```

```js
Plot.plot({
  width,
  height: ALTO.medio,
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

<h2 id="07" data-idx="07 — Conectividad">A dónde se vuela</h2>

La línea aérea une a Mar del Plata casi solo con el resto del país, y sobre todo con Buenos Aires. El mapa cambia cuando se mira **toda la aviación**: aparecen decenas de aeródromos chicos, Uruguay, Chile y Brasil, y vuelos ejecutivos que llegan desde Estados Unidos o el Caribe.

```js
const anioMapa = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
const modoMapa = view(Inputs.radio(["Línea aérea (pasajeros)", "Toda la aviación (movimientos)"], {value: "Toda la aviación (movimientos)"}));
```

```js
const PAIS = (c) => c == null ? "Sin identificar" : c === "FK" ? "Islas Malvinas" : c === "AR" ? "Argentina" : new Intl.DisplayNames(["es"], {type: "region"}).of(c);
// Recorte del mapa: cono sur. Lo que queda afuera se dibuja como una flecha hacia el borde.
const CAJA = {latMin: -56, latMax: -14, lonMin: -76, lonMax: -40};
const enCaja = ([lon, lat]) => lat >= CAJA.latMin && lat <= CAJA.latMax && lon >= CAJA.lonMin && lon <= CAJA.lonMax;
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
const foco = rutas.find((d) => d.foco_lat != null);
const origen = [foco.foco_lon, foco.foco_lat];
const enMapa = puntos.filter((d) => d.lat != null && enCaja([d.lon, d.lat]) && d.codigo !== "MDP");
// Destinos fuera del recorte: punto donde la ruta (círculo máximo) sale de la caja.
const lejanos = puntos.filter((d) => d.lat != null && !enCaja([d.lon, d.lat])).map((d) => {
  const ruta = d3.geoInterpolate(origen, [d.lon, d.lat]);
  let t = 0;
  while (t < 1 && enCaja(ruta(t + 0.005))) t += 0.005;
  const [lonB, latB] = ruta(t);
  return {...d, lonB, latB};
});
const maxValor = d3.max([...enMapa, ...lejanos], (d) => d.valor);
const etiquetas = d3.sort(enMapa.filter((d) => Math.hypot(d.lon - origen[0], d.lat - origen[1]) > 1.2), (d) => -d.valor)
  .filter((d, i, arr) => !arr.slice(0, i).some((o) => Math.hypot(o.lon - d.lon, o.lat - d.lat) < 2.2)).slice(0, 14);
// Rótulos de destinos lejanos: uno por zona del borde (el detalle está en "Destinos lejanos").
const rotulosLejanos = d3.sort(lejanos, (d) => -d.valor)
  .filter((d, i, arr) => !arr.slice(0, i).some((o) => Math.hypot(o.lonB - d.lonB, o.latB - d.latB) < 3.5));
const unidad = esLinea ? "pasajeros" : "movimientos";
const grosor = (d) => 0.6 + 7 * Math.sqrt(d.valor / maxValor);
const colorDe = (d) => d.internacional ? "Exterior" : "Argentina";
```

<div class="mapa-grid">
<div>

```js
resize((w) => Plot.plot({
  width: w, height: Math.round(w * 1.08),
  projection: {type: "mercator", inset: 28,
    domain: {type: "MultiPoint", coordinates: [[CAJA.lonMin, CAJA.latMin], [CAJA.lonMax, CAJA.latMax]]}},
  r: {range: [2.5, 22]},
  color: {domain: ["Argentina", "Exterior"], range: [TINTA_2, ACENTO], legend: true},
  marks: [
    Plot.geo(paises, {fill: TINTA, fillOpacity: 0.05, stroke: TINTA, strokeOpacity: 0.25}),
    Plot.link(enMapa, {x1: () => origen[0], y1: () => origen[1], x2: "lon", y2: "lat", stroke: colorDe, strokeOpacity: 0.45, strokeWidth: grosor}),
    Plot.link(lejanos, {x1: () => origen[0], y1: () => origen[1], x2: "lonB", y2: "latB", stroke: colorDe, strokeOpacity: 0.6, strokeWidth: grosor, markerEnd: "arrow"}),
    Plot.dot(enMapa, {x: "lon", y: "lat", r: "valor", fill: colorDe, stroke: "var(--theme-background)", strokeWidth: 1.5, tip: true,
      title: (d) => `${nombreDestino(d)} (${d.codigo})${d.internacional ? ` · ${PAIS(d.pais)}` : ""}\n${entero(d.valor)} ${unidad}` +
        (esLinea ? `\n${decimal1(d.salidas_semanales_promedio)} salidas por semana` : `\nSobre todo: ${SEG_NOMBRE[d.segmento] ?? d.segmento}`)}),
    ...[[(d) => d.latB >= CAJA.latMax - 0.5, 14], [(d) => d.latB < CAJA.latMax - 0.5, -10]].map(([filtro, dy]) =>
      Plot.text(rotulosLejanos.filter(filtro), {x: "lonB", y: "latB", text: (d) => `${nombreDestino(d)} · ${entero(d.distancia_mdq_km)} km`, dy, fontSize: 11, fill: ACENTO, stroke: "var(--theme-background)", strokeWidth: 3,
        textAnchor: (d) => (d.lonB > -50 ? "end" : "start")})),
    Plot.text(etiquetas, {x: "lon", y: "lat", text: nombreDestino, dy: -12, fontSize: 12, fill: TINTA, stroke: "var(--theme-background)", strokeWidth: 3}),
    Plot.dot([foco], {x: "foco_lon", y: "foco_lat", r: 6, fill: TINTA}),
    Plot.text([foco], {x: "foco_lon", y: "foco_lat", text: () => "Mar del Plata", dx: 10, textAnchor: "start", fontWeight: "bold", fontSize: 13})
  ]
}))
```

</div>
<div>

```js
html`<table class="editorial"><thead><tr><th>Destino</th><th>${esLinea ? "Pasajeros" : "Movim."}</th><th>${esLinea ? "Salidas/sem." : "Sobre todo"}</th></tr></thead><tbody>
${d3.sort(puntos.filter((d) => d.lat != null), (d) => -d.valor).slice(0, 24).map((d) => html`<tr class=${d.internacional ? "foco" : ""}><td>${nombreDestino(d)}${d.internacional ? ` (${PAIS(d.pais)})` : ""}</td><td>${entero(d.valor)}</td><td>${esLinea ? decimal1(d.salidas_semanales_promedio) : SEG_NOMBRE[d.segmento] ?? d.segmento}</td></tr>`)}
</tbody></table>`
```

</div>
</div>

### Vuelos al exterior

```js
const esNumerico = (d) => /^\d+$/.test(d.codigo);
const intl = destinos.filter((d) => d.clasificacion_vuelo === "internacional" && !esNumerico(d));
const intlAnio = intl.filter((d) => d.anio === anioMapa);
const intlTotal = d3.sum(intlAnio, (d) => d.movimientos);
const intlLinea = d3.sum(intlAnio.filter((d) => d.es_linea), (d) => d.movimientos);
const paisesTop = d3.groupSort(intl.filter((d) => d.pais), (v) => -d3.sum(v, (d) => d.movimientos), (d) => d.pais).slice(0, 5);
const grupoPais = (d) => paisesTop.includes(d.pais) ? PAIS(d.pais) : "Otros países";
const ordenPais = [...paisesTop.map(PAIS), "Otros países"];
```

<div class="cifras c3">
  <div><span class="rotulo">Movimientos con el exterior · ${anioMapa}</span><span class="valor">${entero(intlTotal)}</span><div class="nota">${pct1(intlTotal / d3.sum(destinos.filter((d) => d.anio === anioMapa), (d) => d.movimientos))} de todos los movimientos del aeropuerto</div></div>
  <div><span class="rotulo">De línea aérea</span><span class="valor">${entero(intlLinea)}</span><div class="nota">el resto es aviación ejecutiva, privada y oficial</div></div>
  <div><span class="rotulo">Países</span><span class="valor">${new Set(intlAnio.filter((d) => d.pais).map((d) => d.pais)).size}</span><div class="nota">${d3.groupSort(intlAnio.filter((d) => d.pais), (v) => -d3.sum(v, (d) => d.movimientos), (d) => d.pais).slice(0, 3).map(PAIS).join(", ")}</div></div>
</div>

<div class="grid-2">
<div>

```js
Plot.plot({
  title: "Movimientos con el exterior por país",
  width: width / 2 - 20, height: ALTO.medio, marginLeft: 50, marginBottom: 45,
  x: ejeAnios, y: {label: "Movimientos", grid: true},
  color: {domain: ordenPais, range: [...CAT.slice(0, paisesTop.length), OTRO], legend: true},
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
  width: width / 2 - 20, height: ALTO.medio, marginLeft: 150,
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

### Destinos lejanos

Los vuelos que salen del mapa: de dónde vinieron o a dónde fueron, en qué avión y quién los operó.

```js
const PAIS_LEJ = (c) => c === "AR" ? "Argentina" : new Intl.DisplayNames(["es"], {type: "region"}).of(c);
const porDestino = d3.groups(exoticos.filter((d) => !enCaja([d.lon, d.lat])), (d) => d.codigo).map(([codigo, v]) => ({
  codigo, ciudad: v[0].ciudad ?? v[0].nombre, pais: v[0].pais, km: v[0].distancia_mdq_km,
  vuelos: v.length, anios: d3.extent(v, (d) => d.anio), ultimos: d3.sort(v, (d) => -d.fecha).slice(0, 3)
})).sort((a, b) => b.km - a.km);
```

```js
html`<div class="lejanos">${porDestino.map((d) => html`<div class="lejano">
  <span class="seg">${PAIS_LEJ(d.pais)} · ${entero(d.km)} km</span>
  <div class="modelo">${d.ciudad}</div>
  <p class="resumen">${d.vuelos} ${d.vuelos === 1 ? "movimiento" : "movimientos"}${d.anios[0] !== d.anios[1] ? ` entre ${d.anios[0]} y ${d.anios[1]}` : ` en ${d.anios[0]}`}</p>
  <ul>${d.ultimos.map((v) => html`<li><span>${v.fecha.toLocaleDateString("es-AR", {timeZone: "UTC"})}</span> ${v.tipo_movimiento === "aterrizaje" ? "llegó" : "salió"}${v.aeronave && v.aeronave !== "Sin dato" ? ` · ${v.aeronave}` : ""}${v.aerolinea_nombre && v.aerolinea_nombre !== "Sin dato" ? ` · ${v.aerolinea_nombre}` : ""}${v.pasajeros > 0 ? ` · ${v.pasajeros} pax` : ""}</li>`)}</ul>
</div>`)}</div>`
```

<h2 id="08" data-idx="08 — Mercado">Quién vuela</h2>

Qué parte de los pasajeros de línea llevó cada aerolínea, año por año. Aerolíneas Argentinas concentra casi todo el mercado; las low cost y las regionales aparecen y desaparecen.

```js
const comerciales = aerolineas.filter((d) => d.aerolinea_nombre !== "Sin dato");
const aer = topN(comerciales, "aerolinea_nombre", "pasajeros", 5);
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
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

<p class="cobertura">${notaCobertura(cob, {alcance: "linea", campo: "pct_operador", que: "aerolínea conocida", sobre: "movimientos de línea"})}</p>

<h2 id="09" data-idx="09 — Oferta">Asientos y ocupación</h2>

Vuelos de línea: pasajeros transportados y asientos ofrecidos (estimados) por mes. La distancia entre ambas líneas son asientos que volaron vacíos.

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 50,
  y: {grid: true, label: "Por mes", tickFormat: entero},
  x: {label: null, tickFormat: fechaEje},
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

<p class="cobertura">${notaCobertura(cob, {alcance: "linea", campo: "pct_asientos", que: "asientos conocidos (del vuelo exacto, de la cabina publicada o estimados)", sobre: "movimientos de línea"})} Los meses con menos cobertura subestiman la oferta.</p>


<h2 id="10" data-idx="10 — Flota">En qué aviones</h2>

<p class="intro-ancha">Los vuelos de línea a Mar del Plata se hacen sobre todo en Embraer E190, el jet regional de 96 asientos de Aerolíneas, y en Boeing 737 en temporada alta o en las rutas más cargadas. En 2015 todavía volaban Saab 340 y MD-80; entre 2017 y 2019, los ATR de Avianca. Desde la pandemia, casi todo se reduce a esas dos familias.</p>

```js
const flotaHist = historiaSeg.filter((d) => d.anio < 2019 && ["linea_regular", "charter_linea"].includes(d.segmento))
  .map((d) => ({anio: d.anio, familia: d.aeronave_familia, movimientos: d.movimientos}));
const flotaAnac = aeronavesM.filter((d) => d.es_linea)
  .map((d) => ({anio: d.anio, familia: d.aeronave_familia_inferida, movimientos: d.movimientos, inferida: d.aeronave_inferida}));
const flota = [...flotaHist, ...flotaAnac];
const fam = topN(flota.filter((d) => d.familia !== "Sin dato"), "familia", "movimientos", 6);
const famLabel = (d) => d.familia === "Sin dato" ? "Sin dato" : fam.label(d);
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 50,
  y: {percent: true, label: "% de movimientos de línea", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...fam.top, "Otras", "Sin dato"], range: [...CAT.slice(0, fam.top.length), OTRO, "#d6d3cb"]},
  marks: [
    Plot.barY(flota, Plot.stackY(Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: famLabel, order: [...fam.top, "Otras", "Sin dato"], offset: "normalize", inset: 1, tip: true}))),
    Plot.ruleY([0])
  ]
})
```

<p class="cobertura">${notaCobertura(cob, {alcance: "linea", campo: "pct_aeronave_con_inferida", que: "avión conocido o deducido", sobre: "movimientos de línea"})} Lo deducido (por pasajeros o por los asientos del vuelo) se explica en <a href="./metodologia">Metodología</a>.</p>

### Modelo por modelo

<p class="intro-ancha">Desde 2021, modelo por modelo: el E190 hace la base del año y los Boeing 737-700, 737-800 y 737 MAX 8 suman capacidad cuando la demanda sube.</p>

```js
const modelosLinea = aeronavesM.filter((d) => d.es_linea && d.anio >= 2021 && d.aeronave_familia !== "Sin dato");
const mod = topN(modelosLinea, "aeronave_modelo", "movimientos", 6);
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
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

<p class="cobertura">${notaCobertura(cob, {alcance: "linea", campo: "pct_aeronave", que: "modelo informado o recuperado", sobre: "movimientos de línea", desde: 2021})}</p>

<h2 id="11" data-idx="11 — Toda la actividad">Todo lo que vuela</h2>

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
  height: ALTO.serie,
  marginLeft: 50,
  y: {grid: true, label: "Aterrizajes y despegues por mes", tickFormat: entero},
  x: {label: null, tickFormat: fechaEje},
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

### El avión típico

El modelo más frecuente de cada actividad en ${ref.anio}. En taxi aéreo se suma el **avión básico**: el turbohélice más usado, el estándar del vuelo ejecutivo.

```js
const tip = avionTipico.filter((d) => d.anio === ref.anio);
const top1 = (seg) => tip.find((d) => d.segmento === seg && d.ranking === 1);
const fichas = [
  {...top1("linea_regular"), etiqueta: "Línea regular"},
  {...top1("charter_linea"), etiqueta: "Charter de línea"},
  {...top1("taxi_aereo"), etiqueta: "Taxi aéreo"},
  {...tip.find((d) => d.segmento === "taxi_aereo" && d.perfil === "turbohelice" && d.ranking_en_perfil === 1), etiqueta: "Taxi aéreo · avión básico"},
  {...top1("instruccion"), etiqueta: "Escuelas de vuelo"}
].filter((f) => f.aeronave_familia);
const filas = (f) => [
  ["Movimientos", `${entero(f.movimientos)} (${pct(f.share_en_segmento)})`],
  ["Pasajeros promedio", decimal1(f.pax_promedio)],
  ["Lleva hasta (habitual)", f.capacidad_observada_p95],
  ["Duración de vuelo", f.duracion_vuelo_mediana_min != null ? `${Math.round(f.duracion_vuelo_mediana_min)} min` : null],
  ["Hora más frecuente", `${f.hora_mas_frecuente} h`],
  ["Va y viene de", f.principales_origenes_destinos]
].filter(([, v]) => v != null).flatMap(([a, b]) => [html`<dt>${a}</dt>`, html`<dd>${b}</dd>`]);
```

```js
html`<div class="fichas">${fichas.map((f) => html`<div class="ficha">
  <span class="seg" style="color:${SEG_COLOR[f.segmento]}">${f.etiqueta}</span>
  <div class="modelo">${f.aeronave_familia}</div>
  <dl>${filas(f)}</dl></div>`)}</div>`
```

<p class="cobertura">${notaCobertura(cob, {alcance: "resto", campo: "pct_aeronave", que: "avión conocido", sobre: "movimientos fuera de línea de", desde: ref.anio, hasta: ref.anio})} El resto no entra en el ranking.</p>

### Desde 2015

Cómo cambió la mezcla de actividades en la pista, año por año.

```js
const hs = d3.rollups(historiaSeg, (v) => ({movimientos: d3.sum(v, (d) => d.movimientos), fuente: v[0].fuente}), (d) => d.anio, (d) => d.segmento)
  .flatMap(([anio, segs]) => segs.map(([segmento, v]) => ({anio, segmento, nombre: SEG_NOMBRE[segmento] ?? segmento, ...v})));
```

```js
Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 50,
  y: {percent: true, label: "% de los movimientos", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {...segColor, legend: true},
  marks: [
    Plot.barY(hs, Plot.stackY({x: "anio", y: "movimientos", fill: "nombre", order: segColor.domain, offset: "normalize", inset: 0.5, tip: true,
      title: (d) => `${d.nombre} ${d.anio}\n${entero(d.movimientos)} movimientos`})),
    Plot.ruleY([0])
  ]
})
```

<div class="leyenda-grid">
  <p><b>Cómo se agrupa.</b> Cada vuelo entra en el segmento que declara su operador a la ANAC: línea regular, no regular, privado, oficial o escuela. Los no regulares en aviones de línea son <i>charter</i>; el resto, <i>taxi aéreo</i>.</p>
  <p><b>Tres ajustes.</b> Un vuelo privado en jet o turbohélice ejecutivo se cuenta como <i>taxi aéreo</i> (casi siempre es un operador de taxi posicionando el avión). Un taxi aéreo declarado en un avión a pistón de menos de 6 plazas se cuenta como <i>privado</i>. Un vuelo de una escuela de vuelo (CIAC, aeroclub, academia) declarado como privado o no regular se cuenta como <i>escuela</i>.</p>
  <p><b>El límite.</b> ${(() => { const c = cob.find((d) => d.anio === ref.anio && d.alcance === "resto"); return c ? `En ${ref.anio}, fuera de la línea, la ANAC informa el operador en el ${pct(c.pct_operador_anac)} de los movimientos; con los cruces de matrícula, Afectación y el otro extremo del vuelo llega al ${pct(c.pct_operador)}. La frontera entre privado, taxi y escuela depende en parte de lo que declara cada piloto.` : ""; })()}</p>
</div>

<h2 id="12" data-idx="12 — Pronóstico">Lo que viene</h2>

Proyección de pasajeros de línea para los próximos 6 meses si se repite el patrón de las últimas temporadas. La banda marca el rango probable. No anticipa rutas nuevas ni cambios de aerolíneas.

```js
const obs = pronostico.filter((d) => d.tipo === "observado");
const fut = pronostico.filter((d) => d.tipo === "pronostico");
```

```js
Plot.plot({
  width,
  height: ALTO.serie,
  marginLeft: 50,
  y: {grid: true, label: "Pasajeros por mes", tickFormat: compacto},
  x: {label: null, tickFormat: fechaEje},
  marks: [
    Plot.areaY(fut, {x: "periodo", y1: "p10", y2: "p90", fill: ACENTO, fillOpacity: 0.15}),
    Plot.lineY(obs.slice(-30), {x: "periodo", y: "pasajeros", stroke: TINTA, strokeWidth: 1.8}),
    Plot.lineY([obs.at(-1), ...fut], {x: "periodo", y: "pasajeros", stroke: ACENTO, strokeWidth: 2, strokeDasharray: "4,3"}),
    Plot.ruleY([0]),
    Plot.tip(fut, Plot.pointerX({x: "periodo", y: "pasajeros", title: (d) => `${MESES[d.periodo.getUTCMonth()]} ${d.periodo.getUTCFullYear()}\n${entero(d.pasajeros)} (rango ${entero(d.p10)}–${entero(d.p90)})`}))
  ]
})
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
