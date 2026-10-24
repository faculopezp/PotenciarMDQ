# Análisis de repos de referencia (2026-10-24)

Criterio: ¿mejora la web o el análisis **con los datos que tenemos** (ANAC por movimiento, portal
municipal, OurAirports) y **con nuestro stack** (Observable Framework, sin React)? Se clonaron en modo
lectura 17 de los 18 repos (el link de "abidaziz1" es una página de temas, no un repo).

## Diseño visual

| Repo | Qué es | Veredicto | Qué tomamos |
|---|---|---|---|
| [madebymustafa/design-taste](https://github.com/madebymustafa/design-taste) | 24 skills de "anti-slop": reglas de tipografía, color, layout y packs de identidad | **Usar** | Pack `editorial-minimal` (diario suizo): papel cálido, tinta, un acento bermellón, serif grande + etiquetas mono, secciones numeradas con filetes, métricas como tabla tipográfica, casi sin animación. Encaja con público general y periodismo de datos. Más su checklist de pre-vuelo |
| [marvkr/better-design](https://github.com/marvkr/better-design) | Servidor MCP con design systems y reglas de revisión WCAG | Tomar reglas | Checklist de revisión: foco visible, contraste, jerarquía, espaciado. No hace falta instalar el MCP |
| [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) | Skill + CLI con cuenta en superdesign.dev | Descartar | Depende de un servicio externo con login; no aporta sobre design-taste |
| [paper-design/shaders](https://github.com/paper-design/shaders) | Shaders WebGL (mesh gradient, puntos), tiene versión vanilla | Descartar por ahora | Choca con la regla "sin orbes ni gradientes" del pack editorial. Opción futura: textura de grano sutil en la portada |
| [ibelick/motion-primitives](https://github.com/ibelick/motion-primitives) | Componentes de animación React + motion | Descartar | Requiere React |
| [ui-layouts/uilayouts](https://github.com/ui-layouts/uilayouts) | Componentes React creativos | Descartar | Requiere React + framer-motion |
| [ui-layouts/cursify](https://github.com/ui-layouts/cursify) | Efectos de cursor React | Descartar | Decorativo, no ayuda a leer datos y no existe en celular |
| [Hyperiux-Immersion-Labs/hyperiux-components](https://github.com/Hyperiux-Immersion-Labs/hyperiux-components) | Efectos inmersivos Next.js (CLI con login, parte paga) | Descartar | Next.js + cuenta |
| [DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui) | Efectos canvas/WebGL agnósticos de framework | Descartar | Licencia MIT + Commons Clause; efectos de fluido no suman a la lectura |
| [akaieuan/trickle-UI-kit](https://github.com/akaieuan/trickle-UI-kit) | Animaciones de texto en CSS puro | Tomar la idea | Animación solo con CSS + `prefers-reduced-motion`: una única entrada suave por sección |

## Análisis de aviación

| Repo | Qué hace | Aplica a MDQ | Qué tomamos |
|---|---|---|---|
| [lapanquecita/lapanquecita](https://github.com/lapanquecita/lapanquecita) | Estadísticas mensuales de aeropuertos de México (AFAC) | **Sí, el más parecido** | 1) **Tendencia STL**: separar la tendencia de la estacionalidad (clave en MDQ). 2) **Ranking nacional** de aeropuertos por pasajeros (escala log) con MDQ resaltado. 3) **Comparación año contra año** mes a mes |
| [wwh9345/Regression-Modeling-US-Airline-On-Time-Performance](https://github.com/wwh9345/Regression-Modeling-US-Airline-On-Time-Performance) | Demoras en EE. UU., gráficos de control, retrasos en cascada | Parcial | **Gráfico de control** (media ± 2σ) para marcar días atípicos (temporales, paros, feriados). Las demoras no aplican: ANAC no publica horarios programados |
| [InnocenceAllen/AENA_Info_Vuelos_V2](https://github.com/InnocenceAllen/AENA_Info_Vuelos_V2) | Vuelos de AENA cruzados con clima | Parcial | **Cruce con clima** (Open-Meteo, gratis): ¿los días de niebla o viento caen los movimientos? |
| [tapashsutradhar/airport-operations-analytics-forecasting](https://github.com/tapashsutradhar/airport-operations-analytics-forecasting) | Pronóstico ARIMA/Prophet (solo README, sin código) | Parcial | **Pronóstico estacional** de pasajeros a 6 meses, con intervalo y advertencia clara |
| [manishkolla/Airline-Data-Analysis](https://github.com/manishkolla/Airline-Data-Analysis) | Demoras por día de la semana | Ya cubierto | El patrón por día de la semana ya está (explorador y mapa de calor) |
| [jahnvisahni31/Airport_analysis](https://github.com/jahnvisahni31/Airport_analysis) | Dashboard Power BI | Ya cubierto | Estructura resumen → detalle → tiempos (ya la tenemos) |
| [Ugochukwuodinaka/…Delay-And-Cancellation-Analysis](https://github.com/Ugochukwuodinaka/Airline-And-Airport-Flight-Delay-And-Cancellation-Analysis) | Demoras y cancelaciones en Power BI | No aplica | Sin datos de cancelaciones |
| abidaziz1 (PageRank con GraphFrames) | Centralidad de aeropuertos en la red | **Sí** | **Centralidad de red** (PageRank/grado) sobre `fct_tramo`: qué lugar ocupa MDQ en la red argentina y cuánto depende de Aeroparque |

## Backlog priorizado

| # | Mejora | Origen | Esfuerzo | Impacto para público general |
|---|---|---|---|---|
| 1 | Rediseño editorial (paleta papel/tinta/bermellón, serif, secciones numeradas, filetes, tabla de métricas) | design-taste | M | Alto |
| 2 | Tendencia STL ("¿crece Mar del Plata, sacando el efecto verano?") | lapanquecita | S | Alto |
| 3 | Ranking nacional con MDQ resaltado | lapanquecita | S | Alto |
| 4 | Serie larga 2014+ con datasets municipales | probe | M | Alto |
| 5 | Vuelos vs turistas (arribos de turistas, portal municipal) | probe | M | Alto |
| 6 | Días atípicos (gráfico de control) | wwh9345 | S | Medio |
| 7 | Centralidad en la red argentina | abidaziz1 | S | Medio |
| 8 | Clima vs operaciones | AENA | M | Medio |
| 9 | Pronóstico 6 meses | tapashsutradhar | S | Medio (riesgo de sobreinterpretación) |
