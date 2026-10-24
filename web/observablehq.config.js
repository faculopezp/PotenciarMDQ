// Navegación en una barra superior (sin barra lateral ni índice derecho): en escritorio el
// contenido usa todo el ancho. El índice de capítulos vive en la portada de cada página.
const paginas = [
  {name: "La historia", path: "/"},
  {name: "Toda la aviación", path: "/aviacion-general"},
  {name: "Explorador", path: "/explorador"},
  {name: "Metodología y fuentes", path: "/metodologia"}
];

export default {
  title: "PotenciarMDQ",
  root: "src",
  lang: "es",
  style: "style.css",
  pages: paginas,
  header: ({path}) => `<nav class="barra">
  <a class="marca" href="./">PotenciarMDQ</a>
  ${paginas.map((p) => `<a href=".${p.path === "/" ? "/" : p.path}"${(path === p.path || (p.path === "/" && path === "/index")) ? ' class="activa"' : ""}>${p.name}</a>`).join("")}
</nav>`,
  footer: "Datos: ANAC · Municipio de General Pueyrredon · Open-Meteo · OurAirports · OpenSky. Código: github.com/faculopezp/PotenciarMDQ",
  toc: false,
  pager: false,
  sidebar: false
};
