"""Dimensiones de la BD que necesitan Python (regex de config, calendario de feriados)."""

from __future__ import annotations

import re
import unicodedata
from datetime import date, timedelta

import duckdb
import holidays

from potenciar_mdq.settings import load_yaml, mdq


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().upper().strip()


def classify_aeronave(name: str, cfg: dict) -> tuple[str, str, str]:
    """'BO-737-8Q8' -> ('Boeing', 'Boeing 737', 'jet_fuselaje_angosto')."""
    up = name.upper().strip()
    prefix = up.split("-", 1)[0]
    if prefix in cfg["fabricantes"]:
        fabricante = cfg["fabricantes"][prefix]
    elif " " in up:  # formato "EMBRAER E-190" del portal municipal
        fabricante = up.split()[0].title()
    else:
        fabricante = prefix
    for rule in cfg["categorias"]:
        if re.search(rule["patron"], up):
            familia = next(
                (fam for rx, fam in rule.get("familia_regex", {}).items() if re.search(rx, up)),
                f"{fabricante} (otro)",
            )
            return fabricante, familia, rule["categoria"]
    return fabricante, cfg["default"]["familia"], cfg["default"]["categoria"]


def modelo_aeronave(name: str, cfg: dict, familia: str) -> tuple[str, str | None, int | None]:
    """'BO-B737-8SH' -> ('Boeing 737-800', 'B738', None); 'CE-150-M' -> ('Cessna 150', 'C150', 2).

    Sin regla: (familia, None, None). plazas solo está cargado para pistón.
    """
    m = _regla_modelo(name, cfg)
    if m:
        return m["modelo"], (m.get("icao") or None), m.get("plazas")
    return familia, None, None


def _regla_modelo(name: str, cfg: dict) -> dict | None:
    up = name.upper().strip()
    return next((m for m in cfg.get("modelos", []) if re.search(m["patron"], up)), None)


_SIGLA = re.compile(r"\b[A-Z](?:\.\s?[A-Z])+\b\.?")          # L.A.D.E. / S.A / S. A. / S.R.L
_SOCIETARIO = {"SA", "SAS", "SRL", "LTDA", "LTD", "INC", "SAU", "SACI", "SAIC", "SACIF", "SE",
               "LIMITED", "LLC", "CORP", "SCA", "SAF"}
_VACIAS = {"DE", "DEL", "LA", "EL", "LOS", "LAS", "Y"}
_SUFIJO_RX = re.compile(
    r"[\s,.\-]*\b(S\.?\s?A\.?\s?S\.?|S\.?\s?A\.?\s?U\.?|S\.?\s?A\.?|S\.?\s?R\.?\s?L\.?|"
    r"LTDA\.?|LTD\.?|INC\.?|LIMITED|LLC)\s*$", re.I)


def clave_operador(name: str) -> str:
    """'L.A.D.E.' -> 'LADE'; 'HANGAR UNO S.A' / 'HANGAR UNO S.A.' -> 'HANGAR UNO'.

    Clave de agrupación: sin acentos, siglas con puntos colapsadas, sin forma societaria final ni
    artículos/preposiciones. Dos nombres con la misma clave son el mismo operador.
    """
    s = _norm(name)
    s = _SIGLA.sub(lambda m: re.sub(r"[.\s]", "", m.group(0)) + " ", s)
    tokens = re.sub(r"[^A-Z0-9]+", " ", s).split()
    while tokens and tokens[-1] in _SOCIETARIO:
        tokens.pop()
    return " ".join(t for t in tokens if t not in _VACIAS)


def nombre_visible(name: str) -> str:
    """'HANGAR UNO S.A.' -> 'Hangar Uno'; conserva acentos y artículos del original."""
    s = re.sub(r"\s+", " ", name).strip()
    prev = None
    while prev != s:
        prev, s = s, _SUFIJO_RX.sub("", s).strip()
    s = s.title() if s else name.title()
    return re.sub(r"\b(?=[MDCLXVI]+\b)M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b",
                  lambda m: m.group(0).upper(), s, flags=re.I)


def classify_aerolinea(name: str, rules: list[dict]) -> tuple[str, str]:
    n, k = _norm(name), clave_operador(name)
    for r in rules:
        if re.search(r["patron"], n) or re.search(r["patron"], k):
            return (r["nombre"] or nombre_visible(name)), r["tipo"]
    return nombre_visible(name), "otra"


