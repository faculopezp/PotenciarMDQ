# Decisiones y supuestos

## Decisiones del dueño del proyecto (2026-10-24)

| Tema | Decisión |
|---|---|
| Audiencia | Público general → lenguaje simple, sin recomendaciones de política |
| Horizonte | 2014 → hoy; antes de 2014, más adelante |
| Pares | Bariloche, Neuquén, Bahía Blanca, Mendoza, Salta |
| Repo / deploy | `faculopezp/PotenciarMDQ` + Vercel `potenciar-mdq` |
| Actualización | Automática mensual (GitHub Actions, días 5 y 20) |

## Supuestos y hallazgos que cambian el plan

| # | Tema | Estado |
|---|---|---|
| S1 | Comercial = regular + no regular | Vigente (`config/mdq.yaml`) |
| S2 | Código ANAC de MDQ = `MDP` | **Verificado** con datos reales y OurAirports |
| S3 | Serie desde 2014 | **Solo desde 2019 hay datos por movimiento.** 2014–2018 sale de informes mensuales ANAC (PDF) y anuarios del Sistema Nacional de Aeropuertos (PDF): se descargan, la extracción queda como próximo paso |
| S4 | Stack | Python + DuckDB (BD) · Observable Framework (web estática, sin CDN) |
| S5 | Asientos | ANAC no publica asientos: se estiman por avión (p95). Yvera trae asientos oficiales desde 2017 → calibración pendiente |
