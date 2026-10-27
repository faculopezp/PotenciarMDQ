---
title: Metodología y fuentes
---

# Metodología y fuentes

<div class="metodologia">

## De dónde salen los datos

| Dato | Fuente | Cobertura |
|---|---|---|
| Cada aterrizaje y despegue (fecha, hora, aerolínea, avión, origen/destino, pasajeros) | ANAC — "Aterrizajes y despegues procesados por la ANAC", Portal de Datos Abiertos de Transporte | 2019 → hoy, se actualiza mensualmente |
| Pasajeros y movimientos mensuales del aeropuerto, por ruta | Municipio de General Pueyrredon — datos.mardelplata.gob.ar | 2001–2020 (se usa hasta 2018) |
| Vuelos individuales (muestra, sin pasajeros) | Municipio de General Pueyrredon | 2015–2018 (≈ 52 % de los movimientos) |
| Turistas arribados, estadía, fines de semana largos | EMTURyC vía datos.mardelplata.gob.ar | 2007–2025 |
| Clima diario en el aeropuerto | Open-Meteo (reanálisis ERA5) | 2019 → hoy |
| Coordenadas y nombres de aeropuertos | OurAirports (dominio público) | — |
| Feriados nacionales | Calendario oficial (paquete `holidays`) | — |
| Hitos históricos | Notas de prensa y fuentes secundarias, marcadas como tales | — |
| Avión de 2019 | Versión anterior del mismo dataset de la ANAC (exportada en 2025), que todavía traía el avión | 2019 |
| Asientos y vuelos por día y ruta | Yvera, Ministerio de Turismo — "Conectividad aérea", base agregada de frecuencias (fuente SIAC/ANAC) | 2017 → hoy |
| Empresa que explota cada matrícula | ANAC — consulta pública "Afectación de Aeronaves" (extracción manual, se repite cada 1–2 meses) | vigente a la fecha de extracción |
| Empresas certificadas | ANAC — listados de transporte aerocomercial (Partes 121/135) y trabajo aéreo (CETA) | 2024 |
| Tipo de avión por matrícula | tar1090-db, base comunitaria de transpondedores (Mictronics / wiedehopf) | actual |
| Cabinas por aerolínea y modelo | Comunicados y prensa especializada, con fuente por fila (`config/cabinas.yaml`) | — |
| Aeronaves del Estado | Formato de identificación de cada fuerza e identificaciones públicas por serie (`config/estatales.yaml`) | — |
| Micros de media y larga distancia: pasajeros, asientos y viajes por ruta y año; cada servicio de turismo con fecha | CNRT vía Yvera, Ministerio de Turismo — "Conectividad terrestre interurbana" | 2019 → 2024 (Yvera no actualiza desde diciembre de 2024) |
| Tren: pasajeros pagos por mes y servicio | CNRT — planilla de pasajeros de larga distancia, regionales y turísticos | 2008 → hoy, mensual |
| Turistas por medio de transporte (auto, ómnibus, tren, avión) y por región de procedencia | EMTUR vía datos.mardelplata.gob.ar ("Arribo de turistas por medio de transporte", "Procedencia de turistas") | 2013–2025 y 2007–2024, mensual |
| Medio de transporte y región de origen de los turistas residentes | Yvera, Ministerio de Turismo — Encuesta de Viajes y Turismo de los Hogares (EVyTH), microdatos | 2012 → 2024 (trimestral) |
| Tránsito de autos hacia la costa | AUBASA, cifras comunicadas a la prensa con período exacto (`config/autos.yaml`) | puntual |
| Recaladas de cruceros y paradas por emergencia en rada | Notas de prensa, con fuente por fila (`config/cruceros.yaml`), revisadas con una investigación dedicada: no hay datos abiertos del puerto | 2014 → hoy |

Los datos se descargan y procesan automáticamente una vez por mes. El código es abierto.

<div class="met-grid">
<div>

## Cómo se cuenta