def build_dim_aeronave(con: duckdb.DuckDBPyConnection) -> None:
    cfg = load_yaml("aeronaves.yaml")
    extra = (" UNION SELECT DISTINCT aeronave FROM mun_vuelos_hist WHERE aeronave IS NOT NULL"
             if _existe(con, "mun_vuelos_hist") else "")
    names = [r[0] for r in con.execute(
        "SELECT DISTINCT aeronave FROM stg_movimiento WHERE aeronave IS NOT NULL" + extra
    ).fetchall()]
    # Tipos que solo aparecen por recuperación (serie de matrícula estatal).
    names += sorted({s["aeronave"] for s in load_yaml("estatales.yaml")["series"]} - set(names))
    rows = []
    for n in names:
        fabricante, familia, categoria = classify_aeronave(n, cfg)
        regla = _regla_modelo(n, cfg)
        if categoria == cfg["default"]["categoria"] and regla and regla.get("categoria"):
            familia, categoria = regla.get("familia", regla["modelo"]), regla["categoria"]
        rows.append((n, fabricante, familia, categoria, *modelo_aeronave(n, cfg, familia)))
    con.execute(
        "CREATE OR REPLACE TABLE dim_aeronave "
        "(aeronave VARCHAR PRIMARY KEY, fabricante VARCHAR, familia VARCHAR, categoria VARCHAR, "
        "modelo VARCHAR, icao_tipo VARCHAR, plazas INT)"
    )
    if rows:
        con.executemany("INSERT INTO dim_aeronave VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    inferencia = cfg.get("inferencia", [])
    con.execute(
        "CREATE OR REPLACE TABLE ref_inferencia_aeronave (orden INT, operador VARCHAR, "
        "anio_hasta INT, pax_min DOUBLE, pax_max DOUBLE, familia VARCHAR, modelo VARCHAR, "
        "categoria VARCHAR, modelos_validos VARCHAR[])"
    )
    if inferencia:
        con.executemany(
            "INSERT INTO ref_inferencia_aeronave VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(i, r["operador"], r.get("anio_hasta", 2099), r["pax_min"], r["pax_max"],
              r["familia"], r.get("modelo", r["familia"]), r["categoria"],
              r.get("modelos_validos", []))
             for i, r in enumerate(inferencia)],
        )


def build_refs_recuperacion(con: duckdb.DuckDBPyConnection) -> None:
    """Tablas de config para la recuperación (sql/bd/25) y la capacidad (sql/bd/30):
    matrículas estatales (config/estatales.yaml) y cabinas publicadas (config/cabinas.yaml)."""
    est = load_yaml("estatales.yaml")
    con.execute("CREATE OR REPLACE TABLE ref_prefijo_estatal "
                "(orden INT, patron VARCHAR, operador VARCHAR, valida VARCHAR, base VARCHAR)")
    con.executemany("INSERT INTO ref_prefijo_estatal VALUES (?, ?, ?, ?, ?)",
                    [(i, p["patron"], p["operador"], p["valida"], p["base"])
                     for i, p in enumerate(est["prefijos"])])
    con.execute("CREATE OR REPLACE TABLE ref_serie_estatal "
                "(matricula VARCHAR, aeronave VARCHAR, desde DATE, fuente VARCHAR)")
    con.executemany("INSERT INTO ref_serie_estatal VALUES (?, ?, ?, ?)",
                    [(s["matricula"], s["aeronave"], s["desde"], s["fuente"])
                     for s in est["series"]])
    con.execute("CREATE OR REPLACE TABLE ref_cabina "
                "(orden INT, operador VARCHAR, modelo VARCHAR, asientos INT, clases VARCHAR, "
                "fuentes VARCHAR[])")
    con.executemany("INSERT INTO ref_cabina VALUES (?, ?, ?, ?, ?, ?)",
                    [(i, c.get("operador"), c["modelo"], c["asientos"], c.get("clases"),
                      c["fuentes"]) for i, c in enumerate(load_yaml("cabinas.yaml")["cabinas"])])


