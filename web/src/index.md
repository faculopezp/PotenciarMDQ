---
title: Mar del Plata despega
---

<link rel="stylesheet" href="./components/inputs.css">

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import * as Inputs from "@observablehq/inputs";
import {html} from "htl";
import {CAT, OTRO, SEQ, DIV, FOCO, entero, pct, variacion, decimal1, MESES, DIAS, CLASES,
  datos, ultimoAnioCompleto, veranosCompletos, topN} from "./components/util.js";
```

```js
const anual = datos(FileAttachment("data/mdq_anual.json"));
const mensual = datos(FileAttachment("data/mdq_mensual.json"));
const diario = datos(FileAttachment("data/mdq_diario.json"));
const horaSemana = datos(FileAttachment("data/mdq_hora_semana.json"));
const aerolineas = datos(FileAttachment("data/mdq_aerolineas.json"));
const aeronaves = datos(FileAttachment("data/mdq_aeronaves.json"));
const rutas = datos(FileAttachment("data/mdq_rutas.json"));
const verano = datos(FileAttachment("data/mdq_verano.json"));
const rotaciones = datos(FileAttachment("data/mdq_rotaciones.json"));
const tramos = datos(FileAttachment("data/mdq_tramos.json"));
const general = datos(FileAttachment("data/mdq_aviacion_general.json"));
const pares = datos(FileAttachment("data/benchmark_pares.json"));
const paises = FileAttachment("data/sudamerica.json").json();
const hitos = FileAttachment("data/hitos.json").json();
```

```js
const ref = ultimoAnioCompleto(anual);
const anios = anual.map((d) => d.anio);
const desde = d3.min(diario, (d) => d.fecha);
const hasta = d3.max(diario, (d) => d.fecha);
const fechaLarga = (d) => d.toLocaleDateString("es-AR", {day: "numeric", month: "long", year: "numeric", timeZone: "UTC"});
```

<div class="hero">
  <h1>Mar del Plata despega</h1>
  <h2>Cómo vuela la ciudad: pasajeros, rutas, aviones y temporadas en el Aeropuerto Astor Piazzolla, con datos abiertos de la ANAC.</h2>
  <p class="muted">Datos del ${fechaLarga(desde)} al ${fechaLarga(hasta)}. Las cifras principales usan ${ref.anio}, el último año completo.</p>
</div>

<div class="grid grid-cols-4">
  <div class="card"><h2>Pasajeros en ${ref.anio}</h2><span class="big">${entero(ref.pasajeros)}</span>
    <p class="muted">${ref.var_interanual == null ? "" : `${variacion(ref.var_interanual)} vs. ${ref.anio - 1}`}</p></div>
  <div class="card"><h2>Vuelos comerciales por día</h2><span class="big">${decimal1(ref.movimientos_comerciales / 2 / 365)}</span>
    <p class="muted">${entero(ref.movimientos_comerciales)} aterrizajes y despegues en el año</p></div>
  <div class="card"><h2>Destinos directos</h2><span class="big">${ref.destinos_regulares}</span>
    <p class="muted">con vuelos regulares</p></div>
  <div class="card"><h2>Ocupación estimada</h2><span class="big">${pct(ref.lf_estimado)}</span>
    <p class="muted">de los asientos se vendieron (estimación)</p></div>
</div>

## 1. El pulso del aeropuerto

Cada punto es un día. La línea azul es el promedio de los últimos 7 días; la gris punteada, el mismo período del año anterior. Se ve el ritmo de la ciudad: el pico de enero, la calma del invierno y los saltos de los fines de semana largos.

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {grid: true, label: "Pasajeros por día", tickFormat: entero},
  x: {label: null},
  marks: [
    Plot.dot(diario, {x: "fecha", y: "pasajeros", r: 1.5, fill: SEQ[1], fillOpacity: 0.5}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7_anio_anterior", stroke: OTRO, strokeDasharray: "3,3", strokeWidth: 1.5}),
    Plot.lineY(diario, {x: "fecha", y: "pasajeros_ma7", stroke: FOCO, strokeWidth: 2}),
    Plot.ruleY([0]),
    Plot.tip(diario, Plot.pointerX({x: "fecha", y: "pasajeros_ma7",
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\nPasajeros: ${entero(d.pasajeros)}\nPromedio 7 días: ${entero(d.pasajeros_ma7)}${d.var_ma7_interanual == null ? "" : `\nvs. año anterior: ${variacion(d.var_ma7_interanual)}`}`}))
  ]
})
```

## 2. Un calendario que respira con el verano

Cuanto más oscuro el cuadrado, más pasajeros ese día. El verano se ve a simple vista.

```js
const semana = (d) => d3.utcMonday.count(d3.utcYear(d.fecha), d.fecha);
const diaSemana = (d) => (d.fecha.getUTCDay() + 6) % 7;
const inicioMes = d3.range(12).map((m) => ({m, x: d3.utcMonday.count(new Date(Date.UTC(2025, 0, 1)), new Date(Date.UTC(2025, m, 1)))}));
```

```js
Plot.plot({
  width,
  height: 40 + 110 * new Set(diario.map((d) => d.anio)).size,
  padding: 0.08,
  x: {axis: "top", ticks: inicioMes.map((d) => d.x), tickFormat: (x) => MESES[inicioMes.find((d) => d.x === x)?.m] ?? "", tickSize: 0, label: null},
  y: {tickFormat: (i) => DIAS[i], tickSize: 0, label: null},
  fy: {tickFormat: "d", label: null},
  color: {type: "linear", range: [SEQ[0], SEQ[4]], legend: true, label: "Pasajeros por día", tickFormat: entero},
  marks: [
    Plot.cell(diario, {x: semana, y: diaSemana, fy: "anio", fill: "pasajeros", rx: 2, tip: true,
      title: (d) => `${fechaLarga(d.fecha)}${d.feriado_nombre ? ` · ${d.feriado_nombre}` : ""}\n${entero(d.pasajeros)} pasajeros`})
  ]
})
```

### ¿La ciudad se llena o se vacía?

Diferencia entre pasajeros que llegaron y que se fueron cada mes. Azul: llegó más gente de la que se fue. Rojo: se fue más de la que llegó.

```js
Plot.plot({
  width,
  height: 260,
  marginLeft: 50,
  y: {grid: true, label: "Llegados − salidos", tickFormat: entero},
  x: {label: null},
  marks: [
    Plot.rectY(mensual, {x1: "periodo", x2: (d) => d3.utcMonth.offset(d.periodo, 1), y: "balance_pasajeros", inset: 1,
      fill: (d) => (d.balance_pasajeros >= 0 ? DIV.pos : DIV.neg), tip: true,
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\nLlegaron ${entero(d.pasajeros_llegados)}\nSe fueron ${entero(d.pasajeros_salidos)}\nBalance ${entero(d.balance_pasajeros)}`}),
    Plot.ruleY([0])
  ]
})
```

## 3. ¿Cuántos asientos se ofrecen y cuántos se llenan?

Pasajeros transportados y asientos ofrecidos (estimados) por mes. La distancia entre las dos líneas son asientos que volaron vacíos.

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {grid: true, label: "Por mes", tickFormat: entero},
  x: {label: null},
  color: {legend: true, domain: ["Asientos ofrecidos (est.)", "Pasajeros"], range: [OTRO, FOCO]},
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

<div class="note">La ANAC no publica asientos. Los estimamos con la capacidad típica observada de cada avión (ver <a href="./metodologia">metodología</a>).</div>

## 4. ¿A dónde se puede volar?

```js
const anioMapa = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
```

```js
const rutasAnio = rutas.filter((d) => d.anio === anioMapa && d.lat != null && d.pasajeros >= 50);
const maxPax = d3.max(rutasAnio, (d) => d.pasajeros);
const foco = rutas.find((d) => d.foco_lat != null);
const anchoMapa = Math.min(width, 720);
// Etiquetas: se omite la de un punto a menos de 1° de otro más grande (ej. Ezeiza vs Aeroparque).
const etiquetas = rutasAnio.filter((d) => !rutasAnio.some((o) => o.pasajeros > d.pasajeros && Math.hypot(o.lon - d.lon, o.lat - d.lat) < 1));
```

```js
Plot.plot({
  width: anchoMapa,
  height: anchoMapa * 1.1,
  projection: {type: "mercator", inset: 40,
    domain: {type: "MultiPoint", coordinates: [[foco.foco_lon, foco.foco_lat], ...rutasAnio.map((d) => [d.lon, d.lat])]}},
  r: {range: [3, 20]},
  marks: [
    Plot.geo(paises, {fill: "currentColor", fillOpacity: 0.06, stroke: "currentColor", strokeOpacity: 0.25}),
    Plot.link(rutasAnio, {x1: "foco_lon", y1: "foco_lat", x2: "lon", y2: "lat", stroke: FOCO,
      strokeOpacity: 0.6, strokeWidth: (d) => 1 + 8 * Math.sqrt(d.pasajeros / maxPax)}),
    Plot.dot(rutasAnio, {x: "lon", y: "lat", r: "pasajeros", fill: FOCO, stroke: "var(--theme-background)", strokeWidth: 2, tip: true,
      title: (d) => `${d.ciudad}\n${entero(d.pasajeros)} pasajeros con MDQ\n${d.salidas_semanales_promedio} salidas por semana${d.duracion_mediana_min ? `\n${d.duracion_mediana_min} min de vuelo` : ""}`}),
    Plot.text(etiquetas, {x: "lon", y: "lat", text: "ciudad", dy: -16, fontSize: 11, fill: "currentColor"}),
    Plot.dot([foco], {x: "foco_lon", y: "foco_lat", r: 6, fill: "currentColor"}),
    Plot.text([foco], {x: "foco_lon", y: "foco_lat", text: () => "Mar del Plata", dx: 10, textAnchor: "start", fontWeight: "bold"})
  ]
})
```

```js
Inputs.table(rutas.filter((d) => d.anio === anioMapa), {
  columns: ["ciudad", "pasajeros", "salidas_semanales_promedio", "duracion_mediana_min", "lf_estimado", "aerolineas"],
  header: {ciudad: "Destino", pasajeros: "Pasajeros", salidas_semanales_promedio: "Salidas/semana", duracion_mediana_min: "Minutos de vuelo", lf_estimado: "Ocupación est.", aerolineas: "Aerolíneas"},
  format: {pasajeros: entero, salidas_semanales_promedio: decimal1, lf_estimado: (x) => (x == null ? "" : pct(x))},
  sort: "pasajeros", reverse: true, rows: 12
})
```

## 5. ¿Quién vuela?

```js
const comerciales = aerolineas.filter((d) => d.aerolinea_nombre !== "Sin dato");
const aer = topN(comerciales, "aerolinea_nombre", "pasajeros", 5);
```

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {percent: true, label: "% de pasajeros", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...aer.top, "Otras"], range: [...CAT.slice(0, aer.top.length), OTRO]},
  marks: [
    Plot.barY(comerciales, Plot.groupX({y: "sum"}, {x: "anio", y: "share_pasajeros", fill: aer.label, inset: 1, tip: true})),
    Plot.ruleY([0])
  ]
})
```

<div class="grid grid-cols-2">
  <div class="card"><h2>Concentración del mercado (HHI) en ${ref.anio}</h2><span class="big">${entero(ref.hhi_aerolineas)}</span>
    <p class="muted">Va de 0 a 10.000. Más de 2.500 es un mercado muy concentrado; 10.000 es un solo operador.</p></div>
  <div class="card"><h2>Aerolíneas comerciales activas</h2><span class="big">${ref.aerolineas_activas}</span>
    <p class="muted">con al menos un vuelo comercial en ${ref.anio} (incluye charter y taxi aéreo)</p></div>
</div>

## 6. ¿En qué aviones?

```js
const flota = aeronaves.filter((d) => d.es_comercial && d.aeronave_familia !== "Sin dato");
const fam = topN(flota, "aeronave_familia", "movimientos", 5);
```

```js
Plot.plot({
  width,
  height: 300,
  marginLeft: 50,
  y: {percent: true, label: "% de aterrizajes y despegues comerciales", grid: true},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: [...fam.top, "Otras"], range: [...CAT.slice(0, fam.top.length), OTRO]},
  marks: [
    Plot.barY(flota, Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: fam.label, offset: "normalize", inset: 1, tip: true})),
    Plot.ruleY([0])
  ]
})
```

## 7. Un día en el aeropuerto

Promedio de aterrizajes y despegues comerciales por semana, según día y hora.

```js
const anioHora = view(Inputs.select(anios.slice().reverse(), {label: "Año", value: ref.anio, format: String}));
```

```js
Plot.plot({
  width,
  height: 260,
  padding: 0.06,
  x: {label: "Hora local", tickFormat: (h) => `${h}h`},
  y: {domain: d3.range(1, 8), tickFormat: (i) => DIAS[i - 1], label: null},
  color: {type: "linear", range: [SEQ[0], SEQ[4]], legend: true, label: "Movimientos por semana"},
  marks: [
    Plot.cell(horaSemana.filter((d) => d.anio === anioHora), {x: "hora_local", y: "dia_semana", fill: "movimientos_por_semana", rx: 2, tip: true,
      title: (d) => `${d.dia_semana_nombre} ${d.hora_local}h\n${decimal1(d.movimientos_por_semana)} movimientos por semana`})
  ]
})
```

```js
const rotAnio = rotaciones.filter((d) => d.anio === ref.anio && d.tipo_rotacion === "rotacion");
const rotFam = d3.rollups(rotAnio, (v) => ({n: d3.sum(v, (d) => d.rotaciones), med: d3.median(v, (d) => d.mediana_min)}), (d) => d.aeronave_familia)
  .filter(([, v]) => v.n >= 100).sort((a, b) => b[1].n - a[1].n).slice(0, 3);
