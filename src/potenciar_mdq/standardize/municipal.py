"""Portal de datos de Mar del Plata (DKAN): planillas anchas -> una tabla larga.

processed/mun_series.parquet: dataset, serie, anio, mes, valor, unidad, archivo
processed/mun_vuelos_hist.parquet: movimientos individuales 2015–2019 (sin pasajeros)

Problemas reales que se corrigen (ver docs/02):
- movimientos y vuelos por tramo 2019–2020 vienen multiplicados por 1000
- miles con coma entre comillas ("1,073") o con punto ("1.422.547"); decimales con punto o coma
- pasajeros por tramo: hasta 2020 cuentan ambos sentidos; desde 2021 un solo sentido (≈ la mitad)
- Latin-1, separador ";" o ","; "n/h", "-" y vacío = sin dato
"""

from __future__ import annotations

import csv
import io
import logging
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import duckdb

from potenciar_mdq.settings import DATA, PROCESSED, ROOT, load_yaml

log = logging.getLogger(__name__)

RAW_MUN = DATA / "municipal" / "raw"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_LARGOS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                "septiembre", "octubre", "noviembre", "diciembre"]
SIN_DATO = {"", "-", "n/h", "nh", "s/d", "sd"}


def _norm(text: str) -> str:
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()


def leer_tabla(path: Path) -> list[list[str]]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    text = text.lstrip("﻿")
    sep = ";" if text.splitlines()[0].count(";") >= text.splitlines()[0].count(",") else ","
    return [r for r in csv.reader(io.StringIO(text), delimiter=sep) if any(c.strip() for c in r)]


def entero(v: str) -> float | None:
    """'1.422.547' / '1,073' / '955' -> número. Miles con punto o coma."""
    v = v.strip().strip('"')
    if _norm(v) in SIN_DATO:
        return None
    v = v.replace(".", "").replace(",", "").replace(" ", "")
    return float(v) if re.fullmatch(r"-?\d+", v) else None


def decimal(v: str) -> float | None:
    """'6.3' / '6,3' -> 6.3 (valores chicos, sin separador de miles)."""
    v = v.strip()
    if _norm(v) in SIN_DATO:
        return None
    v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def mes_de(col: str) -> int | None:
    c = _norm(col)
    for i, (corto, largo) in enumerate(zip(MESES, MESES_LARGOS, strict=True)):
        if c == largo or c.startswith(corto):
            return i + 1
    return None


def anio_de_archivo(path: Path) -> int | None:
    m = re.findall(r"(19\d\d|20\d\d)", unquote(path.name))
    return int(m[-1]) if m else None


def filas_por_mes(path: Path, dataset: str, unidad: str, escala_max: float | None = None):
    """Planilla con filas = series y columnas = meses de un año (año en el nombre del archivo)."""
    tabla = leer_tabla(path)
    anio = anio_de_archivo(path)
    meses = [mes_de(c) for c in tabla[0][1:]]
    filas = []
    for r in tabla[1:]:
        serie = r[0].strip()
        for m, v in zip(meses, r[1:], strict=False):
            if m is None:
                continue
            val = entero(v)
            if val is not None:
                filas.append([dataset, serie, anio, m, val, unidad, path.name])
    if escala_max is not None:
        vmax = max((f[4] for f in filas), default=0)
        if vmax > escala_max:  # 2019–2020 vienen ×1000
            log.warning("%s: valores ×1000 (máx %s), se corrigen", path.name, vmax)
            for f in filas:
                f[4] = round(f[4] / 1000)
    return filas


def filas_mes_x_anio(path: Path, dataset: str, unidad: str, parse=entero):
    """Planilla con filas = meses y columnas = años."""
    tabla = leer_tabla(path)
    anios = [int(c) if re.fullmatch(r"\d{4}", c.strip()) else None for c in tabla[0][1:]]
    filas = []
    for r in tabla[1:]:
        m = mes_de(r[0])
        if m is None:
            continue
        for a, v in zip(anios, r[1:], strict=False):
            val = parse(v) if a else None
            if val is not None:
                filas.append([dataset, dataset, a, m, val, unidad, path.name])
    return filas


