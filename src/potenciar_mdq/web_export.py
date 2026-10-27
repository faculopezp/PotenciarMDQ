"""Exporta los marts y los hitos a web/src/data/*.json (archivos estáticos versionados).

La web (Observable Framework) se compila en Vercel solo con Node: no necesita Python ni la BD.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import duckdb

from potenciar_mdq.settings import MARTS, ROOT, load_yaml

WEB_DATA = ROOT / "web" / "src" / "data"

# mart -> nombre del archivo en la web
MARTS_WEB = {
    "mart_mdq_anual": "mdq_anual",
    "mart_mdq_mensual": "mdq_mensual",
    "mart_mdq_diario": "mdq_diario",
    "mart_mdq_hora_semana": "mdq_hora_semana",
    "mart_mdq_aerolineas": "mdq_aerolineas",
    "mart_mdq_aeronaves": "mdq_aeronaves",
    "mart_mdq_rutas": "mdq_rutas",
    "mart_mdq_destinos": "mdq_destinos",
    "mart_mdq_vuelos_exoticos": "mdq_vuelos_exoticos",
    "mart_mdq_verano": "mdq_verano",
    "mart_mdq_rotaciones": "mdq_rotaciones",
    "mart_mdq_tramos": "mdq_tramos",
    "mart_mdq_aviacion_general": "mdq_aviacion_general",
    "mart_benchmark_pares": "benchmark_pares",
    "mart_mdq_segmentos_mensual": "mdq_segmentos_mensual",
    "mart_mdq_segmentos_anual": "mdq_segmentos_anual",
    "mart_mdq_avion_tipico": "mdq_avion_tipico",
    "mart_mdq_perfil_aeronave": "mdq_perfil_aeronave",
    "mart_mdq_operadores": "mdq_operadores",
    "mart_ranking_nacional": "ranking_nacional",
    "mart_mdq_dias_atipicos": "mdq_dias_atipicos",
    "mart_mdq_tendencia": "mdq_tendencia",
    "mart_mdq_pronostico": "mdq_pronostico",
    "mart_red_aeropuertos": "red_aeropuertos",
    "mart_mdq_serie_larga": "mdq_serie_larga",
    "mart_mdq_turismo": "mdq_turismo",
    "mart_mdq_findes_largos": "mdq_findes_largos",
    "mart_mdq_historia_segmentos": "mdq_historia_segmentos",
    "mart_mdq_cobertura": "mdq_cobertura",
    "mart_bus_anual": "bus_anual",
    "mart_bus_rutas": "bus_rutas",
    "mart_bus_mensual": "bus_mensual",
    "mart_bus_origen_provincia": "bus_origen_provincia",
    "mart_tren_mensual": "tren_mensual",
    "mart_tren_anual": "tren_anual",
    "mart_tren_servicios": "tren_servicios",
    "mart_tren_operador": "tren_operador",
    "mart_evyth_medio": "evyth_medio",
    "mart_mdq_arribos_medio": "mdq_arribos_medio",
    "mart_evyth_origen": "evyth_origen",
}
COLUMNAR = {"mart_mdq_explorador": "mdq_explorador"}  # tablas grandes: {col: [valores]}


def _default(v):
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, date):
        return v.isoformat()
    if hasattr(v, "__float__"):
        f = float(v)
        return int(f) if f.is_integer() else f
    raise TypeError(type(v))


def _read(parquet: Path) -> tuple[list[str], list[tuple]]:
    con = duckdb.connect()
    rel = con.sql(f"SELECT * FROM read_parquet('{parquet}')")
    cols, rows = rel.columns, rel.fetchall()
    con.close()
    return cols, rows


def _round(v):
    return round(v, 4) if isinstance(v, float) else v


def export(marts: Path = MARTS, out: Path = WEB_DATA) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for mart, name in {**MARTS_WEB, **COLUMNAR}.items():
        cols, rows = _read(marts / f"{mart}.parquet")
        if mart in COLUMNAR:
            payload = {c: [_round(r[i]) for r in rows] for i, c in enumerate(cols)}
        else:
            payload = [{c: _round(v) for c, v in zip(cols, r, strict=True)} for r in rows]
        dest = out / f"{name}.json"
        dest.write_text(
            json.dumps(payload, default=_default, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        written.append(dest)
    for nombre, clave in (("hitos", "hitos"), ("eventos", "eventos"), ("cruceros", "cruceros"),
                          ("autos", "conteos")):
        filas = [{k: str(v) if k == "fecha" or isinstance(v, date) else v for k, v in h.items()}
                 for h in load_yaml(f"{nombre}.yaml")[clave]]
        dest = out / f"{nombre}.json"
        dest.write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
        written.append(dest)
    return written
