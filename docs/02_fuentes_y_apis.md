# Fuentes de datos y APIs

> Estado de verificación: los endpoints se dedujeron de la plataforma que usa cada portal
> (CKAN / Portal Andino / DKAN) y de búsqueda web; el entorno de desarrollo no llega a `*.gob.ar`.
> El workflow `actualizar-datos` corre `pmdq probe` en GitHub y deja el resultado en `reports/probe.md`.
>
> **Verificado con datos reales (CSV ANAC 2023–2026 vía espejo público, sin modificar):** formato de
> columnas, código `MDP`, que `PAX` = pasajeros prorrateados (cabotaje / 2) y que la matrícula aparece
> recién en 2026. **Cobertura del CSV por movimiento: desde 2019** (no 2014).

## Diagnóstico: de dónde "chupan" los datos

- **datos.gob.ar, datos.transporte.gob.ar, datos.yvera.gob.ar** → son nodos de **Portal Andino**
  (CKAN + extensiones de la Secretaría de Innovación). Todo lo que ves en la web sale de la
  **API CKAN** (`/api/3/action/...`) y del catálogo **DCAT** (`/data.json`). Los nodos federan
  a datos.gob.ar, por eso el mismo dataset aparece en ambos con IDs `transporte_<uuid>`.
- **datos.mardelplata.gob.ar** → URLs tipo `?q=dataset/...` = **Drupal + DKAN 7.x**. DKAN expone
  una API compatible con CKAN (`/api/3/action/package_show`) y un DataStore
  (`/api/action/datastore/search.json`).
- **consultas-publicas.anac.gob.ar** → app propia de ANAC (rutas `/canal/<uuid>`). No es CKAN.
  Publica archivos por año (2016–2026). Hay que inspeccionar el tráfico de red para ver si los
  links salen de un JSON interno (ver `scripts/capture_network.py`).
- **datos.anac.gob.ar** → portal ANAC con PDFs estáticos (`/static/docs/...`). Su sección de
  estadísticas estuvo caída (404) en 2025 según prensa → no depender de ella.

**Conclusión:** sí hay API pública sin descargar nada a mano para 3 de 5 portales (CKAN/DKAN).
Lo que la API da es **metadatos + URL de descarga** de cada recurso; el dato en sí es un CSV.
`datastore_search` (filas vía JSON) solo existe si el recurso está cargado en DataStore — verificar.

## Inventario