def filas_medio(path: Path):
    """Turistas por medio de transporte: filas = meses, columnas = medio (año en el nombre)."""
    tabla = leer_tabla(path)
    anio = anio_de_archivo(path)
    medios = [_norm(c) for c in tabla[0][1:]]
    filas = []
    for r in tabla[1:]:
        m = mes_de(r[0])
        if m is None:
            continue
        for medio, v in zip(medios, r[1:], strict=False):
            val = entero(v)
            if val is not None and medio:
                filas.append(["arribos_medio", medio, anio, m, val, "turistas", path.name])
    return filas


REGIONES = {  # encabezados de la planilla de procedencia (cambian entre años) -> región
    "ciudad de buenos aires": "CABA", "caba": "CABA",
    "gran bs as": "Conurbano", "gba": "Conurbano",
    "pcia bs as": "Resto de la provincia", "resto pba": "Resto de la provincia",
    "resto del pais": "Resto del país",
    "exterior": "Exterior", "extranjeros": "Exterior",
}


def filas_procedencia(path: Path):
    """Procedencia de turistas: filas = meses, columnas = región, en % (año en el nombre)."""
    tabla = leer_tabla(path)
    anio = anio_de_archivo(path)
    regiones = [REGIONES.get(_norm(c)) for c in tabla[0][1:]]
    filas = []
    for r in tabla[1:]:
        m = mes_de(r[0])
        if m is None:
            continue
        for region, v in zip(regiones, r[1:], strict=False):
            val = decimal(v.replace("%", ""))
            if region and val is not None:
                filas.append(["procedencia", region, anio, m, val, "porcentaje", path.name])
    return filas


def filas_findes(path: Path):
    """Visitantes por fin de semana largo: filas = años, columnas = feriado (mes = NULL)."""
    tabla = leer_tabla(path)
    filas = []
    for r in tabla[1:]:
        if not r[0].strip().isdigit():
            continue
        for feriado, v in zip(tabla[0][1:], r[1:], strict=False):
            val = entero(v)
            if val is not None and feriado.strip():
                filas.append(["findes_largos", feriado.strip(), int(r[0]), None, val, "visitantes",
                              path.name])
    return filas


def build_series(raw: Path = RAW_MUN, out: Path = PROCESSED) -> Path:
    filas: list[list] = []
    d = raw / "movimientos-del-aeropuerto-internacional-astor-piazzolla"
    for p in sorted(d.glob("*.csv")):
        filas += filas_por_mes(p, "movimientos", "movimientos", escala_max=50_000)
    d = raw / "vuelos-comerciales-vuelos-por-tramo"
    for p in sorted(d.glob("*.csv")):
        filas += filas_por_mes(p, "vuelos_tramo", "movimientos", escala_max=50_000)
    d = raw / "vuelos-comerciales-pasajeros-por-tramo"
    for p in sorted(d.glob("*.csv")):
        anio = anio_de_archivo(p)
        unidad = "pasajeros_ida_y_vuelta" if anio and anio <= 2020 else "pasajeros_un_sentido"
        filas += filas_por_mes(p, "pasajeros_tramo", unidad)
    d = raw / "pasajeros-del-aeropuerto-astor-piazzolla"
    for p in sorted(d.glob("*.csv")):
        filas += filas_por_mes(p, "pasajeros_miles", "miles_de_pasajeros")
    for p in sorted((raw / "arribos-de-turistas").glob("*.csv")):
        filas += filas_mes_x_anio(p, "arribos_turistas", "turistas")
    est = raw / "turismo-estable-estadía-promedio"
    estadia = sorted(est.glob("estadia*"), key=lambda p: anio_de_archivo(p) or 0)
    if estadia:  # el archivo más largo incluye a los anteriores
        filas += filas_mes_x_anio(estadia[-1], "estadia_promedio", "noches", parse=decimal)
    for p in sorted(est.glob("turistas-estables*")):
        filas += filas_mes_x_anio(p, "turistas_estables", "turistas")
    for p in sorted((raw / "turismo-en-fines-de-semana-largo").glob("*.csv")):
        filas += filas_findes(p)
    for p in sorted((raw / "arribo-de-turistas-por-medio-de-transporte").glob("*.csv")):
        filas += filas_medio(p)
    for p in sorted((raw / "procedencia-de-turistas").glob("*.csv")):
        filas += filas_procedencia(p)

    for f in filas:
        if f[0] in ("pasajeros_tramo", "vuelos_tramo"):
            f[1] = normalizar_ruta(f[1])
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE s (dataset VARCHAR, serie VARCHAR, anio INT, mes INT, valor DOUBLE, "
        "unidad VARCHAR, archivo VARCHAR)"
    )
    con.executemany("INSERT INTO s VALUES (?, ?, ?, ?, ?, ?, ?)", filas)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "mun_series.parquet"
    con.execute(f"COPY s TO '{dest}' (FORMAT parquet)")
    log.info("mun_series: %d filas", len(filas))
    return dest