def _existe(con: duckdb.DuckDBPyConnection, tabla: str) -> bool:
    return bool(con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [tabla]
    ).fetchall()[0][0])


def build_dim_aerolinea(con: duckdb.DuckDBPyConnection) -> None:
    rules = load_yaml("aerolineas.yaml")["aerolineas"]
    extra = (" UNION ALL SELECT aerolinea FROM mun_vuelos_hist WHERE aerolinea IS NOT NULL"
             if _existe(con, "mun_vuelos_hist") else "")
    conteo = con.execute(
        "SELECT aerolinea, count(*) FROM (SELECT aerolinea FROM stg_movimiento "
        f"WHERE aerolinea IS NOT NULL{extra}) GROUP BY 1"
    ).fetchall()
    # Operadores que solo aparecen por recuperación (prefijo de matrícula estatal).
    vistos = {n for n, _ in conteo}
    estatales = {p["operador"] for p in load_yaml("estatales.yaml")["prefijos"]}
    conteo += [(n, 0) for n in sorted(estatales - vistos)]
    # Variantes del mismo operador (misma clave): todas toman el nombre y tipo de la más frecuente.
    grupos: dict[str, list[tuple[int, str]]] = {}
    for n, c in conteo:
        grupos.setdefault(clave_operador(n), []).append((c, n))
    rows = []
    for clave, variantes in grupos.items():
        nombre, tipo = classify_aerolinea(max(variantes)[1], rules)
        rows += [(n, nombre, tipo, clave, len(variantes)) for _, n in variantes]
    con.execute(
        "CREATE OR REPLACE TABLE dim_aerolinea "
        "(aerolinea VARCHAR PRIMARY KEY, aerolinea_nombre VARCHAR, aerolinea_tipo VARCHAR, "
        "aerolinea_clave VARCHAR, variantes_nombre INT)"
    )
    if rows:
        con.executemany("INSERT INTO dim_aerolinea VALUES (?, ?, ?, ?, ?)", rows)


def build_dim_fecha(con: duckdb.DuckDBPyConnection, desde: date, hasta: date) -> None:
    """Calendario con feriados nacionales (paquete `holidays`, incluye feriados puente)."""
    verano = set(mdq()["meses_verano"])
    feriados = holidays.country_holidays("AR", years=range(desde.year, hasta.year + 1))
    rows = []
    d = desde
    while d <= hasta:
        rows.append((d, feriados.get(d)))
        d += timedelta(days=1)
    con.execute("CREATE OR REPLACE TEMP TABLE _f (fecha DATE, feriado VARCHAR)")
    con.executemany("INSERT INTO _f VALUES (?, ?)", rows)
    meses = ", ".join(str(m) for m in sorted(verano))
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_fecha AS
        WITH b AS (
          SELECT fecha, feriado,
                 isodow(fecha) IN (6, 7) OR feriado IS NOT NULL AS es_no_laborable
          FROM _f
        ),
        bloques AS (   -- racha de días no laborables consecutivos (finde largo = racha >= 3)
          SELECT *, sum(CASE WHEN es_no_laborable THEN 0 ELSE 1 END) OVER (ORDER BY fecha) AS grp
          FROM b
        )
        SELECT
          fecha,
          year(fecha) AS anio, month(fecha) AS mes, day(fecha) AS dia,
          quarter(fecha) AS trimestre, weekofyear(fecha) AS semana_iso,
          isodow(fecha) AS dia_semana,
          ['lun','mar','mié','jue','vie','sáb','dom'][isodow(fecha)] AS dia_semana_nombre,
          isodow(fecha) IN (6, 7) AS es_fin_de_semana,
          feriado IS NOT NULL AS es_feriado,
          feriado AS feriado_nombre,
          es_no_laborable,
          es_no_laborable AND count(*) FILTER (es_no_laborable) OVER (PARTITION BY grp) >= 3
            AS es_finde_largo,
          month(fecha) IN ({meses}) AS es_temporada_verano,
          CASE WHEN month(fecha) IN ({meses})
               THEN year(fecha) + CASE WHEN month(fecha) >= 7 THEN 1 ELSE 0 END END
            AS verano_anio,
          month(fecha) = 7 AS es_julio   -- proxy de vacaciones de invierno (fechas varían por año)
        FROM bloques
        ORDER BY fecha
    """)
