"""Estandarización liviana: slug de columnas y CSV -> parquet (Yvera, OurAirports).

El esquema canónico de Yvera se fija cuando se vean las columnas reales (docs/04).
"""

from __future__ import annotations

import csv
import io
import json
import logging
import re
from datetime import datetime
from pathlib import Path

import duckdb

from potenciar_mdq.settings import INTERIM, PROCESSED, RAW
from potenciar_mdq.standardize.anac_movimientos import _ident, _latest_per_resource, _q, ensure_utf8
from potenciar_mdq.standardize.columns import slug

log = logging.getLogger(__name__)


def csv_to_parquet(src: Path, dest: Path) -> Path:
    con = duckdb.connect()
    utf8 = ensure_utf8(src)
    rel = f"read_csv({_q(str(utf8))}, header=true, sample_size=-1)"
    cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM {rel}").fetchall()]
    renamed = ", ".join(f"{_ident(c)} AS {_ident(slug(c))}" for c in cols)
    dest.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY (SELECT {renamed} FROM {rel}) TO {_q(str(dest))} (FORMAT parquet)")
    return dest


def build_yvera(raw_dir: Path = RAW / "yvera_conectividad") -> list[Path]:
    files = [p for p in raw_dir.rglob("*") if p.suffix.lower() == ".csv"]
    out = []
    for p in _latest_per_resource(files):
        name = slug(p.stem.split("_", 1)[-1])  # quita el prefijo de fecha
        out.append(csv_to_parquet(p, PROCESSED / f"yvera_{name}.parquet"))
    return out


def build_terrestre(raw_dir: Path = RAW / "yvera_terrestre", out: Path = PROCESSED) -> list[Path]:
    """Yvera "Conectividad terrestre interurbana" (CNRT): cada CSV -> terrestre_<recurso>.parquet.

    Los zip se abren y se convierte cada CSV de adentro (la base agregada de micros viene así).
    """
    import zipfile

    files = [p for p in raw_dir.rglob("*") if p.suffix.lower() in (".csv", ".zip")]
    escritos = []
    for p in _latest_per_resource(files):
        name = slug(p.stem.split("_", 1)[-1])
        if p.suffix.lower() == ".csv":
            escritos.append(csv_to_parquet(p, out / f"terrestre_{name}.parquet"))
            continue
        tmp = INTERIM / "terrestre" / name
        with zipfile.ZipFile(p) as z:
            miembros = [m for m in z.namelist() if m.lower().endswith(".csv")]
            for m in miembros:
                z.extract(m, tmp)
                sub = name if len(miembros) == 1 else f"{name}_{slug(Path(m).stem)}"
                escritos.append(csv_to_parquet(tmp / m, out / f"terrestre_{sub}.parquet"))
    if not escritos:
        raise FileNotFoundError(f"No hay CSV de conectividad terrestre en {raw_dir}")
    return escritos


def build_dim_aeropuerto(raw_dir: Path = RAW / "ourairports") -> Path:
    files = sorted(raw_dir.glob("*airports.csv"))
    if not files:
        raise FileNotFoundError(f"No hay airports.csv en {raw_dir}")
    return csv_to_parquet(files[-1], PROCESSED / "dim_aeropuerto.parquet")


