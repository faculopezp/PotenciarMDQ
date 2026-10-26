// Navegación en una barra superior (sin barra lateral ni índice derecho): en escritorio el
// contenido usa todo el ancho. Barra principal = un modo de transporte por entrada; los modos con
// varias páginas (aviación) suman una segunda barra. Rutas absolutas: las páginas viven en
// subcarpetas (/aviacion/...).
const modos = [
  {name: "Inicio", path: "/"},
  {name: "Cómo llega la gente", path: "/llegadas"},
  {name: "Aviación", path: "/aviacion/", paginas: [
    {name: "La historia", path: "/aviacion/"},
    {name: "Toda la aviación", path: "/aviacion/toda-la-aviacion"},
    {name: "Explorador", path: "/aviacion/explorador"}
  ]},
  {name: "Ómnibus", path: "/omnibus"},
  {name: "Tren", path: "/tren"},
  {name: "Autos", path: "/autos"},
  {name: "Cruceros", path: "/cruceros"},
  {name: "Metodología", path: "/metodologia"}
];

// Observable informa el path sin barra final y con /index para las portadas.
const normal = (p) => p.replace(/\/index$/, "/").replace(/^$/, "/");
const activo = (path, m) => {
  const p = normal(path);
  return m.path === "/" ? p === "/" : p === m.path || p.startsWith(m.path.replace(/\/$/, "") + "/");
};

export default {
  title: "PotenciarMDQ",
  root: "src",
  lang: "es",
  style: "style.css",
  pages: modos.flatMap((m) => m.paginas ?? [{name: m.name, path: m.path}]),
  header: ({path}) => {
    const modo = modos.find((m) => m.paginas && activo(path, m));
    return `<nav class="barra">
  <a class="marca" href="/">PotenciarMDQ</a>
  ${modos.map((m) => `<a href="${m.path}"${activo(path, m) ? ' class="activa"' : ""}>${m.name}</a>`).join("")}
</nav>${modo ? `
<nav class="barra sub">${modo.paginas.map((p) => `<a href="${p.path}"${normal(path) === p.path ? ' class="activa"' : ""}>${p.name}</a>`).join("")}</nav>` : ""}`;
  },
  footer: "Datos: ANAC · CNRT · Yvera (Ministerio de Turismo) · Municipio de General Pueyrredon / EMTUR · Open-Meteo · OurAirports. Código: github.com/faculopezp/PotenciarMDQ",
  toc: false,
  pager: false,
  sidebar: false
};
