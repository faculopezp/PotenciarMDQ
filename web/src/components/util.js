import * as d3 from "d3";

// ── Paleta del sitio (ver docs/11_paleta.md). Cada color tiene un único significado. ──
// Base editorial: papel, tinta y un acento bermellón reservado para lo que se destaca
// (Mar del Plata en comparaciones, récords, alertas, el exterior en el mapa).
export const PAPEL = "#f5f1ea";
export const TINTA = "#1a1a18";
export const TINTA_2 = "#6b675e";
export const ACENTO = "#c73e1d";
export const OTRO = "#a3a29c";        // "otras" / resto agrupado
export const SIN_DATO = "#d6d3cb";    // dato faltante: siempre el gris más claro
// Categórica (validada por contraste y daltonismo), en orden fijo: la usan los segmentos.
export const CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"];
// Secuencial (intensidad: calendarios, mapas de calor) y divergente (más/menos).
export const SEQ = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"];
export const DIV = {neg: "#c73e1d", mid: "#efeae1", pos: "#2a78d6"};
export const FOCO = TINTA;

// Segmentos de actividad: orden y color fijos (el color sigue al segmento, nunca al ranking).
export const SEGMENTOS = [
  {id: "linea_regular", nombre: "Línea regular"},
  {id: "taxi_aereo", nombre: "Taxi aéreo"},
  {id: "privado", nombre: "Privado"},
  {id: "instruccion", nombre: "Escuelas de vuelo"},
  {id: "oficial", nombre: "Oficial y militar"},
  {id: "charter_linea", nombre: "Charter de línea"},
  {id: "trabajo_aereo", nombre: "Trabajo aéreo"}
];
// Perfil de aeronave, de más pesado a más liviano: turbina en azules, pistón en ámbar,
// helicóptero en verde, avión de línea en gris tinta.
export const PERFILES = [
  {id: "jet_ejecutivo", nombre: "Jet ejecutivo", color: "#0d366b"},
  {id: "turbohelice", nombre: "Turbohélice", color: "#3987e5"},
  {id: "piston_6", nombre: "Pistón 6+ plazas", color: "#c98500"},
  {id: "piston_liviano", nombre: "Pistón liviano", color: "#f2c55c"},
  {id: "helicoptero", nombre: "Helicóptero", color: "#1baf7a"},
  {id: "avion_de_linea", nombre: "Avión de línea", color: "#6b675e"},
  {id: "sin_dato", nombre: "Sin dato", color: "#d6d3cb"}
];
// Para tablas por familia (sin plazas): pistón a secas.
export const PERFIL_EXTRA = {piston: {nombre: "Pistón", color: "#eda100"}};
export const PERFIL_NOMBRE = {...Object.fromEntries(PERFILES.map((p) => [p.id, p.nombre])), piston: "Pistón"};
// Color por categoría de aeronave (para gráficos sin perfil calculado, ej. Explorador).
export const CATEGORIA_COLOR = {
  jet_ejecutivo: "#0d366b", turbohelice_ejecutivo: "#3987e5", aviacion_general_piston: "#eda100",
  helicoptero: "#1baf7a", agricola: "#008300", jet_fuselaje_angosto: TINTA_2, jet_fuselaje_ancho: TINTA_2,
  jet_regional: TINTA_2, turbohelice_regional: TINTA_2, transporte_militar: TINTA, otro: OTRO, sin_dato: SIN_DATO
};
export const perfilColor = {domain: PERFILES.map((p) => p.nombre), range: PERFILES.map((p) => p.color)};
export const SEG_NOMBRE = Object.fromEntries(SEGMENTOS.map((s) => [s.id, s.nombre]));
export const SEG_COLOR = Object.fromEntries(SEGMENTOS.map((s, i) => [s.id, CAT[i]]));
export const segColor = {domain: SEGMENTOS.map((s) => s.nombre), range: SEGMENTOS.map((s) => SEG_COLOR[s.id])};

// Formatos en castellano.
const es = d3.formatLocale({decimal: ",", thousands: ".", grouping: [3], currency: ["$", ""]});
export const entero = es.format(",.0f");
export const pct = es.format(".0%");
export const pct1 = es.format(".1%");
export const variacion = es.format("+.1%");
export const decimal1 = es.format(",.1f");
export const compacto = (x) => (Math.abs(x) >= 1e6 ? `${decimal1(x / 1e6)} M` : Math.abs(x) >= 1e3 ? `${entero(x / 1e3)} mil` : entero(x));