const aep = tramos.filter((d) => d.anio === ref.anio && d.origen === "AER" && d.destino === "MDP");
```

<div class="grid grid-cols-4">
  <div class="card"><h2>Hora pico de diseño</h2><span class="big">${entero(ref.pax_hora_sbr30)}</span>
    <p class="muted">pasajeros en la 30.ª hora más cargada de ${ref.anio} (estándar de planificación)</p></div>
  ${rotFam.map(([f, v]) => html`<div class="card"><h2>Tiempo en tierra · ${f}</h2><span class="big">${Math.round(v.med)} min</span>
    <p class="muted">mediana entre aterrizar y volver a despegar (${entero(v.n)} rotaciones)</p></div>`)}
</div>

${aep.length ? html`<p>Un vuelo desde Aeroparque tarda <b>${Math.round(d3.median(aep, (d) => d.duracion_mediana_min))} minutos</b> de pista a pista (mediana ${ref.anio}).</p>` : ""}

## 8. El verano, temporada contra temporada

Pasajeros por destino en cada verano (diciembre, enero y febrero), destinos con más de 1.000 pasajeros en alguna temporada. Solo temporadas con datos completos.

```js
const completos = veranosCompletos(mensual);
const ver = verano.filter((d) => completos.includes(d.verano_anio) && d.ciudad);
const topDest = d3.rollups(ver, (v) => d3.max(v, (d) => d.pasajeros), (d) => d.ciudad)
  .filter(([, max]) => max >= 1000).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([c]) => c);