- **Movimiento:** un aterrizaje o un despegue en Mar del Plata. Un vuelo de ida y vuelta son dos movimientos acá.
- **Pasajeros:** los que bajan más los que suben en Mar del Plata (estándar internacional de aeropuertos). No hay doble conteo.
- **Segmentos:** cada movimiento se clasifica según la clase de vuelo que informa la ANAC: *línea regular*; *charter de línea* (no regular con avión u operador de línea); *taxi aéreo* (el resto de los no regulares: jets y turbohélices ejecutivos, avionetas, helicópteros); *privado*; *oficial y militar*; *escuelas de vuelo*; *trabajo aéreo*. Ningún movimiento queda sin segmento.
- **Lugares aptos denunciados (LAD):** los orígenes/destinos con código numérico son superficies aptas registradas por denuncia ante la ANAC, que no son aeródromos (art. 25 del Código Aeronáutico). No tienen coordenadas públicas: no aparecen en el mapa ni se cuentan como vuelos al exterior, aunque la ANAC los clasifique como internacionales.
- **Modelo de avión:** las denominaciones de la ANAC se estandarizan a un modelo con designador ICAO (ej. `BO-737-800`, `BO-B737-800` y `BO-737-8SH` son el Boeing 737-800). Validado contra OpenSky por matrícula (95 % de coincidencia).
- **Operadores:** variantes del mismo nombre (`LADE` / `L.A.D.E.`, `S.A.` / `SA`) se unifican.
- **Taxi aéreo a pistón:** cuenta como taxi solo con 6 plazas o más (piloto + 5 pasajeros); si no, se analiza como privado.
- **Privado en jet o turbohélice ejecutivo:** se analiza como taxi aéreo. En MDQ, casi todos los que traen operador o matrícula son de empresas o aviones que también vuelan como taxi: son tramos de posicionamiento declarados como privados.
- **Modelo de avión faltante:** la ANAC no informa el modelo en 2019 y en parte de 2020, y en ~20 % de los movimientos posteriores (sobre todo vuelos oficiales y militares). Primero se recupera con cruces exactos: en 2019, el avión sale de una versión anterior del mismo dataset de la ANAC, que sí lo traía (mismo día, hora UTC, movimiento y origen/destino, coincidencia 1 a 1; los pasajeros no sirven de clave porque la ANAC los corrigió entre versiones; en 2023–2024 esas claves dan el mismo avión en 11.015 de 11.016 vuelos), y si no, del registro municipal del mismo vuelo. Lo que queda, en vuelos de Aerolíneas, se infiere por pasajeros: hasta 96 → E190 (acierta 93–98 %), más de 128 → 737-800/MAX 8 (95 %); entre 97 y 128 no se asigna (30 % eran E190). Avian 2019 → ATR 72-600; Flyest → CRJ200. En 2020, además, el avión sale de los asientos del vuelo exacto según Yvera: para cada aerolínea, la cantidad de asientos que en los años con dato corresponde siempre al mismo avión (96 → E190 en 2.187 de 2.187 vuelos); si ese día hubo varios vuelos, solo cuando la única combinación posible es que todos sean el mismo avión. En 2026, tar1090-db completa el tipo por matrícula (misma familia que la ANAC en prácticamente todos los casos comparables). Lo inferido se marca como tal.
- **Operador recuperado:** si un vuelo no trae operador, se toma de la consulta de Afectación de la ANAC (matrícula → empresa, desde la fecha de afectación; coincide con el operador informado en el 99,9 % de los casos), de otros vuelos del mismo avión (matrícula, desde 2026) cuando todos coinciden, o del registro del otro extremo del mismo vuelo (aeropuertos cruzados, horario compatible y un solo candidato; coincide en el 99 % de los vuelos que traen el dato). En aeronaves del Estado, la identificación dice la fuerza (T-, TC- Fuerza Aérea; AE- Ejército; 2-H- Armada; PA- Prefectura; GN- Gendarmería; PF- Policía Federal) y, cuando hay identificación pública, el modelo (ej. T-99 Boeing 737-700, PA-40 Dauphin). Auditoría completa en `reports/qa/auditoria.md`.
- **Serie larga:** hasta 2018 se usan los datos municipales y desde 2019 los de la ANAC. En 2019, año que cubren ambas fuentes, difieren menos de 4 % por mes. Desde 2021 el Municipio publica pasajeros de un solo sentido, por eso no se usa.
- **Datos provisorios:** la ANAC marca como provisorios los últimos meses; pueden cambiar.
- **Hora local:** hora UTC − 3.
- **Micros:** servicios de jurisdicción nacional (CNRT) con Mar del Plata en un extremo del par origen–destino. *Regular*: líneas con horario y boleto; *turismo*: servicios contratados (DUT). Los pasajeros salen de las bases con cada viaje; en los años que esas bases no cubren, del archivo de rutas con al menos un viaje semanal (un piso). En turismo, ambas coinciden ruta por ruta donde se pueden comparar. Los nombres de localidad se unifican (con y sin tildes, "CABA" = Ciudad Autónoma de Buenos Aires). En algunas rutas largas la fuente registra más pasajeros que asientos: no se publica la ocupación por ruta. Validación en `reports/qa/omnibus.md`.
- **Tren:** pasajeros pagos de los servicios que llegan a Mar del Plata (Constitución–Mar del Plata, con o sin extensión a Miramar), en los dos sentidos y con estaciones intermedias. Para comparar con las llegadas se toma la mitad.
- **Reparto por medio (EMTUR):** la suma de las cuatro vías es el total de turistas del mes. Avión coincide con los pasajeros que aterrizan según ANAC (diferencia menor al 2 % por año) y tren con la mitad de los pasajeros de la CNRT (hasta 11 %); el auto es la parte estimada. Comparación año por año en "Cómo llega la gente" y en `reports/qa/omnibus.md`.
- **Procedencia:** % mensual por región de residencia; las cantidades son ese % por el total de turistas del mes. Los nombres de las regiones cambian entre planillas y se unifican (CABA, Conurbano, Resto de la provincia, Resto del país, Exterior).
- **Reparto por medio (EVyTH):** viajes de residentes en los grandes aglomerados urbanos con destino Mar del Plata, expandidos con el factor de la encuesta; solo turistas (al menos una noche). Tren y avión salen de pocas decenas de casos por año: el visor muestra la cantidad de encuestados de cada barra.
- **Cómo llega la gente:** turistas del EMTUR (un modelo municipal, todas las vías) contra los pasajeros que llegaron en avión (aterrizajes de línea), micro y crucero. Los pasajeros incluyen a residentes que vuelven y el auto no se mide: la relación es una aproximación, no un reparto exacto.


