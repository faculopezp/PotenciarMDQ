# Reportes de referencia (para usar como guía)

Criterio: qué copiar de cada uno (estructura, métricas, forma de contar). Marcado si lo
abrí o solo lo encontré por búsqueda (el entorno de investigación no tenía acceso directo a `*.gob.ar`).

## Oficiales Argentina

| Reporte | Qué tomar | Acceso |
|---|---|---|
| [ANAC — Anuario Estadístico 2019](https://datos.anac.gob.ar/static/docs/anuario_ANAC_2019.pdf) | Convención de conteo: vuelo de cabotaje = 2 movimientos, internacional = 1 (en totales país). Estructura anual por aeropuerto/aerolínea | búsqueda |
| [ANAC — Informe Mensual dic-2021](https://datos.anac.gob.ar/static/docs/Informe_Mensual_202112.pdf) | Notas generales/metodología, formato de tabla mensual por aeropuerto → base para reconciliación | búsqueda |
| [ANAC/DNTA — Estadísticas en Consultas Públicas](https://consultas-publicas.anac.gob.ar/estadisticas-dnta/) | Informes de la Dirección de Estudios de Mercado y Estadísticas: pasajeros cabotaje/internacional, operadores, movimientos y demanda por aeropuerto; archivos por año 2016–2026 | búsqueda |
| [EANA — Informes mensuales](https://eana.com.ar/sites/default/files/2023-11/EANA%20Informe%20Mensual%202023-10.pdf) | Datos de SIAC (ANAC) consolidados con sistemas ATM; define "movimiento" = aterrizaje o despegue; últimos 3 meses provisorios | búsqueda |
| [Yvera — Tablero de Conectividad Aérea](https://tableros.yvera.tur.ar/conectividad.html) + [Bitácora: datos abiertos de conectividad](https://bitacora.yvera.tur.ar/posts/2023-08-23-datos-abiertos-de-conectividad-aerea/) | Enfoque turismo: asientos, pasajeros, rutas, aerolíneas desde 2017. Modelo de "tablero + nota metodológica" | búsqueda |
| [Sistema Nacional de Aeropuertos — estadística anual (ej. 2015)](https://www.argentina.gob.ar/sites/default/files/estadistica_2015.pdf) | Pasajeros por aeropuerto (cabotaje/internacional/tránsito) — única vía para serie pre-2014. Hay PDFs 2007, 2009, 2012, 2014, 2015 | búsqueda |

## Internacionales (estándar de métricas)

| Reporte | Qué tomar |
|---|---|
| [UK CAA — Aviation Trends (trimestral)](https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/latest-quarterly-statistics/) | Definiciones limpias: load factor = pax/asientos; asientos por vuelo; doble conteo de cabotaje; exclusión de air taxi. Formato "trends" corto con 1 gráfico + 1 mensaje |
| ICAO — Statistics Programme / ACI World Airport Traffic Report | Pax = embarcados + desembarcados; ATM vs movimientos totales (incluye aviación general) |

## Prensa / análisis sectorial (contexto, NO fuente de datos)

| Fuente | Uso |
|---|---|
| [Aviacionline — verano 2025 MDQ](https://aviacionline.com/menos-vuelos-a-mar-del-plata-durante-el-verano-2025-se-proyecta-una-caida-de-dos-digitos-en-la-oferta) | Récord de la década 2018: 454.162 pax; caída de oferta verano 2025 (~121 mil asientos ene–mar, −11,3 %); Corredor Atlántico suspendido sep-2024 → hitos |
| [La Capital MDP — +346 % en 10 años](https://www.lacapitalmdp.com/la-cantidad-de-pasajeros-que-llega-al-aeropuerto-local-aumento-346-en-los-ultimos-diez-anos/) | 2008 ≈ 50 mil vs 2018 = 222.685 **arribos** (cita ANAC). Ojo: arribos ≠ total pax (≈ ½) → buen test de consistencia |
| [La Capital MDP — se duplicó la cantidad de pasajeros](https://www.lacapitalmdp.com/se-duplico-la-cantidad-de-pasajeros-que-llegan-a-mar-del-plata-en-avion/) | 2001 ≈ 300 mil pax vs 2015 ≈ 200 mil (serie EMTUR) → contexto pre-datos abiertos |
| [El Economista — Flybondi a MDQ](https://eleconomista.com.ar/negocios/flybondi-comenzo-volar-mar-plata-50-minutos-cuatro-frecuencias-semana-n69791) | Hito low cost verano 2024 |
| [iProfesional — plenario conectividad 2026](https://www.iprofesional.com/actualidad/456499-la-confirmacion-con-la-que-suena-mar-del-plata-para-reafirmar-su-liderazgo-turistico) | Contexto político actual: objetivo desestacionalizar vía conectividad |
| [CIDETUR UNSAM — boletín jun-2018](https://icrym.unsam.edu.ar/escuelas/eeyn/centros/cidetur/boletines/boletin_junio_2018.pdf) | Formato de boletín de turismo con datos aéreos |

## Proyectos de código similares

| Repo | Qué tomar |
|---|---|
| [alvarofpp/dataset-flights-brazil](https://github.com/alvarofpp/dataset-flights-brazil) | Estructura: descarga ANAC-BR → merge → dataset de aeropuertos → grafo de rutas |
| [Paola Corrales — #30DayMapChallenge día 2](https://paocorrales.github.io/30DayMapChallenge2023/day2.html) | Mapa de rutas con datos ANAC (R) — referencia visual para el capítulo "a dónde" |
| [CRAN flightsbr](https://packages.oit.ncsu.edu/cran/web/packages/flightsbr/refman/flightsbr.html) | API de paquete para datos ANAC-BR: buen modelo de interfaz `read_flights(year)` |

## Estructura de relato recomendada (síntesis)

Los reportes buenos comparten: **1 pregunta → 1 gráfico → 1 número → 1 frase de "por qué importa"**.
Capítulos propuestos en `web/src/index.md`.
