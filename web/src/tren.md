---
title: Tren
---

```js
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import {html} from "htl";
import {TINTA, TINTA_2, ACENTO, CAT, OTRO, entero, pct, pct1, variacion, compacto, MESES, ALTO, ejeAnios} from "./components/util.js";
```

```js
const anual = await FileAttachment("data/tren_anual.json").json();
const mensual = (await FileAttachment("data/tren_mensual.json").json()).map((d) => ({...d, periodo: new Date(`${d.periodo}T00:00:00Z`)}));
const servicios = await FileAttachment("data/tren_servicios.json").json();
const porOperador = await FileAttachment("data/tren_operador.json").json();
```

```js
const conDatos = anual.filter((d) => d.pasajeros > 0);
const completos = conDatos.filter((d) => d.anio_completo && d.meses === 12);
const ref = completos.at(-1);
const prev = completos.find((d) => d.anio === ref?.anio - 1);
const record = d3.greatest(completos, (d) => d.pasajeros);
const ultimoMes = mensual.at(-1);
const opNombre = (o) => (o ?? "").replace("FERROBAIRES", "Ferrobaires (provincia)").replace(/SOFS[EA]/g, "Trenes Argentinos (SOFSE)");
const aniosDe = (re) => conDatos.filter((d) => re.test(d.operadores ?? "")).map((d) => d.anio);
const ferro = aniosDe(/FERROBAIRES/), sofse = aniosDe(/SOFS[EA]/);
const ambos = ferro.filter((a) => sofse.includes(a));
const rangoTxt = (a) => (a.length ? (a.length === 1 ? `${a[0]}` : `${d3.min(a)}–${d3.max(a)}`) : "");
// Mismo año, mismo período del año anterior (para el año en curso).
const enCurso = conDatos.at(-1)?.anio !== ref?.anio ? conDatos.at(-1) : null;
const mesesEnCurso = enCurso ? mensual.filter((d) => d.anio === enCurso.anio).map((d) => d.mes) : [];
const mismoPeriodoPrev = enCurso ? d3.sum(mensual.filter((d) => d.anio === enCurso.anio - 1 && mesesEnCurso.includes(d.mes)), (d) => d.pasajeros) : null;
```

<div class="portada">
  <div><p class="etiqueta">PotenciarMDQ · Constitución–Mar del Plata</p><h1>El tren a <em>Mar del Plata</em></h1></div>
  <p class="bajada">Pasajeros del servicio Constitución–Mar del Plata mes por mes desde ${mensual[0]?.anio ?? "2008"}, con los datos que la CNRT publica para todos los trenes de larga distancia del país.</p>
</div>

```js
ref ? html`<div class="cifras c3">
  <div><span class="rotulo">Pasajeros en ${ref.anio}</span><span class="valor">${compacto(ref.pasajeros)}</span><p class="nota">${prev ? `${variacion(ref.pasajeros / prev.pasajeros - 1)} contra ${prev.anio} · ` : ""}${pct(ref.share_larga_distancia)} de la larga distancia del país</p></div>
  <div><span class="rotulo">${enCurso ? `${enCurso.anio}, hasta ${MESES[ultimoMes.mes - 1]}` : "Récord"}</span><span class="valor">${enCurso ? compacto(enCurso.pasajeros) : compacto(record.pasajeros)}</span><p class="nota">${enCurso && mismoPeriodoPrev ? `${variacion(enCurso.pasajeros / mismoPeriodoPrev - 1)} contra el mismo período de ${enCurso.anio - 1}` : `en ${record.anio}`}</p></div>
  <div><span class="rotulo">El mejor año de la serie</span><span class="valor">${compacto(record.pasajeros)}</span><p class="nota">${record.anio} · ${d3.greatest(porOperador.filter((d) => d.anio === record.anio), (d) => d.pasajeros)?.operador ?? ""}</p></div>
</div>` : html`<p class="leyenda">Todavía no hay datos del tren cargados.</p>`
```

### Año por año

