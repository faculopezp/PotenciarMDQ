"""CLI: pmdq probe | ingest | standardize | bd | qa | marts | web-data | all."""

from __future__ import annotations

import logging

import typer

from potenciar_mdq import analitica, muestras, quality, web_export
from potenciar_mdq import bd as bd_mod
from potenciar_mdq import ingest as ingest_mod
from potenciar_mdq import marts as marts_mod
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
    for step in (generic.build_yvera, generic.build_dim_aeropuerto, generic.build_anac_aeropuertos,
                 generic.build_opensky, generic.build_madhel,
                 generic.build_clima,
                 municipal.build):
        try:
            typer.echo(step())
        except Exception as exc:  # noqa: BLE001 - fuentes secundarias: no cortan el pipeline
            typer.echo(f"skip {step.__name__}: {type(exc).__name__}: {exc}")


@app.command()
def bd() -> None:
    """processed -> data/potenciar_mdq.duckdb (+ data/bd/*.parquet)."""
    typer.echo(bd_mod.build())


@app.command()
def qa() -> None:
    """Reporte de calidad -> reports/qa/."""
    typer.echo(quality.run())
    typer.echo(muestras.run())


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
