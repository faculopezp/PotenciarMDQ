import * as d3 from "d3";

// Paleta de referencia (skill dataviz): categórica en orden fijo, secuencial azul, divergente azul↔rojo.
export const CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"];
export const OTRO = "#a3a29c";
export const SEQ = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"];
export const DIV = {neg: "#e34948", mid: "#f0efec", pos: "#2a78d6"};
export const FOCO = CAT[0];

// Formatos en castellano (separador de miles con punto).
const es = d3.formatLocale({decimal: ",", thousands: ".", grouping: [3], currency: ["$", ""]});
export const entero = es.format(",.0f");
export const pct = es.format(".0%");
export const pct1 = es.format(".1%");
export const variacion = es.format("+.1%");
export const decimal1 = es.format(",.1f");

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

// Lee un JSON de FileAttachment y convierte las columnas de fecha ("YYYY-MM-DD") a Date (UTC).
const FECHAS = ["fecha", "periodo"];
export async function datos(file) {
  const rows = await file.json();
  for (const r of rows) for (const k of FECHAS) if (typeof r[k] === "string") r[k] = new Date(`${r[k]}T00:00:00Z`);
  return rows;
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

// JSON columnar {col: [valores]} -> lista de objetos.
export async function columnas(file) {
  const c = await file.json();
  const keys = Object.keys(c);
  return c[keys[0]].map((_, i) => Object.fromEntries(keys.map((k) => [k, c[k][i]])));
}
