# Paleta y reglas visuales

Definida en `web/src/components/util.js` (colores de datos) y `web/src/style.css` (tokens CSS).
Regla: **cada color tiene un único significado en todo el sitio**.

| Rol | Color | Uso |
|---|---|---|
| Papel | `#f5f1ea` / `#efeae1` | Fondo / tarjetas |
| Tinta | `#1a1a18` | Texto y dato principal |
| Tinta 2 | `#6b675e` | Texto secundario, aviones de línea en gráficos de flota |
| Bermellón (acento) | `#c73e1d` | Lo que se destaca: Mar del Plata, récord, exterior en el mapa, alertas |
| Gris | `#a3a29c` | "Otras" / resto agrupado |
| Gris claro | `#d6d3cb` | Dato faltante ("Sin dato") |
| Categórica (7) | `#2a78d6 #eb6834 #1baf7a #eda100 #e87ba4 #008300 #6250d6` | Segmentos, en orden fijo: línea regular, taxi aéreo, privado, escuelas, oficial, charter, trabajo aéreo |
| Perfil de aeronave | jet `#0d366b` · turbohélice `#3987e5` · pistón 6+ `#c98500` · pistón liviano `#f2c55c` · helicóptero `#1baf7a` · línea `#6b675e` | Con qué vuela cada segmento |
| Secuencial | `#cde2fb → #0d366b` | Intensidad (calendario, mapas de calor) |
| Divergente | bermellón ↔ azul | Más / menos (balance llegados − salidos) |

Tamaños: gráficos a todo el ancho 380 px de alto, de media columna 300 px. Años en barras a 45°.
Ejes de fecha en castellano. Filtros como chips (radio/checkbox) y selects de borde fino.