| ID | Fuente | Qué trae | Granularidad | Cobertura | Acceso | Prioridad |
|---|---|---|---|---|---|---|
| `anac_movimientos` | Secretaría de Transporte — [Aterrizajes y despegues procesados por ANAC](https://datos.transporte.gob.ar/dataset?organization=anac) | Cada movimiento: fecha, hora UTC, clase de vuelo, cabotaje/internacional, aterrizaje/despegue, aeropuerto, origen/destino, aerolínea, aeronave, pasajeros, calidad del dato | Movimiento individual | Un CSV por año (a verificar desde qué año); actualización mensual | CKAN `package_show` → `resources[].url` | **P1 (columna vertebral)** |
| `yvera_conectividad` | Min. Turismo — [Conectividad aérea](https://datos.yvera.gob.ar/dataset/conectividad-aerea) (también en [datos.gob.ar](https://www.datos.gob.ar/dataset/turismo-conectividad-aerea)) | Fuente SIAC/ANAC. Vuelos, **asientos**, pasajeros, rutas, aerolíneas. Recursos: "Vuelos, asientos y pasajeros por día" (`indice_tiempo, clasificacion_vuelo, pasajeros, asientos`), "Base agregada de frecuencias aéreas" (incluye `origen_aeropuerto`, `origen_localidad`…), "Principales rutas por año", ficha técnica PDF | Día / ruta-mes | 2017 → hoy, mensual | CKAN | **P1** (único con asientos → load factor) |
| `anac_dnta` | ANAC — [Estadísticas DNTA](https://consultas-publicas.anac.gob.ar/estadisticas-dnta/) | Tablas de movimientos y pasajeros por aeropuerto / operador | Mes | 2016–2026 | Scraping de links (o JSON interno) | **P1 para reconciliación** |
| `ourairports` | [OurAirports](https://ourairports.com/data/) `airports.csv` | Coordenadas, IATA/OACI, `local_code` (= código ANAC, verificado) | Aeropuerto | — | CSV estático, dominio público | P1 (mapa + join de códigos) |
| `anac_movimientos_espejo` | [baubyte/anac-datos-2023-2026](https://github.com/baubyte/anac-datos-2023-2026) | Copia sin modificar de los CSV ANAC 2023–2026 | Movimiento | 2023–2026 | raw.githubusercontent.com | Respaldo automático si el portal no responde |
| `anac_informes_mensuales` | `datos.anac.gob.ar/static/docs/Informe_Mensual_YYYYMM.pdf` | Tablas por aeropuerto | Mes | 2014–2018 a confirmar | PDF | P1 para 2014–2018 |
| `snaero_pdf` | argentina.gob.ar — `estadistica_<AÑO>.pdf` (Sistema Nacional de Aeropuertos) | Pasajeros y movimientos por aeropuerto | Año | 2007, 2009, 2012, 2014, 2015 (otros a verificar) | PDF → `pdfplumber` | P2 (serie larga) |
| `eana_informes` | [EANA](https://eana.com.ar) informes mensuales/anuarios | Movimientos por aeropuerto (vista control de tránsito) | Mes | 2016 → | PDF | P3 (cross-check) |
| `mdp_portal` | [datos.mardelplata.gob.ar](https://datos.mardelplata.gob.ar) | Hoy: turismo (centros de información, gastronomía), callejero. **No se encontró dataset aéreo** | — | — | DKAN | P3 (contexto turístico) |
| `series_tiempo` | [API Series de Tiempo](https://apis.datos.gob.ar/series/api/) | Series agregadas nacionales; buscar `?q=pasajeros aereos` | Mes | — | REST JSON/CSV | P3 |
| `indec_eoh` | INDEC — Encuesta de Ocupación Hotelera (Mar del Plata es localidad relevada) | Pernoctes/viajeros hospedados | Mes | — | XLS | Backlog (cruce turismo) |
| `opensky` | OpenSky Network | Trayectorias ADS-B | Vuelo | Cobertura baja en AR | API con cuenta | Descartado para el finde |

## Endpoints concretos

### CKAN / Andino (transporte, yvera, datos.gob.ar)

```text
GET {base}/api/3/action/status_show
GET {base}/api/3/action/package_search?q=aterrizajes&rows=100&start=0
GET {base}/api/3/action/package_search?fq=organization:anac&rows=100
GET {base}/api/3/action/package_show?id={dataset_slug}
GET {base}/api/3/action/datastore_search?resource_id={id}&limit=1000&offset=0   # si DataStore está activo
GET {base}/data.json                                                           # catálogo DCAT completo (Andino)
```

Slugs/IDs a validar con `make probe`:

- transporte: `aterrizajes-y-despegues-procesados-por-la-administracion-nacional-de-aviacion-civil-anac`
  (recurso 2026 visto: `7b6d0103-0a69-4c67-aed9-33cb58ae12f5`)
- datos.gob.ar (federado): `transporte-aterrizajes-despegues-procesados-por-administracion-nacional-aviacion-civil-anac`
- yvera: `conectividad-aerea` (recursos vistos: `d406a6fa-…`, `03b4176f-…`, `bdb24072-…`, `aab49234-…`, `26bf262e-…`, ficha PDF `b23e3a61-…`)

### DKAN (Mar del Plata)

```text
GET https://datos.mardelplata.gob.ar/api/3/action/package_list
GET https://datos.mardelplata.gob.ar/api/3/action/package_show?id={slug}
GET https://datos.mardelplata.gob.ar/api/action/datastore/search.json?resource_id={id}&limit=100
# fallback Drupal sin clean URLs:
GET https://datos.mardelplata.gob.ar/?q=api/3/action/package_list
```

### ANAC DNTA (consultas públicas)

1. `GET /estadisticas-dnta/` y `/estadisticas-dnta/canal/{uuid}` → parsear `<a href>` a `.xlsx/.xls/.csv/.pdf`.
2. Si el HTML viene vacío (render JS) → `scripts/capture_network.py` registra los XHR/fetch; el
   endpoint JSON que liste archivos se agrega a `config/sources.yaml` como `kind: json_api`.

## Identificadores de Mar del Plata

| Sistema | Código | Estado |
|---|---|---|
| IATA | `MDQ` | conocido |
| OACI | `SAZM` | conocido |
| ANAC/local (usado en el CSV de movimientos, campo `Aeropuerto` y `Origen / Destino`) | `MDP` | verificado (datos reales + `local_code` de OurAirports) |

## Cruces posibles (y la llave)

| Cruce | Llave | Para qué |
|---|---|---|
| ANAC movimientos × OurAirports | `aeropuerto` / `origen_destino` ↔ `local_code` (fallback `ident`/OACI para extranjeros) | Coordenadas, nombres, ciudad → mapa de rutas |
| ANAC movimientos × Yvera | (`anio`,`mes`, ruta MDQ↔destino, `clasificacion`) | Load factor = pax ANAC / asientos Yvera (o pax/asientos ambos Yvera — preferido, misma fuente) |
| ANAC movimientos × DNTA | (`anio`,`mes`,`aeropuerto`) | Reconciliación de totales |
| MDQ × INDEC EOH | (`anio`,`mes`) | ¿El avión explica la ocupación hotelera fuera de temporada? |
| ANAC × `config/aeronaves.yaml` | regex sobre `aeronave` | Categoría de flota (jet/turbohélice/aviación general) |

## Hallazgo 2026-10-24: series municipales (datos.mardelplata.gob.ar, DKAN)

Verificado por `pmdq probe` desde GitHub Actions (vista previa en `reports/probe.md`):

| Dataset (slug) | Contenido | Cobertura | Problemas de formato |
|---|---|---|---|
| `movimientos-del-aeropuerto-internacional-astor-piazzolla` | Movimientos mensuales cabotaje / internacional (formato ancho, un CSV por año) | **2001–2020** | 2019–2020 vienen ×1000; miles con coma entre comillas (`"1,073"`) |
| `vuelos-del-aeropuerto-internacional-astor-piazzolla` | Movimientos individuales (fecha, hora, clase, OACI origen/destino, aerolínea, aeronave; sin pasajeros) | **2015–2019** | Latin-1, coma como separador, hora sin minutos |
| `pasajeros-del-aeropuerto-astor-piazzolla` | Pasajeros arribados + embarcados por mes, en miles | 2020–2022 (+ a confirmar) | `;`, meses como `ene-22`, valores en miles |
| `vuelos-comerciales-pasajeros-por-tramo` | Pasajeros por ruta y mes | 2022–2024 (+) | `;`, Latin-1 |
| `vuelos-comerciales-vuelos-por-tramo` | Vuelos por ruta y mes | 2018–2020 (+) | 2019–2020 ×1000 |
| `arribos-de-turistas` | Turistas arribados por mes | **2007–2025** | Punto de miles (`1.422.547`) |
| `turismo-en-fines-de-semana-largo` | Visitantes por fin de semana largo | 2007–2025 | `n/h` = no hubo |
| `turismo-estable-estadía-promedio` | Estadía promedio y turistas estables por mes | 2006–2024 | Decimal con punto o coma según el año; `-` = sin dato |

Con esto la serie de movimientos llega a **2001** y se puede cruzar aviación con turismo (2007+).
## Lista oficial de aeródromos (ANAC / Secretaría de Transporte) — verificada 2026-10-24

- URL: `datos.transporte.gob.ar/.../aeropuertos_detalle.csv` (`config/sources.yaml → anac_aeropuertos`).
- Columnas: `local;oaci;iata;tipo;denominacion;coordenadas;latitud;longitud;elev;...;provincia;inhab`.
- **Las columnas `latitud` y `longitud` vienen invertidas** (ej. ACB Coronel Bogado: `coordenadas`
  33°16'20"S 60°34'14"W, `latitud` -60.57). Se usa `coordenadas` (DMS con hemisferio) como fuente
  principal. El cruce contra OurAirports queda en reports/qa ("Lista ANAC vs OurAirports").
- Los **códigos numéricos** del CSV de movimientos (ej. 2278, 3073, 2574) no están en esta lista
  ni en OurAirports. ANAC los clasifica como "internacional" aunque los informan aeropuertos del
  interior (Salta, Posadas, San Fernando). En la web no se cuentan como vuelos al exterior.
- Resolución de códigos (dim_aeropuerto): OurAirports AR `local_code` → lista ANAC → Antártida →
  OACI (`ident` y `gps_code`; ej. SPJC Lima figura en OurAirports con ident SPIM).