</div>
<div>

## Notas por capítulo

- **01 · Serie larga:** las barras claras (2001–2018) son datos del Municipio y las oscuras (2019+), de la ANAC. Movimientos comerciales = vuelos regulares y no regulares.
- **04 · Todo lo que vuela, "Desde 2015":** 2015–2018 sale de una muestra municipal de vuelos (≈ 52 % de los movimientos, sin vuelos oficiales ni escuelas); por eso la composición se muestra en porcentaje.
- **04 · Avión típico:** familia con más movimientos de cada segmento. "Lleva hasta (habitual)" = percentil 95 de pasajeros de esa familia en ese segmento en todo el país. El **avión básico** del taxi aéreo es el turbohélice más frecuente entre los que llevan 5 o más pasajeros.
- **05 · Asientos:** la ANAC no publica asientos. Primero, los asientos del vuelo exacto según Yvera (cuando ese día hubo un solo vuelo en la ruta y coinciden los pasajeros); si no, la configuración de cabina publicada de cada aerolínea y modelo (E190 de Aerolíneas 96, 737-800 de Flybondi 189, 737 MAX 8 170, ATR 72 de Avian 72…); donde las fuentes no coinciden, la capacidad típica observada (p95 de pasajeros). Ambas dan lo mismo donde se pueden comparar.
- **06 · A dónde se vuela:** el mapa recorta el cono sur; los destinos fuera del recorte se dibujan como flechas hacia el borde y se detallan en "Destinos lejanos". Ubicación de cada código: lista oficial de aeródromos y helipuertos de la ANAC, OurAirports y MADHEL. Los vuelos a lugares aptos denunciados no se cuentan como exterior.
- **08 · Flota:** en 2019–2020 el avión se infiere por operador y pasajeros (ver "Modelo de avión faltante"); el resto queda como "Sin dato".
- **Toda la aviación · Operadores:** "Sin dato" = la ANAC no informa el operador (frecuente en vuelos oficiales y militares).
- **Explorador:** la familia de avión incluye la inferida para 2019–2020; los movimientos sin avión informado se cuentan aparte.


</div>
</div>

## Métricas estimadas (leer con cuidado)

