---
title: Ómnibus
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, CAT, OTRO, entero, pct, variacion, decimal1, compacto, MESES, ALTO, ejeAnios,
  ultimoAnioCompleto} from "./components/util.js";
```

```js
const anual = await FileAttachment("data/bus_anual.json").json();
const rutas = await FileAttachment("data/bus_rutas.json").json();
const mensual = await FileAttachment("data/bus_mensual.json").json();
const provincias = await FileAttachment("data/bus_origen_provincia.json").json();
const avion = await FileAttachment("data/mdq_anual.json").json();
```

```js
const SERVICIOS = [
  {id: "regular", nombre: "Regular (líneas con horario)", color: TINTA},
  {id: "turismo", nombre: "Turismo (servicios contratados)", color: CAT[1]}
];
const SERV_NOMBRE = Object.fromEntries(SERVICIOS.map((s) => [s.id, s.nombre]));
// Nombres largos, más cortos para gráficos y tablas.
const corto = (n) => (n ?? "").replace("Ciudad Autónoma de Buenos Aires", "Ciudad de Buenos Aires").replace("Ciudad Autónoma De Buenos Aires", "Ciudad de Buenos Aires");
const servColor = {domain: SERVICIOS.map((s) => s.nombre), range: SERVICIOS.map((s) => s.color)};

// Año de referencia: el último que el archivo diario del servicio regular cubre entero.
const regular = anual.filter((d) => d.servicio === "regular");
const ref = regular.filter((d) => d.anio_completo).at(-1) ?? regular.at(-1);
const anioRef = ref?.anio;
const delAnio = (a) => anual.filter((d) => d.anio === a);
const llegadas = (a) => d3.sum(delAnio(a), (d) => d.pasajeros_llegada);
const idaVuelta = (a) => d3.sum(delAnio(a), (d) => d.pasajeros);
const prev = anual.some((d) => d.anio === anioRef - 1) ? anioRef - 1 : null;
const hasta = d3.max(anual, (d) => d.hasta);
const aereo = avion.find((d) => d.anio === anioRef);
const porAvion = aereo ? idaVuelta(anioRef) / aereo.pasajeros_comerciales : null;
const rutasRef = rutas.filter((d) => d.anio === anioRef);
// Localidades con servicio frecuente: 52 viajes o más en el año (ida y vuelta, ambos servicios).
const localidades = d3.rollups(rutasRef, (v) => d3.sum(v, (d) => d.viajes), (d) => d.extremo).filter(([, n]) => n >= 52).length;
const localidadesTodas = new Set(rutasRef.map((d) => d.extremo)).size;
const fechaTxt = (s) => s ? new Date(`${s}T00:00:00Z`).toLocaleDateString("es-AR", {day: "numeric", month: "long", year: "numeric", timeZone: "UTC"}) : "—";
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · micros de larga distancia</p><h1>En micro, <em>desde todo el país</em></h1></div>
  <p class="bajada">Cuántos pasajeros viajan en micro entre Mar del Plata y el resto del país, desde dónde y en qué época, con los datos de la CNRT que publica el Ministerio de Turismo.</p>
</div>

```js
anual.length ? html`<div class="cifras c3">
  <div><span class="rotulo">Llegaron en micro en ${anioRef}</span><span class="valor">${compacto(llegadas(anioRef))}</span><p class="nota">${prev ? `${variacion(llegadas(anioRef) / llegadas(prev) - 1)} contra ${prev} · ` : ""}regular ${compacto(d3.sum(delAnio(anioRef).filter((d) => d.servicio === "regular"), (d) => d.pasajeros_llegada))} · turismo ${compacto(d3.sum(delAnio(anioRef).filter((d) => d.servicio === "turismo"), (d) => d.pasajeros_llegada))}</p></div>
  <div><span class="rotulo">Por cada pasajero de avión</span><span class="valor">${porAvion ? `${decimal1(porAvion)} en micro` : "—"}</span><p class="nota">idas y vueltas de ${anioRef}, línea aérea (ANAC) contra micro</p></div>
  <div><span class="rotulo">Localidades conectadas</span><span class="valor">${entero(localidades)}</span><p class="nota">con 52 viajes o más en ${anioRef} (${entero(localidadesTodas)} con al menos uno)</p></div>
</div>` : html`<p class="leyenda">Todavía no hay datos de micros cargados.</p>`
```

### Año por año