def normalizar_ruta(texto: str) -> str:
    """'Córdoba - Mar del Plata' / 'Mar del Plata - Tucumán' -> código ANAC del otro extremo."""
    rutas = load_yaml("municipal.yaml")["rutas"]
    partes = [_norm(p) for p in re.split(r"\s+-\s+", texto)]
    otro = next((p for p in partes if "mar del plata" not in p), partes[0] if partes else "")
    for patron, codigo in rutas.items():
        if re.search(patron, otro):
            return codigo
    return texto.strip()


def build_vuelos_hist(raw: Path = RAW_MUN, out: Path = PROCESSED) -> Path:
    """Movimientos individuales 2015–2019. Trae ambas puntas: se queda con los de MDQ."""
    files = sorted((raw / "vuelos-del-aeropuerto-internacional-astor-piazzolla").glob("*.csv"))
    if not files:
        raise FileNotFoundError("No hay vuelos históricos municipales")
    src = files[-1]
    oaci = load_yaml("mdq.yaml")["foco"]["oaci"]
    dest = out / "mun_vuelos_hist.parquet"
    con = duckdb.connect()
    con.execute(f"""
        COPY (
          SELECT
            CAST(strptime("Fecha", '%d/%m/%Y') AS DATE)               AS fecha,
            try_cast("Hora" AS INT)                                    AS hora_local,
            lower(regexp_replace(strip_accents("Clase de Vuelo"), '[^A-Za-z0-9]+', '_', 'g'))
                                                                       AS clase_vuelo,
            lower(strip_accents("Tipo de Movimiento"))                 AS tipo_movimiento,
            CASE WHEN lower("Tipo de Movimiento") LIKE 'aterrizaje%' THEN "Origen OACI"
                 ELSE "Destino OACI" END                               AS origen_destino_oaci,
            upper(trim("Aerolinea Nombre"))                            AS aerolinea,
            upper(trim("Aeronave"))                                    AS aeronave,
            '{src.name}'                                               AS archivo
          FROM read_csv('{src}', all_varchar=true, header=true, encoding='latin-1')
          WHERE (lower("Tipo de Movimiento") LIKE 'aterrizaje%' AND "Destino OACI" = '{oaci}')
             OR (lower("Tipo de Movimiento") LIKE 'despegue%' AND "Origen OACI" = '{oaci}')
        ) TO '{dest}' (FORMAT parquet)
    """)
    return dest


def sincronizar(
    descargas: Path = DATA / "raw" / "mdp_portal_catalogo", raw: Path = RAW_MUN
) -> int:
    """Copia la última descarga de cada recurso a data/municipal/raw/<dataset>/ (en git)."""
    if not descargas.exists():
        return 0
    n = 0
    for recurso in (p for p in descargas.glob("*/*") if p.is_dir()):
        archivos = sorted(f for f in recurso.iterdir() if f.is_file() and f.stat().st_size < 20e6)
        if not archivos:
            continue
        ultimo = archivos[-1]
        destino = raw / recurso.parent.name / re.sub(r"^\d{8}_", "", ultimo.name)
        destino.parent.mkdir(parents=True, exist_ok=True)
        if not destino.exists() or destino.read_bytes() != ultimo.read_bytes():
            shutil.copyfile(ultimo, destino)
            n += 1
    return n


def build(raw: Path = RAW_MUN, out: Path = PROCESSED) -> list[Path]:
    log.info("municipal: %d archivos actualizados", sincronizar(raw=raw))
    if not raw.exists():
        raise FileNotFoundError(f"No hay fuentes municipales en {raw.relative_to(ROOT)}")
    return [build_series(raw, out), build_vuelos_hist(raw, out)]