const verTop = ver.filter((d) => topDest.includes(d.ciudad));
```

```js
completos.length < 2
  ? html`<p class="muted">Hacen falta al menos dos temporadas completas para comparar.</p>`
  : Plot.plot({
      width,
      height: 60 + 34 * topDest.length,
      marginLeft: 160,
      x: {grid: true, label: "Pasajeros en la temporada", tickFormat: entero},
      y: {domain: topDest, label: null},
      color: {legend: true, type: "ordinal", domain: completos, range: SEQ.slice(-completos.length), tickFormat: (y) => `Verano ${y}`},
      marks: [
        Plot.link(d3.groups(verTop, (d) => d.ciudad), {
          x1: ([, v]) => d3.min(v, (d) => d.pasajeros), x2: ([, v]) => d3.max(v, (d) => d.pasajeros), y1: ([c]) => c, y2: ([c]) => c, stroke: OTRO, strokeWidth: 2}),
        Plot.dot(verTop, {x: "pasajeros", y: "ciudad", fill: "verano_anio", r: 6, stroke: "var(--theme-background)", strokeWidth: 2, tip: true,
          title: (d) => `${d.ciudad} · verano ${d.verano_anio}\n${entero(d.pasajeros)} pasajeros\n${d.salidas} salidas`})
      ]
    })
