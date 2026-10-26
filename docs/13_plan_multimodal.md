# Plan: PotenciarMDQ multimodal (aviación, ómnibus, tren, autos, mar)

Estado: **plan, nada construido**. Fuentes verificadas el 2026-10-26 solo con búsqueda web: desde el
entorno de desarrollo no se llega a los sitios .gob.ar. Cada fuente lleva su estado de verificación.

## 1. Diagnóstico

- **Aviación:** ANAC publica cada movimiento. Es el único modo con datos registro por registro, y por
  eso la sección de aviación es profunda (rotaciones, avión típico, pulso diario).
- **Ómnibus:** existe un equivalente casi directo a la base de vuelos de Yvera:
  **Conectividad terrestre interurbana** (CNRT vía Yvera, desde 2019, viajes, asientos y
  pasajeros por ruta). Alcanza para una sección sólida, pero agregada por ruta y no por micro.
- **Tren, autos y mar:** no tienen datos abiertos tabulares por viaje. Hay PDF oficiales (CNRT
  ferroviario, informes de pesca de MAGyP), prensa con cifras puntuales (peajes de AUBASA,
  terminal, cruceros) y el total de arribos de EMTUR. Sirven para secciones más livianas o para
  una página comparativa, no para el mismo nivel de detalle.

## 2. Recomendación

1. **Landing + ómnibus primero.** El ómnibus reutiliza casi todo lo aprendido: misma fuente madre
   (Yvera), misma lógica de rutas, asientos y ocupación, y la comparación directa contra el avión
   en las mismas rutas.
2. **Página transversal "Cómo llega la gente"** con los arribos de EMTUR (2007–2025, ya cargados),
   más el reparto por modo donde exista (EVyTH de Yvera, a verificar) y las series de cada modo.
   Es la página que justifica la landing.
3. **Tren, autos y mar como secciones livianas** (series mensuales o anuales y contexto), con la
   cobertura bien explicada. Solo se suben de nivel si aparece una fuente abierta mejor o la
   consiguen ustedes (pedido a AUBASA, Consorcio Portuario).

## 3. Lo que aprendimos con aviación (y se aplica desde el día 1)

| Aprendizaje | Cómo se aplica |
|---|---|
| Las fuentes oficiales cambian sin aviso: ANAC vació el avión de 2019 en una versión nueva | Guardar cada descarga con fecha y hash; no pisar versiones viejas; diff entre versiones en el reporte de calidad |
| El entorno de desarrollo no llega a *.gob.ar; el CI sí | Probe automático en el CI (`reports/probe.md`) antes de modelar; espejo local de una muestra; pasos tolerantes a fallas que escriben el error en el reporte |
| Validar con datos reales antes de suponer el formato | Probe con vista previa de columnas y filas; tests con fixtures reales |
| Recuperar solo con cruces exactos y validados | Cada regla de recuperación se valida contra los registros que sí traen el dato; se publica el porcentaje de acierto |
| Mismo origen no es validación independiente (Yvera, EANA y ANAC salen todos del SIAC) | Documentar el origen de cada fuente; separar "consistencia" de "exactitud" |
| Nombres sucios (operadores, modelos) | Normalizar con config YAML más tests: empresas de micro (Plusmar, Rápido Argentino, Flechabus…) y estaciones |
| Segmentos y reclasificaciones discutibles | Definirlos en config, marcar los reclasificados y explicarlos en Metodología |
| Cobertura por gráfico | Mart de cobertura por modo y renglón al pie de cada gráfico desde el primer día |
| Corridas del CI que chocan al subir datos | Ya resuelto: rebase con "gana la más nueva"; agregar `concurrency` por modo |
| Fuentes sin API (Afectación) | Rutina de extracción manual con un prompt fijo, archivo fechado más log y repetición periódica |
| Licencias para sitio público | Antes de usar una fuente comercial, revisar si permite publicar datos derivados |

## 4. Arquitectura del sitio

```
/                      Landing: una tarjeta por modo (cifra clave, tendencia, acceso) y "Cómo llega la gente"
/llegadas              Página transversal: arribos de EMTUR, reparto por modo, estacionalidad comparada
/aviacion/...          Lo actual (historia, toda la aviación, explorador)
/omnibus/...           Historia, rutas, empresas, ocupación, explorador
/tren/...              Servicio Constitución–MdP: pasajeros, frecuencias, temporada
/autos/...             Peajes, rutas 2 / 11 / 226, flujo en fines de semana largos
/mar/...               Puerto: pesca (desembarques), cruceros, carga si existe
/metodologia           Una sola página con una pestaña o sección por modo y la tabla de cobertura
```