```js
const OPS = ["Ferrobaires (provincia)", "Trenes Argentinos (SOFSE)"];
const mesesAnio = new Map(conDatos.map((d) => [d.anio, d.meses]));
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  marginBottom: 45,
  y: {grid: true, label: "Pasajeros pagos por año", tickFormat: compacto},
  x: ejeAnios,
  color: {legend: true, domain: OPS, range: [TINTA_2, ACENTO]},
  marks: [
    Plot.barY(porOperador, {x: "anio", y: "pasajeros", fill: "operador", order: OPS, fillOpacity: (d) => (mesesAnio.get(d.anio) === 12 ? 1 : 0.45), inset: 1.5, tip: true,
      title: (d) => `${d.anio} · ${d.operador}\n${entero(d.pasajeros)} pasajeros en ${d.meses} meses${mesesAnio.get(d.anio) === 12 ? "" : `\nAño con ${mesesAnio.get(d.anio)} meses de servicio informado`}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Barras claras: años con menos de 12 meses de servicio informado (suspensiones o año en curso).${ambos.length ? ` En ${ambos.join(", ").replace(/, (\d+)$/, " y $1")} hay pasajeros de los dos operadores.` : ""}</p>

### Mes por mes

```js
// Meses sin dato como hueco (null), no como línea que une los extremos.
const porMes = new Map(mensual.map((d) => [+d.periodo, d]));
const serieMes = d3.utcMonth.range(mensual[0].periodo, d3.utcMonth.offset(mensual.at(-1).periodo, 1))
  .map((p) => porMes.get(+p) ?? {periodo: p, anio: p.getUTCFullYear(), mes: p.getUTCMonth() + 1, pasajeros: null});
display(Plot.plot({
  width,
  height: ALTO.medio,
  marginLeft: 55,
  y: {grid: true, label: "Pasajeros pagos por mes", tickFormat: compacto},
  x: {label: null, type: "utc"},
  marks: [
    Plot.areaY(serieMes, {x: "periodo", y: "pasajeros", fill: ACENTO, fillOpacity: 0.1, curve: "step-after"}),
    Plot.lineY(serieMes, {x: "periodo", y: "pasajeros", stroke: ACENTO, strokeWidth: 1.25, curve: "step-after"}),
    Plot.dot(mensual, {x: "periodo", y: "pasajeros", r: 0, tip: true,
      title: (d) => `${MESES[d.mes - 1]} ${d.anio}\n${entero(d.pasajeros)} pasajeros\n${opNombre(d.operadores)}`}),
    Plot.ruleY([0])
  ]
}));
```

<p class="leyenda">Los picos son enero y febrero. Los huecos son meses sin servicio informado.</p>

### Entre los trenes de larga distancia

```js
const rank = servicios.filter((d) => d.anio === ref?.anio).slice(0, 10);
display(Plot.plot({
  width,
  height: 34 * rank.length + 40,
  marginLeft: 330,
  x: {grid: true, label: `Pasajeros pagos en ${ref?.anio}`, tickFormat: compacto},
  y: {label: null, domain: rank.map((d) => d.servicio)},
  marks: [
    Plot.barX(rank, {x: "pasajeros", y: "servicio", fill: (d) => (d.es_foco ? ACENTO : TINTA), inset: 2, tip: true,
      title: (d) => `${d.servicio}\n${entero(d.pasajeros)} pasajeros · ${d.operador}`}),
    Plot.ruleX([0])
  ]
}));
```

<div class="leyenda-grid">
  <p><b>Qué se cuenta.</b> Pasajeros pagos (los que abonaron pasaje, según el manual de indicadores de la CNRT) del servicio entero: los dos sentidos y también quienes viajan entre estaciones intermedias o, en los años de Ferrobaires, hasta Miramar.</p>
  <p><b>Quién lo operó.</b> Ferrobaires (provincia de Buenos Aires): datos en ${rangoTxt(ferro)}. Trenes Argentinos (SOFSE): ${rangoTxt(sofse)}; empezó en julio de 2011 con trenes Talgo, servicio que se suspendió en octubre de 2012 (hoja "Cambios en los Servicios" de la planilla de la CNRT).</p>
  <p><b>De dónde sale.</b> Planilla de pasajeros de larga distancia, regionales y turísticos de la CNRT, actualizada mensualmente. Detalle y validación en <a href="/metodologia">Metodología</a>.</p>
</div>
