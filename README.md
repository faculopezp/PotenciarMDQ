# PotenciarMDQ

Análisis y relato web de la aviación comercial en Mar del Plata (Aeropuerto Astor Piazzolla —
IATA `MDQ`, OACI `SAZM`, código ANAC `MDP`) con datos abiertos.

**Web:** <https://potenciar-mdq.vercel.app> · se actualiza sola los días 5 y 20 de cada mes.

## Qué hay

- **Nuestra BD** (`data/potenciar_mdq.duckdb`): cada aterrizaje y despegue del país desde 2019,
  estandarizado y enriquecido (calendario y feriados, aerolínea y avión normalizados, distancias,
  asientos y load factor estimados), más vuelos reconstruidos (duración) y rotaciones (turnaround).
  Diccionario y métricas: [`docs/07_bd_y_metricas.md`](docs/07_bd_y_metricas.md).
- **Web** (`web/`, Observable Framework): historia en 11 capítulos para público general, explorador
  interactivo y metodología. Referencias de diseño: [`docs/08_dashboards_referencia.md`](docs/08_dashboards_referencia.md).
- **Automatización**: `.github/workflows/actualizar-datos.yml` baja datos → BD → marts → JSON de la web
  → commit → Vercel publica.

## Pipeline

```
fuentes (ANAC CKAN, OurAirports, PDFs ANAC 2014–18, espejo de respaldo)
  └─ pmdq ingest       data/raw/ + manifest.jsonl
  └─ pmdq standardize  data/processed/stg_movimiento.parquet (esquema canónico)
  └─ pmdq bd           data/potenciar_mdq.duckdb (dims + fct_movimiento + fct_tramo + fct_rotacion)
  └─ pmdq qa           reports/qa/anac_movimientos.md
  └─ pmdq marts        data/marts/*.parquet (sql/mart_*.sql)
  └─ pmdq web-data     web/src/data/*.json (versionado; Vercel compila solo con Node)
```

## Uso local

```bash
make setup     # uv + dependencias
make all       # ingest → standardize → bd → qa → marts → web-data
make web-dev   # http://localhost:3000
make test      # 28 tests (fixtures sintéticos + extracto real de OurAirports)
```

## Documentación

| Doc | Contenido |
|---|---|
| `docs/00_plan.md` | Plan, objetivos y estado |
| `docs/01_reportes_referencia.md` | Reportes usados como guía |
| `docs/02_fuentes_y_apis.md` | Fuentes, APIs (CKAN/DKAN) y cruces |
| `docs/03_metodologia_adquisicion.md` | Scraping y buenas prácticas |
| `docs/07_bd_y_metricas.md` | Diccionario de la BD y métricas |
| `docs/08_dashboards_referencia.md` | Dashboards de referencia |
| `docs/09_pasos_manuales.md` | Lo que hay que hacer a mano |
| `docs/06_preguntas_y_supuestos.md` | Decisiones y supuestos |
