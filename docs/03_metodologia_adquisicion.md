# Metodología de adquisición, scraping y estandarización

## 1. Orden de preferencia para obtener un dato

1. **API documentada** (CKAN/DKAN `package_show`, Series de Tiempo) → estable, con metadatos.
2. **Catálogo DCAT** (`/data.json`) → descubrir todo de una, sin paginar.
3. **Archivo estático** (`resources[].url` → CSV/XLSX) → descarga directa.
4. **API interna no documentada** (XHR que usa la web) → descubrir con DevTools/`capture_network.py`;
   tratar como frágil: fijar contrato en un test.
5. **Scraping HTML** (BeautifulSoup) → solo para listar links de archivos.
6. **Navegador headless** (Playwright) → solo si el HTML depende de JS y no hay XHR utilizable.
7. **PDF → tabla** (`pdfplumber`) → último recurso; validar cada tabla contra totales impresos.

Descartado: scrapear iframes de Power BI/Tableau (endpoints `querydata` internos) — frágil y
probablemente contra términos de uso; si una web solo ofrece eso, pedir los datos por
**acceso a la información pública (Ley 27.275)**.

## 2. Cómo descubrir la API detrás de una web (checklist 10 min)

- [ ] Mirar el footer/`/acerca`: "CKAN", "Andino", "DKAN", "Socrata", "ArcGIS Hub" → API conocida.
- [ ] Probar `/api/3/action/status_show` y `/data.json`.
- [ ] URLs `?q=node/...` o `?q=dataset/...` → Drupal/DKAN.
- [ ] DevTools → Network → filtro Fetch/XHR → recargar → buscar respuestas JSON con los números que ves.
- [ ] Click derecho → "Copy as cURL" → reproducir fuera del navegador sin cookies. Si funciona: es API pública de facto.
- [ ] Revisar `robots.txt` y términos de uso. Anotar en `config/sources.yaml` (`robots_checked: fecha`).

## 3. Buenas prácticas de scraping (implementadas en `src/potenciar_mdq/http.py`)

| Práctica | Implementación |
|---|---|
| Identificarse | `User-Agent: PotenciarMDQ/0.1 (+contacto en env CONTACT)` |
| Rate limit | ≥ 1 s entre requests al mismo host (configurable) |
| Reintentos | Backoff exponencial en 429/5xx/timeouts (urllib3 `Retry`), respeta `Retry-After` |
| Timeouts | connect 10 s / read 120 s (CSV grandes) |
| No re-descargar | Comparar `last_modified`/`size` de CKAN y `ETag` HTTP con el manifest; hash sha256 |
| Inmutabilidad | `data/raw/` nunca se edita; cada descarga queda con fecha en el nombre |
| Trazabilidad | `data/raw/manifest.jsonl`: url, fecha, status, bytes, sha256, etag, source_id |
| Fallar fuerte | Si cambia el esquema → excepción con la lista de columnas nuevas, no "seguir de largo" |
| Horario | Correr fuera de horario pico; los portales del Estado son lentos |

## 4. Capas de datos (medallion simple)

```
raw/         tal cual llegó (CSV/XLSX/PDF) + manifest            → inmutable
interim/     CSV transcodificado a UTF-8 (si hacía falta)          → descartable
processed/   parquet con ESQUEMA CANÓNICO, tipado, 1 tabla por entidad
marts/       agregados para análisis/web (DuckDB SQL en sql/)
```

## 5. Estandarización (reglas)

1. **Nombres de columnas**: `slug` (minúsculas, sin acentos, `_`) → mapa de alias → nombre canónico
   (`standardize/columns.py`). Columna no mapeada = error.
2. **Encoding**: detectar UTF-8 vs Latin-1; separador `;` vs `,` (auto-detección DuckDB).
3. **Fechas**: probar formatos `dd/mm/yyyy`, `yyyy-mm-dd`, `dd-mm-yyyy`; guardar `fecha` (DATE) +
   `hora_utc` (TIME) + `fecha_hora_local` (UTC−3).
4. **Categóricas**: normalizar a vocabulario cerrado (`cabotaje|internacional`,
   `aterrizaje|despegue`, `definitivo|provisorio`) — valores fuera de vocabulario se reportan en QA.
5. **Códigos de aeropuerto**: guardar el código tal cual (`aeropuerto_cod_src`) y el resuelto
   (`aeropuerto_iata`, `aeropuerto_oaci`) vía tabla de referencia.
6. **Números**: `pasajeros` entero ≥ 0; vacío ≠ 0 (null se mantiene null).
7. **Linaje**: cada fila lleva `source_id`, `source_file`, `ingested_at`.

## 6. Cruce de datos (reglas)

- Cruzar siempre a la **granularidad más gruesa común** (ej. ANAC por movimiento vs Yvera por ruta-mes → agregar ANAC a ruta-mes antes del join).
- **Mismo universo**: filtrar las mismas clases de vuelo (regular + no regular comercial) antes de comparar.
- **Doble conteo**: el total país suma cada vuelo de cabotaje 2 veces (origen y destino). Para MDQ
  filtrando `aeropuerto = MDQ` no hay doble conteo: pax MDQ = embarcados + desembarcados (estándar ACI).
- **Conservación**: después de cada join, verificar que la suma de pasajeros no cambió (test).
- **Provisorio**: excluir últimos 3 meses de comparaciones interanuales o marcarlos.
- **Huso horario**: Argentina UTC−3 sin horario de verano desde 2009; 2007–2009 tuvo DST → `hora local` aproximada en esos años.

## 7. Calidad (QA) mínima por corrida

- Filas por archivo vs corrida anterior (alerta si ±20 %).
- % nulos por columna clave.
- Duplicados exactos.
- `pasajeros` > capacidad plausible por tipo de aeronave (outliers).
- Meses faltantes en la serie MDQ.
- Reconciliación vs DNTA/informe ANAC (tolerancia 2 %).