```

## 9. Más allá de las aerolíneas

No todo lo que despega es un avión de línea: escuelas de vuelo, aviones privados y vuelos oficiales usan el mismo aeropuerto.

```js
const ga = general.map((d) => ({...d, grupo: CLASES[d.clase_vuelo] ?? "Otros"}));
const gruposGA = ["Privado", "Oficial", "Escuela de vuelo", "Otros"];
```

<div class="card"><h2>Movimientos no comerciales en ${ref.anio}</h2><span class="big">${pct(ref.share_movimientos_no_comerciales)}</span>
  <p class="muted">de todos los aterrizajes y despegues del aeropuerto</p></div>

```js
Plot.plot({
  width,
  height: 240,
  marginLeft: 50,
  y: {grid: true, label: "Movimientos no comerciales", tickFormat: entero},
  x: {label: null, tickFormat: "d"},
  color: {legend: true, domain: gruposGA, range: CAT.slice(0, 4)},
  marks: [Plot.barY(ga, Plot.groupX({y: "sum"}, {x: "anio", y: "movimientos", fill: "grupo", inset: 1, tip: true})), Plot.ruleY([0])]
})
```

## 10. Mar del Plata y sus pares

Comparación con otros aeropuertos turísticos y regionales del país en ${ref.anio}.

```js
const paresAnio = pares.filter((d) => d.anio === ref.anio);
const metricaPar = view(Inputs.radio(new Map([
  ["Pasajeros comerciales", "pasajeros_comerciales"],
  ["Estacionalidad (mes pico ÷ mes valle)", "ratio_pico_valle"],
  ["Destinos directos", "destinos_regulares"],
  ["Ocupación estimada", "lf_estimado"]
]), {value: "pasajeros_comerciales", label: "Métrica"}));
```

```js
Plot.plot({
  width,
  height: 260,
  marginLeft: 150,
  x: {grid: true, label: null, tickFormat: metricaPar === "lf_estimado" ? pct : metricaPar === "ratio_pico_valle" ? decimal1 : entero},
  y: {label: null},
  marks: [
    Plot.barX(paresAnio, {x: metricaPar, y: "ciudad", sort: {y: "-x"}, fill: (d) => (d.es_foco ? FOCO : OTRO), rx: 2, tip: true}),
    Plot.ruleX([0])
  ]
})
```

## 11. Línea de tiempo

```js
html`<ul class="timeline">${hitos.map((h) => html`<li><b>${h.fecha}</b> — ${h.titulo}
  <a href=${h.fuente} target="_blank" rel="noopener">(${h.tipo_fuente === "prensa" ? "nota de prensa" : "fuente"})</a></li>`)}</ul>`