export const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
export const DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"];

export const CATEGORIAS = {
  jet_fuselaje_angosto: "Jet de fuselaje angosto (737, A320)",
  jet_fuselaje_ancho: "Jet de fuselaje ancho",
  jet_regional: "Jet regional (E190)",
  turbohelice_regional: "Turbohélice regional",
  jet_ejecutivo: "Jet ejecutivo",
  turbohelice_ejecutivo: "Turbohélice ejecutivo",
  aviacion_general_piston: "Avioneta a pistón",
  helicoptero: "Helicóptero",
  agricola: "Agrícola",
  transporte_militar: "Transporte militar",
  otro: "Otro",
  sin_dato: "Sin dato"
};

export const CLASES = {
  regular: "Regular",
  no_regular: "No regular (charter / taxi aéreo)",
  vuelo_privado_con_matricula_nacional: "Privado",
  vuelo_privado_con_matricula_extranjera: "Privado",
  vuelo_oficial_nacional: "Oficial",
  vuelo_oficial_extranjero: "Oficial",
  vuelo_escuela: "Escuela de vuelo",
  trabajo_aereo: "Otros",
  vuelo_de_adiestramiento: "Otros"
};

// JSON de FileAttachment con columnas de fecha ("YYYY-MM-DD") convertidas a Date (UTC).
const FECHAS = ["fecha", "periodo"];
export async function datos(file) {
  const rows = await file.json();
  for (const r of rows) for (const k of FECHAS) if (typeof r[k] === "string") r[k] = new Date(`${r[k]}T00:00:00Z`);
  return rows;
}

// JSON columnar {col: [valores]} -> lista de objetos.
export async function columnas(file) {
  const c = await file.json();
  const keys = Object.keys(c);
  return c[keys[0]].map((_, i) => Object.fromEntries(keys.map((k) => [k, c[k][i]])));
}

// Último año completo (12 meses y sin datos provisorios); si no hay, el último disponible.
export function ultimoAnioCompleto(anual) {
  const completos = anual.filter((d) => d.meses_con_datos === 12 && !d.tiene_provisorio);
  return (completos.length ? completos : anual).at(-1);
}

// Temporadas de verano completas (dic del año anterior + ene + feb presentes en la serie mensual).
export function veranosCompletos(mensual) {
  const hay = new Set(mensual.map((d) => `${d.anio}-${d.mes}`));
  const anios = [...new Set(mensual.map((d) => d.anio))];
  return anios.filter((y) => hay.has(`${y - 1}-12`) && hay.has(`${y}-1`) && hay.has(`${y}-2`));
}

// Deja las `n` categorías más grandes y agrupa el resto en "Otras" (máx. 8 colores).
export function topN(rows, key, value, n = 6, otras = "Otras") {
  const tot = d3.rollup(rows, (v) => d3.sum(v, (d) => d[value]), (d) => d[key]);
  const top = new Set([...tot].sort((a, b) => b[1] - a[1]).slice(0, n).map(([k]) => k));
  return {top: [...top], label: (d) => (top.has(d[key]) ? d[key] : otras)};
}

export const fechaLarga = (d) => d.toLocaleDateString("es-AR", {day: "numeric", month: "long", year: "numeric", timeZone: "UTC"});

// Tamaños estándar: series anchas (todo el ancho) y gráficos de media columna.
export const ALTO = {serie: 380, medio: 300};
// Eje de años en barras: rotado 45° para que no se encimen.
export const ejeAnios = {label: null, tickFormat: "d", tickRotate: -45};
// Ejes de fecha en castellano: "ene / 2024" en enero, el mes abreviado el resto del año.
export const fechaEje = (d) => (d.getUTCMonth() === 0 ? `${MESES[0]}\n${d.getUTCFullYear()}` : MESES[d.getUTCMonth()]);

// "Cessna 150 · Cessna 182" bajo la familia "Cessna" -> "150 · 182": saca el fabricante repetido.
export function modelosCortos(modelos, familia) {
  if (!modelos) return "—";
  const marca = familia.split(" ")[0];
  return modelos.split(" · ").map((m) => {
    const [primera, ...resto] = m.split(" ");
    return resto.length && primera.startsWith(marca) ? resto.join(" ") : m;
  }).join(" · ");
}