- **Repo:** el mismo monorepo. El núcleo reutilizable (ingest, probe, standardize, qa, auditoría,
  web_export, paleta y componentes) pasa a `potenciar_mdq/core`. Cada modo agrega su config
  (`config/<modo>/`), su SQL (`sql/<modo>/`) y sus páginas (`web/src/<modo>/`).
- **Base:** una sola DuckDB con prefijo por modo (`av_`, `bus_`, `tren_`, `auto_`, `mar_`) y
  dimensiones compartidas (`dim_fecha`, feriados, clima, `dim_localidad` con códigos INDEC,
  OACI y CNRT).
- **CI:** un workflow por modo, con frecuencia propia (aviación y ómnibus mensual, tren
  trimestral, mar mensual) y `concurrency` por modo. Vercel publica igual que hoy.
- **Diseño:** la paleta y los tamaños actuales (`docs/11_paleta.md`) son el sistema. Cada modo toma
  un color de acento propio para la landing; adentro, los colores siguen significando lo mismo.

## 5. Fuentes por modo

Estado: **V** = verificada a nivel de metadatos (búsqueda); **P** = existe pero en PDF o tablero;
**?** = sin confirmar; **✗** = no hay dato abierto.

### Ómnibus (fase 1)

| Fuente | Qué trae | Período | Estado |
|---|---|---|---|
| Yvera — [Conectividad terrestre interurbana](https://datos.yvera.gob.ar/dataset/conectividad-terrestre-interurbana) (CNRT) | Servicios regulares de jurisdicción nacional entre cabeceras: viajes, asientos y pasajeros por ruta (excluye cancelados, < 3 pasajeros y mismo origen/destino) | 2019 → hoy | V |
| Documento de trabajo DNMyE ([PDF](https://tableros.yvera.tur.ar/recursos/biblioteca/conectividad_terrestre.pdf), [ficha](https://datos.yvera.gob.ar/dataset/b18f1c90-0c66-4771-8bd8-289e5cfa6e60/resource/a5b850c6-8865-4945-848e-44e8fc43388c/download/transporte_terrestre.pdf)) | Metodología y resultados 2019–2023 | 2019–2023 | V |
| CNRT — [estadísticas automotor](https://www.argentina.gob.ar/transporte/cnrt/estadisticas-automotor) | Informes de interurbano y urbano (servicios, pasajeros, parque) | último visto 2017 | P |
| SUBE — [transacciones por día](https://datos.gob.ar/dataset/transporte-sube---cantidad-transacciones-usos-por-fecha) (empresa, línea, provincia, municipio) | Colectivo urbano de Mar del Plata, si figura General Pueyrredon | 2020 → | ? (falta confirmar el municipio) |
| Terminal ferroautomotora (torre de control) | Micros ingresados por día | — | ✗ (solo prensa, ej. [La Capital](https://www.lacapitalmdp.com/cayo-la-cantidad-de-micros-que-ingreso-a-mar-del-plata-en-lo-que-va-de-la-temporada/)) |
| GTFS urbano de Mar del Plata | Recorridos y paradas | — | ? |

**Qué se puede contar:**
- Pasajeros y asientos por ruta y mes, y ocupación.
- Rutas que crecen y caen.
- Empresas, si el dataset las trae (el tablero sí las muestra).
- Estacionalidad contra el avión.
- **Micro contra avión en la misma ruta:** Buenos Aires–MdP, Córdoba–MdP, Rosario–MdP.

### Tren (fase 3)

| Fuente | Qué trae | Período | Estado |
|---|---|---|---|
| CNRT — [estadísticas ferroviarias](https://www.argentina.gob.ar/transporte/cnrt/estadisticas-ferroviarias): anuario de larga distancia ([2023](https://www.argentina.gob.ar/sites/default/files/informe_estadistico_2023_ffcc_pasajeros_larga_distancia_if-2024-34515082-apn-sfgsldcnrt.pdf), [2019](https://argentina.gob.ar/sites/default/files/info_estadistico_pasajeros_larga_distancia_2019.pdf)) y [reportes trimestrales](https://www.argentina.gob.ar/sites/default/files/reporte_trimestral_pax_ld_2024-1.pdf) | Pasajeros por servicio (Constitución–MdP) | 2019–2024 | P (parseo de PDF) |
| Trenes Argentinos (prensa) | Venta de pasajes de temporada | puntual | P |

**Qué se puede contar:** serie anual o trimestral de pasajeros del servicio, su peso frente a
micro y avión, y la temporada.

### Autos (fase 4)

| Fuente | Qué trae | Período | Estado |
|---|---|---|---|
| EMTUR arribos (ya cargado) | Turistas por mes, total sin separar por modo | 2007–2025 | V |
| Reparto por modo (EMTUR, informes municipales hasta 2018) | Por ejemplo, enero 2018: auto 77 %, ómnibus 18 %, avión 2,4 %, tren 2,3 % ([UNMdP](https://nulan.mdp.edu.ar/id/eprint/3911/1/roldan-etal-2023.pdf)) | ≤ 2018 | P |
| AUBASA — peajes Samborombón, La Huella, Maipú, Madariaga, Mar Chiquita | Tránsito: solo cifras de prensa; tarifas en [resoluciones](https://normas.gba.gob.ar/ar-b/resolucion/2025/1190/557055) | — | ✗ datos / V tarifas |
| Vialidad Nacional — [TMDA](https://www.datos.gob.ar/dataset/transporte-tmda) | Tránsito medio diario por tramo de ruta nacional (Ruta 226) | 2017 | V (desactualizado) |
| Yvera — EVyTH (Encuesta de Viajes y Turismo de los Hogares), microdatos | Viajes de residentes con medio de transporte y destino (región) | 2012 → | ? (confirmar que identifique Mar del Plata o la Costa Atlántica) |

**Qué se puede contar:** poco con datos propios. Lo valioso es el reparto por modo (EVyTH) y, si
AUBASA comparte datos, el pulso de los fines de semana largos. Recomiendo un pedido formal a AUBASA
o al Ministerio de Infraestructura de la Provincia de Buenos Aires.

### Mar (fase 4)

| Fuente | Qué trae | Período | Estado |
|---|---|---|---|
| MAGyP — [informes de coyuntura de pesca marítima](https://www.magyp.gob.ar/sitio/areas/pesca_maritima/informes/coyuntura/_archivos/260000_2026/260501_Informe%20de%20Coyuntura%20-%20Mayo%202026.pdf) | Desembarques por puerto y especie (MdP es el puerto principal) | mensual, varios años | P (parseo de PDF); buscar CSV en datos.magyp |
| Consorcio Portuario Regional MdP | Cruceros, buques, carga | — | ✗ (solo prensa, ej. [El Marplatense](https://www.elmarplatense.com/un-crucero-con-mas-de-300-pasajeros-amarro-en-mar-del-plata)) |
| Subsecretaría de Puertos | Estadísticas de carga por puerto | — | ? |

**Qué se puede contar:** el puerto pesquero (desembarques mensuales, especies, comparación con
otros puertos), que es más "Mar del Plata" que los cruceros. Los cruceros, como hitos.

### Transversal (ya disponible)

- Arribos de EMTUR, fines de semana largos, clima (Open-Meteo) y feriados: ya están en la base.

## 6. Fases

| Fase | Entrega | Depende de |
|---|---|---|
| 0 · Plataforma | Núcleo reutilizable, landing con tarjetas, navegación por modo, Metodología por modo. Aviación pasa a `/aviacion` sin cambiar datos | — |
| 1 · Ómnibus | Pipeline de Yvera terrestre, normalización de empresas y localidades, marts, páginas, cobertura y auditoría | Probe en CI de los recursos de Yvera terrestre |
| 2 · Cómo llega la gente | Página transversal con EMTUR, reparto por modo y series de avión y ómnibus | Fase 1; EVyTH si identifica el destino |
| 3 · Tren | Parser de los PDF de CNRT, serie del servicio Constitución–MdP | Probe de los PDF |
| 4 · Autos y mar | Secciones livianas; pesca desde los PDF de MAGyP; peajes si se consiguen | Pedidos de datos |

## 7. Decisiones abiertas

- [ ] ¿La landing reemplaza la home actual de aviación o vive en otro dominio?
- [ ] ¿El colectivo urbano (SUBE) entra en "ómnibus" o queda afuera? Recomiendo afuera en la fase 1,
      porque es otra historia: movilidad interna, no llegada a la ciudad.
- [ ] ¿Mar = puerto pesquero, cruceros, o ambos?

## 8. Próximos pasos (sin construir)

- [ ] Agregar al CI, sin activar el pipeline, un probe de las fuentes nuevas: los recursos de Yvera
      terrestre (columnas, filas y si trae empresa y cabeceras de MdP), SUBE (si figura General
      Pueyrredon), EVyTH (campo de destino y de transporte), CNRT ferroviario y datos.magyp.
- [ ] Sesión local con Chrome: revisar datos.mardelplata.gob.ar (transporte, terminal, peajes) y el
      sitio del Consorcio Portuario.
- [ ] Definir con vos las decisiones de la sección 7.
- [ ] Con el probe hecho: estimar la fase 0 y la fase 1 y arrancar.