| Métrica | Cómo se calcula | Por qué es una estimación |
|---|---|---|
| Asientos ofrecidos | Asientos del vuelo exacto según Yvera; si no, cabina publicada por aerolínea y modelo (`config/cabinas.yaml`); si no hay, percentil 95 de los pasajeros observados en ese modelo (y aerolínea) en todo el país | ANAC no publica asientos |
| Ocupación (load factor) | Pasajeros ÷ asientos estimados | Hereda la estimación de asientos; tiende a sobrestimar unos puntos |
| Duración de vuelo | Se une el despegue en el origen con el aterrizaje en destino del mismo avión | ANAC no publica número de vuelo; se empareja por aerolínea y modelo (y matrícula desde 2026) |
| Tiempo en tierra (turnaround) | Aterrizaje → siguiente despegue del mismo avión en MDQ | Igual que arriba; validado contra matrícula en 2026 (medianas 51 vs 52 min) |
| Hora pico de diseño | 30.ª hora con más pasajeros del año (Standard Busy Rate) | — |
| Concentración (HHI) | Suma de las cuotas de mercado al cuadrado × 10.000 | — |
| Tendencia | Descomposición estacional STL (período 12) de los pasajeros mensuales | Suaviza; los extremos se revisan con cada dato nuevo |
| Días atípicos | Desvío respecto de la mediana del mismo día de la semana ±3 semanas, en desvíos robustos (MAD); atípico si supera 3 | Los paros se rotulan solo con fuente de prensa |
| Pronóstico | Holt-Winters (log, tendencia amortiguada, estacionalidad anual) sobre la serie pospandemia; banda = 80 % de 2.000 simulaciones | No anticipa rutas nuevas ni cambios de aerolíneas |
| Peso en la red | PageRank de la red de vuelos de cabotaje reconstruidos | — |
| Avión típico | Familia con más movimientos por segmento; "capacidad observada" = p95 de pasajeros de ese modelo en ese segmento en todo el país | En aviación general es pasajeros llevados, no asientos |

## Disponibilidad de datos

Qué hay, qué falta y quién lo tiene. "Pedido de acceso" = solicitud de acceso a la información pública (Ley 27.275 para organismos nacionales; en la Provincia y el Municipio, sus propios regímenes de acceso).

| Vía | Lo que tenemos | Lo que falta | Quién lo tiene / debería publicarlo |
|---|---|---|---|
| **Avión** | Cada aterrizaje y despegue desde 2019 (ANAC); asientos por vuelo (Yvera); serie municipal 2001–2020 | Operador y avión de vuelos privados, escuelas y oficiales 2019–2025 (sin matrícula); horarios programados (puntualidad, cancelaciones); tarifas | ANAC (matrícula histórica, pedido de acceso); Aeropuertos Argentina (horarios programados); las aerolíneas (tarifas) |
| **Ómnibus** | Cada viaje de larga distancia con pasajeros y asientos, regular y turismo, 2019–nov 2024 (CNRT vía Yvera) | Datos desde diciembre de 2024 (Yvera dejó de actualizar); servicios provinciales (no son de la CNRT); pasajeros reales por tramo (hay rutas con más pasajeros que asientos) | Ministerio de Turismo / CNRT (actualizar el conjunto); Provincia de Buenos Aires (servicios provinciales); Terminal de Ómnibus de Mar del Plata (arribos por andén) |
| **Tren** | Pasajeros pagos por mes y servicio desde 2008 (CNRT) | Subidas y bajadas por estación y por sentido (hoy es el servicio entero, ida y vuelta) | Trenes Argentinos (SOFSE) / CNRT |
| **Auto** | Estimación mensual del EMTUR desde 2013; cifras de AUBASA comunicadas a la prensa; tránsito medio diario anual de la Ruta 226 (Vialidad Nacional) | Conteos por cabina de peaje, día y sentido en las rutas 2 y 11; el método con que el EMTUR estima el auto | AUBASA y Ministerio de Infraestructura de la Provincia (conteos, pedido de acceso); EMTUR (método) |
| **Cruceros** | Registro armado con notas de prensa, con fuente por fila | Cualquier serie oficial: la de cruceros de Yvera/Migraciones cubre solo Buenos Aires, Puerto Madryn y Ushuaia | Dirección Nacional de Migraciones (entradas por el puerto de Mar del Plata, pedido de acceso); Consorcio Portuario Regional de Mar del Plata (recaladas y pasajeros) |
| **Turistas** | Total mensual, reparto por vía (desde 2013) y procedencia por región (desde 2007) del EMTUR; encuesta de hogares EVyTH (Ministerio de Turismo) | Abril–noviembre de 2020; procedencia de algunos meses (2014, 2019–2021); la base de cálculo detrás de cada cifra | EMTUR (Municipio de General Pueyrredon) |

<div class="met-grid">
<div>

## Qué tan completo es cada dato

Parte de los movimientos de cada año con el dato disponible, ya sea informado por la ANAC, recuperado con cruces exactos o deducido (Mar del Plata). Al pie de cada gráfico se indica la cobertura que le corresponde.

```js
const cob = datos(FileAttachment("data/mdq_cobertura.json"));
```