```js
const serie = anual.map((d) => ({...d, servicio_nombre: SERV_NOMBRE[d.servicio]}));
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Pasajeros que llegaron por año", tickFormat: compacto},
  x: ejeAnios,
  color: {...servColor, legend: true},
  marks: [
    Plot.barY(serie, {x: "anio", y: "pasajeros_llegada", fill: "servicio_nombre", fillOpacity: (d) => (d.anio_completo ? 1 : 0.45), inset: 1.5, tip: true,
      title: (d) => `${d.anio} · ${d.servicio_nombre}\n${entero(d.pasajeros_llegada)} pasajeros llegaron\n${entero(d.viajes_llegada)} viajes${d.anio_completo ? "" : `\nAño incompleto (datos del ${fechaTxt(d.desde)} al ${fechaTxt(d.hasta)})`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Las barras claras son años incompletos: los servicios de turismo se registran desde abril de 2019 y la serie llega hasta el ${fechaTxt(hasta)}. ${(() => { const anuales = anual.filter((d) => d.fuente === "anual_por_ruta"); return anuales.length ? `En ${anuales.map((d) => `${d.anio} (${d.servicio})`).join(", ")} solo hay el archivo de rutas con al menos un viaje por semana: un piso, no el total. El resto sale de la base con cada viaje.` : "Todo sale de la base con cada viaje."; })()}</p>

### Desde dónde

```js
const top = d3.rollups(rutasRef, (v) => ({
    llegada: d3.sum(v, (d) => d.pasajeros_llegada),
    salida: d3.sum(v, (d) => d.pasajeros_salida),
    viajes: d3.sum(v, (d) => d.viajes),
    provincia: v.find((d) => d.provincia)?.provincia,
    regular: d3.sum(v.filter((d) => d.servicio === "regular"), (d) => d.pasajeros_llegada),
    turismo: d3.sum(v.filter((d) => d.servicio === "turismo"), (d) => d.pasajeros_llegada)
  }), (d) => corto(d.extremo))
  .map(([extremo, v]) => ({extremo, ...v, provincia: corto(v.provincia)}))
  .sort((a, b) => b.llegada - a.llegada);
const top15 = top.slice(0, 15);
const totalLlegadas = d3.sum(top, (d) => d.llegada);
```

<div class="grid-2">
<div>

```js
Plot.plot({
  width: width / 2 - 20,
  height: 420,
  marginLeft: 190,
  x: {grid: true, label: `Pasajeros que llegaron en ${anioRef}`, tickFormat: compacto},
  y: {label: null, domain: top15.map((d) => d.extremo)},
  marks: [
    Plot.barX(top15, {x: "llegada", y: "extremo", fill: (d, i) => (i === 0 ? ACENTO : TINTA), inset: 2, tip: true,
      title: (d) => `${d.extremo}${d.provincia ? ` (${d.provincia})` : ""}\n${entero(d.llegada)} llegaron · ${entero(d.salida)} salieron\nregular ${entero(d.regular)} · turismo ${entero(d.turismo)}`}),
    Plot.ruleX([0])
  ]
})
```

</div>
<div>

```js
const provRef = d3.rollups(provincias.filter((d) => d.anio === anioRef), (v) => ({pasajeros: d3.sum(v, (d) => d.pasajeros), viajes: d3.sum(v, (d) => d.viajes)}), (d) => corto(d.provincia))
  .map(([provincia, v]) => ({provincia, ...v})).sort((a, b) => b.pasajeros - a.pasajeros).slice(0, 12);
display(Plot.plot({
  width: width / 2 - 20,
  height: 420,
  marginLeft: 190,
  x: {grid: true, label: `Pasajeros que llegaron, por provincia de origen, ${anioRef}`, tickFormat: compacto},
  y: {label: null, domain: provRef.map((d) => d.provincia)},
  marks: [
    Plot.barX(provRef, {x: "pasajeros", y: "provincia", fill: TINTA, inset: 2, tip: true,
      title: (d) => `${d.provincia}\n${entero(d.pasajeros)} pasajeros en ${entero(d.viajes)} viajes`}),
    Plot.ruleX([0])
  ]
}));
```

</div>
</div>

<p class="leyenda">Izquierda: localidad de origen del micro, regular y turismo juntos. ${top.length ? `Las 15 primeras suman el ${pct(d3.sum(top15, (d) => d.llegada) / totalLlegadas)} de las llegadas.` : ""} Derecha: provincia de origen (la traen las bases por viaje).</p>

### La temporada

```js
const temporada = (servicio) => {
  const rows = mensual.filter((d) => d.servicio === servicio);
  const anios = [...new Set(rows.map((d) => d.anio))];
  const completo = anios.filter((a) => rows.filter((d) => d.anio === a).length === 12).at(-1);
  const gris = "#c9c5bb";
  return Plot.plot({
    width: width / 2 - 20,
    height: ALTO.medio,
    marginLeft: 55,
    title: SERV_NOMBRE[servicio],
    y: {grid: true, label: "Pasajeros que llegaron por mes", tickFormat: compacto},
    x: {label: null, domain: d3.range(1, 13), tickFormat: (m) => MESES[m - 1], type: "point"},
    marks: [
      Plot.lineY(rows.filter((d) => d.anio !== completo), {x: "mes", y: "pasajeros_llegada", z: "anio", stroke: gris, strokeWidth: 1.25}),
      Plot.lineY(rows.filter((d) => d.anio === completo), {x: "mes", y: "pasajeros_llegada", stroke: ACENTO, strokeWidth: 2.5}),
      Plot.dot(rows, {x: "mes", y: "pasajeros_llegada", r: 2, fill: (d) => (d.anio === completo ? ACENTO : gris), tip: true,
        title: (d) => `${MESES[d.mes - 1]} ${d.anio}\n${entero(d.pasajeros_llegada)} llegaron · ${entero(d.pasajeros_salida)} salieron\n${entero(d.viajes_llegada)} viajes`}),
      Plot.text(rows.filter((d) => d.anio === completo).slice(-1), {x: "mes", y: "pasajeros_llegada", text: (d) => `${d.anio}`, dx: 14, fill: ACENTO}),
      Plot.ruleY([0])
    ]
  });
};
const rango = (servicio) => {
  const rows = mensual.filter((d) => d.servicio === servicio);
  return rows.length ? `${MESES[rows[0].mes - 1]} ${rows[0].anio} a ${MESES[rows.at(-1).mes - 1]} ${rows.at(-1).anio}` : "sin datos";
};
```

<div class="grid-2">
<div>${mensual.some((d) => d.servicio === "regular") ? temporada("regular") : html`<p class="leyenda">Sin base por viaje del servicio regular.</p>`}</div>
<div>${temporada("turismo")}</div>
</div>

<p class="leyenda">Cada línea es un año; en rojo, el último completo. Bases por viaje: regular de ${rango("regular")}, turismo de ${rango("turismo")}.</p>

### Ruta por ruta, ${anioRef}

<p class="leyenda">Superavitaria: llegaron más pasajeros de los que salieron hacia esa localidad en el año (la ciudad "gana" gente por esa ruta); deficitaria, al revés; pareja, diferencia menor al 5 %.</p>

```js
// Saldo de la ruta: llegaron − salieron. Superavitaria = llegan más de los que se van (±5 % = pareja).
const balance = (d) => {
  const r = d.salida ? d.llegada / d.salida - 1 : Infinity;
  return Math.abs(r) < 0.05 ? {txt: "Pareja", color: TINTA_2} : r > 0 ? {txt: "Superavitaria", color: ACENTO} : {txt: "Deficitaria", color: TINTA};
};
const signo = (v) => (v > 0 ? "+" : v < 0 ? "−" : "") + entero(Math.abs(v));
display(html`<table class="editorial"><thead><tr><th>Localidad</th><th>Provincia</th><th>Llegaron</th><th>Salieron</th><th>Saldo</th><th>Balance</th><th>Viajes</th><th>Regular</th><th>Turismo</th></tr></thead><tbody>
${top.slice(0, 30).map((d) => { const b = balance(d); return html`<tr><td>${d.extremo}</td><td>${d.provincia ?? "—"}</td><td>${entero(d.llegada)}</td><td>${entero(d.salida)}</td><td>${signo(d.llegada - d.salida)}</td><td style=${`color:${b.color};font-weight:600`}>${b.txt}</td><td>${entero(d.viajes)}</td><td>${entero(d.regular)}</td><td>${entero(d.turismo)}</td></tr>`; })}
</tbody></table>`);
```

<div class="leyenda-grid">
  <p><b>Qué se cuenta.</b> Pasajeros de los micros de media y larga distancia de jurisdicción nacional que salen de Mar del Plata o llegan a la ciudad. Regular: las líneas con horario y boleto. Turismo: viajes contratados, excursiones y chárter.</p>
  <p><b>Qué no.</b> Los servicios que no son de jurisdicción nacional (la CNRT no los registra) y, en los años sin base por viaje, las rutas con menos de un viaje por semana.</p>
  <p><b>Límites.</b> La fuente informa el par origen–destino del servicio y en algunas rutas largas registra más pasajeros que asientos (en ${anioRef}, rutas con el ${pct(ref?.share_pax_rutas_sobre_asientos ?? 0)} de los pasajeros regulares), así que no publicamos la ocupación por ruta. Yvera no actualiza el conjunto desde diciembre de 2024. Detalle en <a href="/metodologia">Metodología</a>.</p>
</div>