```

## Lo que muestran los datos

```js
const delAnio = mensual.filter((d) => d.anio === ref.anio).sort((a, b) => b.pasajeros - a.pasajeros);
const rutasRef = rutas.filter((d) => d.anio === ref.anio).sort((a, b) => b.pasajeros - a.pasajeros);
const shareTop = rutasRef[0].pasajeros / d3.sum(rutasRef, (d) => d.pasajeros);
```

- **Una temporada fuerte:** en ${ref.anio} el mes con más pasajeros (${MESES[delAnio[0].mes - 1]}) movió ${decimal1(ref.ratio_pico_valle)} veces más gente que el más flojo (${MESES[delAnio.at(-1).mes - 1]}).
- **Un puente aéreo con Buenos Aires:** ${pct(shareTop)} de los pasajeros de vuelos regulares viajaron entre Mar del Plata y ${rutasRef[0].ciudad}.
- **Mercado concentrado:** el índice de concentración de aerolíneas fue ${entero(ref.hhi_aerolineas)} sobre 10.000.
- **Aviones llenos:** la ocupación estimada fue ${pct(ref.lf_estimado)} en ${ref.anio}.

<style>
.hero { margin: 2rem 0 1rem; }
.hero h1 { font-size: 3rem; margin: 0; max-width: none; }
.hero h2 { font-weight: 400; color: var(--theme-foreground-muted); max-width: 46rem; }
.timeline { list-style: none; padding-left: 0; }
.timeline li { border-left: 2px solid var(--theme-foreground-faintest); padding: 0.25rem 0 0.75rem 1rem; }
</style>