```js
html`<table class="editorial"><thead><tr><th>Año</th><th>Movimientos</th><th>Operador (ANAC)</th><th>Operador (con recuperación)</th><th>Avión de línea</th><th>Avión fuera de línea</th><th>Asientos de línea</th></tr></thead><tbody>
${cob.filter((d) => d.alcance === "todos").map((t) => {
  const l = cob.find((d) => d.anio === t.anio && d.alcance === "linea") ?? {};
  const r = cob.find((d) => d.anio === t.anio && d.alcance === "resto") ?? {};
  return html`<tr><td>${t.anio}</td><td>${entero(t.movimientos)}</td><td>${pct(t.pct_operador_anac)}</td><td>${pct(t.pct_operador)}</td><td>${pct(l.pct_aeronave_con_inferida ?? 0)}</td><td>${pct(r.pct_aeronave_con_inferida ?? 0)}</td><td>${pct(l.pct_asientos ?? 0)}</td></tr>`;
})}
</tbody></table>`
```

## Lo que no se puede medir con estos datos

- Puntualidad y cancelaciones (no hay horarios programados).
- Operador y avión de privados, escuelas y vuelos oficiales 2019–2025: la ANAC publica la matrícula recién desde 2026 y sin matrícula no hay cruce posible.
- Tarifas.
- Origen de los pasajeros aéreos (el dataset de la ANAC no trae nacionalidad ni residencia; la procedencia del EMTUR es de todos los turistas, no por vía).


## Colores

Cada color significa siempre lo mismo en todo el sitio.

```js
const muestras = [
  ["Bermellón", ACENTO, "lo que se destaca: Mar del Plata, récords, el exterior"],
  ["Tinta", TINTA, "datos principales"],
  ["Gris", OTRO, "otras / resto agrupado"],
  ["Gris claro", SIN_DATO, "dato faltante"],
  ...SEGMENTOS.map((x) => [x.nombre, SEG_COLOR[x.id], "segmento"]),
  ...PERFILES.filter((x) => x.id !== "sin_dato").map((x) => [x.nombre, x.color, "tipo de aeronave"])
];
```

```js
html`<div class="paleta">${muestras.map(([n, c, uso]) => html`<div><span class="muestra" style="background:${c}"></span><span><b>${n}</b><br><span class="muted">${uso}</span></span></div>`)}</div>`
```

</div>
<div>

## Descargar los datos

```js
const archivos = [
  ["Serie anual", FileAttachment("data/mdq_anual.json")],
  ["Serie mensual", FileAttachment("data/mdq_mensual.json")],
  ["Serie diaria", FileAttachment("data/mdq_diario.json")],
  ["Rutas", FileAttachment("data/mdq_rutas.json")],
  ["Aerolíneas", FileAttachment("data/mdq_aerolineas.json")],
  ["Aeropuertos pares", FileAttachment("data/benchmark_pares.json")],
  ["Orígenes y destinos (toda la aviación)", FileAttachment("data/mdq_destinos.json")],
  ["Vuelos a destinos lejanos", FileAttachment("data/mdq_vuelos_exoticos.json")],
  ["Flota por modelo", FileAttachment("data/mdq_aeronaves.json")],
  ["Segmentos por año", FileAttachment("data/mdq_segmentos_anual.json")],
  ["Cobertura de cada dato", FileAttachment("data/mdq_cobertura.json")],
  ["Micros por año", FileAttachment("data/bus_anual.json")],
  ["Micros por ruta y año", FileAttachment("data/bus_rutas.json")],
  ["Micros de turismo por mes", FileAttachment("data/bus_mensual.json")],
  ["Tren por mes", FileAttachment("data/tren_mensual.json")],
  ["Tren por año", FileAttachment("data/tren_anual.json")],
  ["Turistas por medio de transporte (EMTUR)", FileAttachment("data/mdq_arribos_medio.json")],
  ["Turistas por procedencia (EMTUR)", FileAttachment("data/mdq_procedencia.json")],
  ["Turistas por medio de transporte (EVyTH)", FileAttachment("data/evyth_medio.json")],
  ["Turistas por región de origen (EVyTH)", FileAttachment("data/evyth_origen.json")],
  ["Cruceros", FileAttachment("data/cruceros.json")]
];
```

```js
html`<ul>${archivos.map(([n, f]) => html`<li><a href=${f.href} download=${f.name}>${n}</a> (JSON)</li>`)}</ul>`
```


</div>
</div>

</div>

```js
import {html} from "htl";
import {ACENTO, TINTA, OTRO, SIN_DATO, SEGMENTOS, SEG_COLOR, PERFILES, datos, entero, pct} from "./components/util.js";
```
