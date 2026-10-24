"""Marts analíticos en Python: tendencia (STL), red de aeropuertos (PageRank) y pronóstico.

Se ejecutan después de los marts SQL y escriben en data/marts/ con el mismo formato.
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import duckdb
import networkx as nx
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import STL

from potenciar_mdq import bd
from potenciar_mdq.settings import BD, MARTS

log = logging.getLogger(__name__)


def _mensual_linea(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Pasajeros de línea por mes en el foco, solo meses definitivos y completos."""
    df = con.execute("""
        SELECT make_date(anio, mes, 1) AS periodo, sum(pasajeros) AS pasajeros,
               bool_or(es_provisorio) AS provisorio, count(DISTINCT fecha) AS dias
        FROM fct_movimiento
        WHERE aeropuerto = getvariable('foco') AND es_linea
        GROUP BY ALL ORDER BY periodo
    """).df()
    df["periodo"] = pd.to_datetime(df["periodo"])
    completo = df["dias"] >= df["periodo"].dt.days_in_month - 1
    return df[completo & ~df["provisorio"]].set_index("periodo").asfreq("MS")


def tendencia(con: duckdb.DuckDBPyConnection, marts: Path = MARTS) -> pd.DataFrame:
    """STL sobre la serie larga (municipal 2001–2018 + ANAC 2019+), solo meses completos."""
    larga = marts / "mart_mdq_serie_larga.parquet"
    if larga.exists():
        df = duckdb.sql(f"SELECT periodo, pasajeros, tiene_provisorio FROM '{larga}'").df()
        df["periodo"] = pd.to_datetime(df["periodo"])
        df = df[~df["tiene_provisorio"]].set_index("periodo").asfreq("MS")
        ultimo_completo = _mensual_linea(con).index.max()
        s = df["pasajeros"].astype(float)
        s = s[s.index <= ultimo_completo] if pd.notna(ultimo_completo) else s
    else:
        s = _mensual_linea(con)["pasajeros"].astype(float)
    s = _tramo_continuo(s.interpolate(limit=2))
    if len(s) < 36:
        log.warning("Tendencia: serie corta (%d meses)", len(s))
        return pd.DataFrame(columns=["periodo", "pasajeros", "tendencia", "estacional", "residuo"])
    res = STL(s, period=12, robust=True).fit()
    out = pd.DataFrame({
        "periodo": s.index.date,
        "pasajeros": s.values,
        "tendencia": res.trend.values.round(0),
        "estacional": res.seasonal.values.round(0),
        "residuo": res.resid.values.round(0),
    })
    return out


def _tramo_continuo(s: pd.Series) -> pd.Series:
    """El tramo más reciente sin huecos (STL necesita una serie regular)."""
    s = s.copy()
    huecos = s.isna()
    if not huecos.any():
        return s
    ultimo_hueco = s.index[huecos][-1]
    return s[s.index > ultimo_hueco]


def pronostico(con: duckdb.DuckDBPyConnection, horizonte: int = 6, desde: str = "2022-06-01",
               simulaciones: int = 2000) -> pd.DataFrame:
    """Holt-Winters (log, tendencia y estacionalidad aditivas) sobre la serie pospandemia."""
    s = _mensual_linea(con)["pasajeros"].astype(float)
    s = s[s.index >= desde].dropna()
    if len(s) < 30:
        log.warning("Pronóstico: serie pospandemia corta (%d meses)", len(s))
        return pd.DataFrame(columns=["periodo", "tipo", "pasajeros", "p10", "p90"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = ExponentialSmoothing(np.log(s), trend="add", damped_trend=True, seasonal="add",
                                   seasonal_periods=12, initialization_method="estimated").fit()
        sims = fit.simulate(
            horizonte, repetitions=simulaciones, error="add", random_errors="bootstrap"
        )
    futuro = pd.date_range(s.index[-1] + pd.offsets.MonthBegin(1), periods=horizonte, freq="MS")
    sims = np.exp(np.asarray(sims))
    hist = pd.DataFrame({"periodo": s.index.date, "tipo": "observado", "pasajeros": s.values,
                         "p10": np.nan, "p90": np.nan})
    fut = pd.DataFrame({
        "periodo": futuro.date, "tipo": "pronostico",
        "pasajeros": np.exp(fit.forecast(horizonte)).values.round(0),
        "p10": np.percentile(sims, 10, axis=1).round(0),
        "p90": np.percentile(sims, 90, axis=1).round(0),
    })
    return pd.concat([hist, fut], ignore_index=True)


def red(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """PageRank de la red de cabotaje (tramos reconstruidos) por año."""
    edges = con.execute("""
        SELECT anio, origen, destino, count(*) AS tramos
        FROM fct_tramo GROUP BY ALL
    """).df()
    filas = []
    for anio, e in edges.groupby("anio"):
        g = nx.DiGraph()
        for r in e.itertuples():
            g.add_edge(r.origen, r.destino, weight=r.tramos)
        pr = nx.pagerank(g, weight="weight")
        for codigo, valor in pr.items():
            filas.append({
                "anio": int(anio), "codigo": codigo, "pagerank": round(valor, 6),
                "destinos_directos": g.out_degree(codigo),
                "tramos_salientes": int(g.out_degree(codigo, weight="weight")),
            })
    out = pd.DataFrame(filas)
    if out.empty:
        return out
    out["ranking"] = out.groupby("anio")["pagerank"].rank(ascending=False, method="min").astype(int)
    nombres = con.execute("SELECT codigo, ciudad, nombre FROM dim_aeropuerto").df()
    foco = con.execute("SELECT getvariable('foco')").fetchall()[0][0]
    out = out.merge(nombres, on="codigo", how="left")
    out["es_foco"] = out["codigo"] == foco
    return out.sort_values(["anio", "ranking"])


def build(db_path: Path = BD, out: Path = MARTS) -> list[Path]:
    con = bd.connect(db_path, read_only=True)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for nombre, fn in {
        "mart_mdq_tendencia": lambda c: tendencia(c, out),
        "mart_mdq_pronostico": pronostico,
        "mart_red_aeropuertos": red,
    }.items():
        df = fn(con)
        dest = out / f"{nombre}.parquet"
        duckdb.from_df(df).write_parquet(str(dest)) if len(df) else _vacio(df, dest)
        written.append(dest)
    con.close()
    return written


def _vacio(df: pd.DataFrame, dest: Path) -> None:
    duckdb.sql("SELECT 1 AS sin_datos WHERE false").write_parquet(str(dest))
