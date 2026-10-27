"""CLI: pmdq probe | ingest | standardize | bd | qa | marts | web-data | all."""

from __future__ import annotations

import logging

import typer

from potenciar_mdq import analitica, auditoria, fuentes, muestras, quality, web_export
from potenciar_mdq import bd as bd_mod
from potenciar_mdq import ingest as ingest_mod
from potenciar_mdq import marts as marts_mod
from potenciar_mdq.settings import REPORTS
from potenciar_mdq.standardize import anac_movimientos, generic, municipal

app = typer.Typer(no_args_is_help=True, add_completion=False)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


@app.command()
def probe() -> None:
    """Valida endpoints de config/sources.yaml -> reports/probe.md."""
    typer.echo(f"Reporte: {ingest_mod.probe()}")


@app.command()
def ingest(
    only: list[str] = typer.Option(None, help="IDs de fuente (default: enabled)"),
    force: bool = typer.Option(False, help="Re-descargar aunque no haya cambios"),
) -> None:
    """Descarga raw + manifest."""
    files = ingest_mod.ingest(only, force)
    typer.echo(f"{len(files)} archivos nuevos")
    for f in files:
        typer.echo(f"  {f}")


@app.command()
def standardize() -> None:
    """raw -> processed (parquet con esquema canónico)."""
    typer.echo(anac_movimientos.build())
    pasos = ["# Pasos de estandarización", "", "| paso | resultado |", "|---|---|"]
    for step in (generic.build_yvera, generic.build_dim_aeropuerto, generic.build_anac_aeropuertos,
                 generic.build_opensky, generic.build_madhel, generic.build_tar1090,
                 generic.build_clima, generic.build_terrestre, generic.build_tren,
                 generic.build_evyth, generic.build_failbondi,
                 municipal.build):
        try:
            res = step()
            typer.echo(res)
            n = len(res) if isinstance(res, list) else 1
            pasos.append(f"| {step.__name__} | ok ({n} archivo{'s' if n != 1 else ''}) |")
        except Exception as exc:  # noqa: BLE001 - fuentes secundarias: no cortan el pipeline
            typer.echo(f"skip {step.__name__}: {type(exc).__name__}: {exc}")
            pasos.append(f"| {step.__name__} | ❌ {type(exc).__name__}: {str(exc)[:300]} |")
    # El CI commitea reports/qa: así se ve qué fuente secundaria falló sin abrir los logs.
    (REPORTS / "qa").mkdir(parents=True, exist_ok=True)
    (REPORTS / "qa" / "pasos.md").write_text("\n".join(pasos) + "\n", encoding="utf-8")


@app.command()
def bd() -> None:
    """processed -> data/potenciar_mdq.duckdb (+ data/bd/*.parquet)."""
    typer.echo(bd_mod.build())


@app.command()
def qa() -> None:
    """Reporte de calidad -> reports/qa/."""
    typer.echo(quality.run())
    typer.echo(muestras.run())
    try:
        typer.echo(auditoria.run())
    except Exception as exc:  # noqa: BLE001 - la auditoría informa, no corta el pipeline
        typer.echo(f"skip auditoria: {type(exc).__name__}: {exc}")
    try:
        typer.echo(auditoria.run_omnibus())
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"skip auditoria micros: {type(exc).__name__}: {exc}")
    try:
        typer.echo(auditoria.run_puntualidad())
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"skip auditoria puntualidad: {type(exc).__name__}: {exc}")


@app.command()
def marts() -> None:
    """BD -> data/marts/*.parquet."""
    for p in [*marts_mod.build(), *analitica.build()]:
        typer.echo(p)


@app.command(name="web-data")
def web_data() -> None:
    """data/marts -> web/src/data/*.json (lo que publica la web)."""
    for p in web_export.export():
        typer.echo(p)


@app.command(name="muestras-fuentes")
def muestras_fuentes() -> None:
    """Muestras de las fuentes nuevas (CSV y texto de PDF) -> reports/fuentes/."""
    typer.echo(fuentes.run())


@app.command(name="all")
def run_all() -> None:
    ingest(None, False)
    standardize()
    bd()
    qa()
    marts()
    web_data()


if __name__ == "__main__":
    app()