def build_clima(raw_dir: Path = RAW / "clima_mdq") -> Path:
    """Open-Meteo (JSON diario) -> processed/clima_diario.parquet."""
    files = sorted(raw_dir.glob("*"))
    if not files:
        raise FileNotFoundError(f"No hay datos de clima en {raw_dir}")
    src = files[-1]
    dest = PROCESSED / "clima_diario.parquet"
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
          SELECT CAST(unnest(daily.time) AS DATE)           AS fecha,
                 unnest(daily.weather_code)::INT            AS codigo_tiempo,
                 unnest(daily.precipitation_sum)            AS precipitacion_mm,
                 unnest(daily.wind_speed_10m_max)           AS viento_max_kmh,
                 unnest(daily.wind_gusts_10m_max)           AS rafaga_max_kmh,
                 unnest(daily.temperature_2m_max)           AS temp_max_c
          FROM read_json({_q(str(src))})
        ) TO {_q(str(dest))} (FORMAT parquet)
        """
    )
    return dest


_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_HEMI = re.compile(r"([NSEOW])\s*$", re.I)


def coordenada(texto: str | None, negativa_por_defecto: bool = True) -> float | None:
    """'-34.5594' / '-34,5594' / '34°33'32"S' / '34 33 32 S' -> grados decimales.

    Sin hemisferio explícito en DMS se asume S/O (todo el listado ANAC está en el hemisferio
    sur y al oeste de Greenwich).
    """
    if texto is None:
        return None
    t = str(texto).strip()
    if not t:
        return None
    try:
        return float(t.replace(",", "."))
    except ValueError:
        pass
    nums = [float(n.replace(",", ".")) for n in _NUM.findall(t)][:3]
    if not nums:
        return None
    val = sum(n / 60**i for i, n in enumerate(nums))
    hemi = _HEMI.search(t)
    neg = hemi.group(1).upper() in ("S", "W", "O") if hemi else negativa_por_defecto
    return -val if neg else val


def build_anac_aeropuertos(raw_dir: Path = RAW / "anac_aeropuertos", out: Path = PROCESSED) -> Path:
    """Lista oficial ANAC -> processed/anac_aeropuertos.parquet (código, OACI, IATA, lat, lon)."""
    files = sorted(p for p in raw_dir.rglob("*") if p.is_file())
    if not files:
        raise FileNotFoundError(f"No hay lista de aeropuertos ANAC en {raw_dir}")
    src = files[-1]
    raw = src.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    first = text.splitlines()[0]
    sep = max((";", ",", "\t"), key=first.count)
    filas = list(csv.DictReader(io.StringIO(text), delimiter=sep))
    if not filas:
        raise ValueError(f"{src.name}: vacío")
    cols = {slug(c): c for c in filas[0]}

    def col(*nombres: str) -> str | None:
        return next((cols[n] for n in nombres if n in cols), None)

    c_local, c_oaci, c_iata = (
        col("local", "codigo_local", "cod_local"),
        col("oaci", "icao"),
        col("iata"),
    )
    c_nombre, c_tipo = col("denominacion", "nombre"), col("tipo")
    c_lat, c_lon, c_coord = col("latitud", "lat"), col("longitud", "lon"), col("coordenadas")
    c_prov = col("provincia")
    if not c_local:
        raise ValueError(f"{src.name}: sin columna de código local ({list(cols)})")

    registros = []
    for f in filas:
        # "coordenadas" (DMS con hemisferio) es la fuente principal: en el archivo real las
        # columnas latitud/longitud vienen invertidas (verificado 2026-10-24, ver docs/02).
        lat = lon = None
        if c_coord and f.get(c_coord):
            partes = re.split(r"(?<=[NSEOW])\s*[,;]?\s*|\s*[,;]\s*", f[c_coord].strip(), maxsplit=1)
            if len(partes) == 2:
                lat, lon = coordenada(partes[0]), coordenada(partes[1])
        if (lat is None or lon is None) and c_lat and c_lon:
            lat, lon = coordenada(f.get(c_lat)), coordenada(f.get(c_lon))
            # Invertidas: "lat" con valor de longitud continental (-53,5 a -75) y "lon" con una
            # latitud continental (-21 a -56). Solo respaldo: el DMS de "coordenadas" manda.
            if lat is not None and lon is not None and -75 <= lat <= -53.5 and -56 <= lon <= -21:
                lat, lon = lon, lat
        if lat is not None and not (-91 < lat < 0) or lon is not None and not (-180 < lon < 0):
            lat = lon = None  # fuera de Argentina/Antártida: dato roto
        codigo = (f.get(c_local) or "").strip().upper()
        if not codigo:
            continue
        registros.append(
            {
                "codigo": codigo,
                "oaci": (f.get(c_oaci) or "").strip().upper() or None if c_oaci else None,
                "iata": (f.get(c_iata) or "").strip().upper() or None if c_iata else None,
                "nombre": (f.get(c_nombre) or "").strip() or None if c_nombre else None,
                "tipo": (f.get(c_tipo) or "").strip() or None if c_tipo else None,
                "provincia": (f.get(c_prov) or "").strip() or None if c_prov else None,
                "lat": lat,
                "lon": lon,
                "archivo": src.name,
            }
        )
    dest = out / "anac_aeropuertos.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE a (codigo VARCHAR, oaci VARCHAR, iata VARCHAR, nombre VARCHAR, "
        "tipo VARCHAR, provincia VARCHAR, lat DOUBLE, lon DOUBLE, archivo VARCHAR)"
    )
    con.executemany(
        "INSERT INTO a VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [list(r.values()) for r in registros]
    )
    con.execute(
        f"COPY (SELECT * FROM a QUALIFY row_number() OVER (PARTITION BY codigo) = 1) "
        f"TO {_q(str(dest))} (FORMAT parquet)"
    )
    sin = sum(r["lat"] is None for r in registros)
    log.info("anac_aeropuertos: %d códigos, %d sin coordenadas", len(registros), sin)
    return dest


def build_opensky(raw_dir: Path = RAW / "opensky_aeronaves", out: Path = PROCESSED) -> Path:
    """OpenSky aircraftDatabase.csv -> processed/opensky.parquet (solo matrículas LV-/LQ-)."""
    files = sorted(p for p in raw_dir.rglob("*") if p.is_file())
    if not files:
        raise FileNotFoundError(f"No hay base de OpenSky en {raw_dir}")
    dest = out / "opensky.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    duckdb.connect().execute(f"""
        COPY (
          SELECT DISTINCT upper(trim(registration)) AS registration,
                 upper(trim(typecode)) AS typecode, manufacturername, model
          FROM read_csv({_q(str(files[-1]))}, all_varchar=true, header=true, ignore_errors=true)
          WHERE regexp_matches(upper(trim(registration)), '^L[VQ]-')
        ) TO {_q(str(dest))} (FORMAT parquet)""")
    return dest


def build_tar1090(raw_dir: Path = RAW / "tar1090_db", out: Path = PROCESSED) -> Path:
    """tar1090-db aircraft.csv.gz (hex;matrícula;tipo;flags;descripción) -> tar1090.parquet.

    Solo el bloque de direcciones de Argentina (E00000–E3FFFF) y matrículas LV-/LQ-. `ident` es la
    matrícula sin guiones (T-99 = T99), como se compara con ANAC.
    """
    files = sorted(p for p in raw_dir.rglob("*.csv.gz") if p.is_file())
    if not files:
        raise FileNotFoundError(f"No hay tar1090-db en {raw_dir}")
    dest = out / "tar1090.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    duckdb.connect().execute(f"""
        COPY (
          SELECT upper(column0) AS hex, upper(trim(column1)) AS matricula,
                 upper(regexp_replace(trim(column1), '[- ]', '', 'g')) AS ident,
                 upper(trim(column2)) AS tipo_icao, column3 AS flags, trim(column4) AS descripcion
          FROM read_csv({_q(str(files[-1]))}, delim=';', header=false, all_varchar=true,
                        ignore_errors=true, null_padding=true)
          WHERE coalesce(trim(column1), '') <> '' AND coalesce(trim(column2), '') <> ''
            AND (upper(column0) BETWEEN 'E00000' AND 'E3FFFF'
                 OR regexp_matches(upper(trim(column1)), '^L[VQ]-'))
        ) TO {_q(str(dest))} (FORMAT parquet)""")
    return dest


def build_madhel(raw_dir: Path = RAW / "madhel_api", out: Path = PROCESSED) -> Path:
    """MADHEL /api/v2/airports/ (JSON) -> processed/madhel.parquet, columnas tal cual vengan."""
    files = sorted(p for p in raw_dir.rglob("*") if p.is_file())
    if not files:
        raise FileNotFoundError(f"No hay respuesta de MADHEL en {raw_dir}")
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    if isinstance(data, dict):  # paginado o envuelto: {"results": [...]} / {"data": [...]}
        data = next((v for v in data.values() if isinstance(v, list)), [data])
    tmp = out / "madhel.jsonl"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in data), encoding="utf-8")
    dest = out / "madhel.parquet"
    duckdb.connect().execute(
        f"COPY (SELECT * FROM read_json_auto({_q(str(tmp))}, format='newline_delimited', "
        f"sample_size=-1)) TO {_q(str(dest))} (FORMAT parquet)"
    )
    log.info("madhel: %d registros", len(data))
    return dest


MESES_ES = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
     "octubre", "noviembre", "diciembre"], start=1)}


def build_tren(raw_dir: Path = RAW / "cnrt_ferroviario", out: Path = PROCESSED) -> Path:
    """CNRT, pasajeros pagos de larga distancia, regionales y turísticos (xlsx, hoja DATOS):
    una fila por año, mes y servicio -> processed/tren_pasajeros.parquet."""
    import openpyxl

    files = sorted(p for p in raw_dir.rglob("*") if p.suffix.lower() == ".xlsx")
    if not files:
        raise FileNotFoundError(f"No hay planillas de la CNRT en {raw_dir}")
    src = max(files, key=lambda p: p.name)
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    filas = []
    for fila in wb["DATOS"].iter_rows(min_row=2, max_col=8, values_only=True):
        anio, mes, linea, operador, tipo, jurisdiccion, servicio, pax = fila
        # Año y PAX pueden venir como número o como texto ("2007", "2007.0", "28.062").
        anio_txt = str(anio).strip().removesuffix(".0")
        mes_txt = str(mes).strip().lower()
        if not re.fullmatch(r"\d{4}", anio_txt) or mes_txt not in MESES_ES or not servicio:
            continue
        pax_txt = re.sub(r"[^\d]", "", str(pax).split(",")[0].removesuffix(".0")) if pax else ""
        filas.append((int(anio_txt), MESES_ES[mes_txt], linea, operador, tipo, jurisdiccion,
                      str(servicio).strip(), int(pax_txt) if pax_txt else None))
    if not filas:
        raise ValueError(f"{src.name}: la hoja DATOS no trae filas año/mes/servicio")
    con = duckdb.connect()
    con.execute("CREATE TABLE t (anio INT, mes INT, linea VARCHAR, operador VARCHAR, "
                "tipo_servicio VARCHAR, jurisdiccion VARCHAR, servicio VARCHAR, pax INT)")
    con.executemany("INSERT INTO t VALUES (?, ?, ?, ?, ?, ?, ?, ?)", filas)
    dest = out / "tren_pasajeros.parquet"
    con.execute(f"COPY (SELECT *, {_q(src.name)} AS archivo FROM t) TO {_q(str(dest))} "
                "(FORMAT parquet)")
    return dest


def build_evyth(raw_dir: Path = RAW / "yvera_evyth", out: Path = PROCESSED) -> list[Path]:
    """EVyTH (Yvera): viajes de residentes con destino Mar del Plata -> evyth_mdq.parquet, más el
    diccionario de códigos -> evyth_diccionario.parquet. Una fila por visitante y viaje; pondera
    es el factor de expansión."""
    csvs = _latest_per_resource([p for p in raw_dir.rglob("*.csv")])
    micro = [p for p in csvs if "microdatos" in p.name]
    dicc = [p for p in csvs if "diccionario" in p.name]
    if not micro:
        raise FileNotFoundError(f"No hay microdatos de la EVyTH en {raw_dir}")
    con = duckdb.connect()
    rel = f"read_csv({_q(str(ensure_utf8(micro[-1])))}, header=true, all_varchar=true)"
    dest = out / "evyth_mdq.parquet"
    con.execute(f"""
        COPY (
          SELECT TRY_CAST(anio AS INT) AS anio, TRY_CAST(trimestre AS INT) AS trimestre,
                 region_origen, tipo_visitante, px09, px07, px08_agrup, px10_1,
                 TRY_CAST(replace(pondera, ',', '.') AS DOUBLE) AS pondera,
                 trim(localidad_destino) AS localidad_destino, provincia_destino
          FROM {rel}
          WHERE lower(strip_accents(trim(localidad_destino))) = 'mar del plata'
        ) TO {_q(str(dest))} (FORMAT parquet)""")
    escritos = [dest]
    if dicc:
        d = out / "evyth_diccionario.parquet"
        con.execute(f"""COPY (SELECT * FROM read_csv({_q(str(ensure_utf8(dicc[-1])))},
                        header=true, all_varchar=true)) TO {_q(str(d))} (FORMAT parquet)""")
        escritos.append(d)
    return escritos


CANCELADOS = {"cancelado", "no opera"}


def hora_aa2000(texto: str | None, referencia: datetime) -> datetime | None:
    """'DD/MM HH:MM' (hora local, sin año) -> datetime, con el año de la fecha de referencia y
    corrigiendo el cruce de año (vuelo del 31/12 informado el 1/1 o al revés)."""
    m = re.fullmatch(r"(\d{2})/(\d{2}) (\d{2}):(\d{2})", (texto or "").strip())
    if not m:
        return None
    dia, mes, hh, mm = map(int, m.groups())
    anio = referencia.year
    if mes == 1 and referencia.month == 12:
        anio += 1
    elif mes == 12 and referencia.month == 1:
        anio -= 1
    try:
        return datetime(anio, mes, dia, hh, mm)
    except ValueError:
        return None


def build_failbondi(raw_dir: Path = RAW / "failbondi", out: Path = PROCESSED) -> Path:
    """failbondi.fail (estado de vuelos de AA2000, foco) -> processed/vuelos_aa2000.parquet.

    El programado (stda) y el real (atda) vienen como 'DD/MM HH:MM' sin año: el año sale de la fecha
    del vuelo (x_date), no de la fecha de actualización (así el sitio fecha mal los vuelos que
    cruzan el año)."""
    files = sorted(raw_dir.glob("*_dump.jsonl"))
    if not files:
        raise FileNotFoundError(f"No hay dumps de failbondi en {raw_dir}")
    filas = []
    for linea in files[-1].read_text(encoding="utf-8").splitlines():
        o = json.loads(linea)
        j = o.get("json") or {}
        try:
            fecha = datetime.strptime(str(j.get("x_date"))[:10], "%Y-%m-%d")
        except ValueError:
            continue
        prog = hora_aa2000(j.get("stda"), fecha)
        real = hora_aa2000(j.get("atda"), prog or fecha)
        estado = (j.get("estes") or "").strip()
        cancelado = estado.lower() in CANCELADOS
        operado = prog and real and not cancelado
        demora = round((real - prog).total_seconds() / 60) if operado else None
        pax = str(j.get("pasajeros") or "").strip()
        filas.append((
            o.get("aerolineas_flight_id"), fecha.date(), j.get("arpt"),
            "salida" if j.get("mov") == "D" else "llegada" if j.get("mov") == "A" else j.get("mov"),
            (j.get("aerolinea") or "").strip(), (j.get("nro") or "").strip(),
            (j.get("IATAdestorig") or "").strip(), prog, real, demora, estado, cancelado,
            int(pax) if pax.isdigit() else None, (j.get("matricula") or "").strip() or None,
            (j.get("idshared") or "").strip() or None, o.get("last_updated"),
        ))
    con = duckdb.connect()
    con.execute("""CREATE TABLE t (flight_id VARCHAR, fecha DATE, aeropuerto VARCHAR,
        movimiento VARCHAR, aerolinea VARCHAR, nro VARCHAR, otro_extremo VARCHAR,
        programado TIMESTAMP, real TIMESTAMP, demora_min INT, estado VARCHAR, cancelado BOOLEAN,
        pasajeros INT, matricula VARCHAR, idshared VARCHAR, actualizado VARCHAR)""")
    con.executemany("INSERT INTO t VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", filas)
    dest = out / "vuelos_aa2000.parquet"
    con.execute(f"COPY (SELECT *, {_q(files[-1].name)} AS archivo FROM t) TO {_q(str(dest))} "
                "(FORMAT parquet)")
    return dest
