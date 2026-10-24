# Plan paso a paso — fin de semana

> **Estado 2026-10-24:** etapas 1–5 implementadas y validadas con datos reales 2023–2026 (BD, marts,
> web y despliegue). Falta: primera corrida en GitHub con fuentes oficiales (2019+), extracción de
> PDFs 2014–2018 y calibración de asientos con Yvera. Pasos manuales en `docs/09_pasos_manuales.md`.

## Objetivos (definición de "terminado")

| # | Objetivo | Criterio de aceptación |
|---|---|---|
| O1 | Serie mensual MDQ de movimientos y pasajeros | `mart_mdq_mensual` cubre todos los años disponibles en el CSV ANAC, sin meses faltantes sin explicar |
| O2 | Reconciliación con fuente oficial | Diferencia ≤ 2 % vs informe ANAC/DNTA en ≥ 3 meses testigo (anotados en `config/reconciliacion.csv`) |
| O3 | Métricas estándar | Las métricas de `docs/05_metricas.md` calculadas por año (P1 obligatorias) |
| O4 | Benchmark | MDQ vs ≥ 4 aeropuertos pares en pasajeros, estacionalidad y concentración |
| O5 | Web publicada | 6–8 capítulos con 1 gráfico + 1 insight cada uno, deploy estático con URL |
| O6 | Reproducible | `make all` desde cero regenera todo; fuentes y fechas de descarga en `manifest.jsonl` |

Fuera de alcance del finde (backlog): serie 1954–2013 desde PDFs, cruce con EOH/INDEC, datos ADS-B.

## Timeboxing (≈15 h)

### Viernes noche — 2 h · Etapa 1: validar fuentes
- [ ] `make setup && make probe` → revisar `reports/probe.md`
- [ ] Si `consultas-publicas.anac.gob.ar` es JS: `python scripts/capture_network.py <url>` y anotar endpoints reales en `config/sources.yaml`
- [ ] Bajar 1 CSV anual de ANAC y mirar columnas/encoding/separador a mano (5 min)
- [ ] Confirmar código ANAC de Mar del Plata en el campo `Aeropuerto` (supuesto: `MDP`) → `config/mdq.yaml`

### Sábado AM — 4 h · Etapa 2–3: ingesta + estandarización ANAC
- [ ] `make ingest` (todos los años de "Aterrizajes y despegues")
- [ ] `make standardize` → resolver columnas no mapeadas que reporte el log (`standardize/columns.py`)
- [ ] `make qa` → revisar nulos, duplicados, % provisorio, saltos de volumen
- [ ] Llenar `config/reconciliacion.csv` con 3 meses del informe ANAC y correr reconciliación

### Sábado PM — 3 h · Etapa 3b: Yvera + referencias
- [ ] Ingesta Yvera conectividad aérea (asientos → load factor, rutas)
- [ ] Definir esquema canónico Yvera en `docs/04_modelo_de_datos.md` con columnas reales
- [ ] OurAirports → `data/reference/aeropuertos.parquet` (coordenadas para el mapa)
- [ ] Revisar `config/aeronaves.yaml` contra `SELECT DISTINCT aeronave` de MDQ

### Domingo AM — 3 h · Etapa 4: análisis
- [ ] `make marts`
- [ ] Notebook/SQL exploratorio: 1 hallazgo por capítulo (ver `web/src/index.md`)
- [ ] Hitos: validar `config/hitos.yaml` con fuente primaria o marcarlos como prensa

### Domingo PM — 3 h · Etapa 5: web + deploy
- [ ] Gráficos por capítulo (Observable Plot)
- [ ] Página de metodología y fuentes
- [ ] Deploy (GitHub Pages o Vercel) y revisar en celular

## Riesgos y mitigación

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Portales `.gob.ar` caídos/lentos (pasó con la sección de estadísticas ANAC en 2025) | Bloquea ingesta | Cache raw local + manifest; reintentos con backoff; descargar todo el viernes |
| Columnas cambian entre años del CSV ANAC | Serie rota | Diccionario de alias + test por archivo + falla ruidosa ante columna desconocida |
| Datos provisorios (últimos 3 meses) | Números que cambian | Flag `calidad_dato`; la web muestra hasta el último mes definitivo |
| Serie larga (pre-2014) solo en PDF/prensa | Relato incompleto | Capítulo "antes de los datos" con hitos + backlog de extracción PDF |
| Discrepancias open data vs informe ANAC | Credibilidad | Reconciliación documentada (O2) y nota metodológica visible |
