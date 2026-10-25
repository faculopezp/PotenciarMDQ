"""End-to-end sobre fixtures: raw -> stg -> BD -> marts."""

import shutil
from pathlib import Path

import duckdb
import pytest

from potenciar_mdq import bd, marts
from potenciar_mdq.standardize import anac_movimientos, generic

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def work(tmp_path_factory) -> Path:
    tmp = tmp_path_factory.mktemp("pmdq")
    raw = tmp / "raw" / "anac_movimientos"
    for i, name in enumerate(sorted(FIXTURES.glob("anac_*.csv"))):
        d = raw / f"recurso{i}"
        d.mkdir(parents=True)
        shutil.copy(name, d / f"20260101_{name.name}")
    processed = tmp / "processed"
    anac_movimientos.build(raw, processed, interim_dir=tmp / "interim")
    oa = FIXTURES / "ourairports_extracto.csv"
    generic.csv_to_parquet(oa, processed / "dim_aeropuerto.parquet")
    bd.build(processed, tmp / "bd.duckdb", export=None)
    marts.build(tmp / "bd.duckdb", tmp / "marts")
    return tmp


def q(work: Path, sql: str):
    con = duckdb.connect(str(work / "bd.duckdb"), read_only=True)
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()


def test_stg_parsea_formatos_reales(work: Path):
    con = duckdb.connect()
    rows = con.execute(
        f"""SELECT fecha, hora_utc, clasificacion_vuelo, aerolinea, aeronave, matricula,
                   pasajeros, pax_nacional, calidad_dato, clase_vuelo
            FROM '{work}/processed/stg_movimiento.parquet' ORDER BY fecha, hora_utc"""
    ).fetchall()
    assert len(rows) == 9
    first = rows[0]
    assert str(first[0]) == "2025-01-05" and str(first[1]) == "12:00:00"
    assert first[2] == "cabotaje"
    assert first[6:8] == (150, 75)          # "150,00" / "75,00" con coma decimal
    assert first[8] == "definitivo" and first[9] == "regular"
    privado = [r for r in rows if r[4] == "CE-150-M"][0]
    assert str(privado[1]) == "09:05:00"    # hora "9:05"
    assert privado[3] is None               # aerolínea "0" -> NULL
    assert rows[-1][6] is None              # pasajeros vacío -> NULL, no 0
    assert {r[5] for r in rows if r[5]} == {"LV-XXX", "LV-YYY", "LV-ZZZ"}


def test_correccion_aeropuerto_y_hora_local(work: Path):
    [(orig, fixed)] = q(work, "SELECT aeropuerto_original, aeropuerto FROM fct_movimiento "
                              "WHERE aeropuerto_corregido")
    assert (orig, fixed) == ("MDB", "MDP")
    [(ts, fecha, dia)] = q(work, "SELECT ts_local, fecha, dia_semana_nombre FROM fct_movimiento "
                                 "WHERE aeronave = 'AIB-A320-232'")
    assert str(ts) == "2026-01-15 22:15:00" and str(fecha) == "2026-01-15" and dia == "jue"


def test_enriquecimiento(work: Path):
    rows = dict(q(work, "SELECT aeronave, aeronave_categoria FROM fct_movimiento "
                        "GROUP BY ALL"))
    assert rows["BO-737-8"] == "jet_fuselaje_angosto"
    assert rows["EMB-ERJ190100IGW"] == "jet_regional"
    assert rows["CE-150-M"] == "aviacion_general_piston"
    [(km,)] = q(work, "SELECT DISTINCT distancia_km FROM fct_movimiento "
                      "WHERE aeropuerto = 'MDP' AND origen_destino = 'AER'")
    assert 370 < km < 390   # AEP–MDQ ≈ 380 km


def test_tramo_y_rotacion(work: Path):
    [(origen, destino, dur)] = q(work, "SELECT origen, destino, duracion_min FROM fct_tramo")
    assert (origen, destino, dur) == ("AER", "MDP", 44)
    [(minutos, tipo)] = q(work, "SELECT tiempo_en_tierra_min, tipo_rotacion FROM fct_rotacion")
    assert (minutos, tipo) == (56, "rotacion")


def test_marts_conservan_pasajeros(work: Path):
    con = duckdb.connect()
    total_mensual = con.execute(
        f"SELECT sum(pasajeros) FROM '{work}/marts/mart_mdq_mensual.parquet'"
    ).fetchall()[0][0]
    assert total_mensual == 150 + 140 + 1 + 60 + 34 + 80 + 170
    anual = con.execute(
        f"""SELECT anio, movimientos, movimientos_comerciales, hhi_aerolineas
            FROM '{work}/marts/mart_mdq_anual.parquet' ORDER BY anio"""
    ).fetchall()
    assert anual[0][:3] == (2025, 5, 4)    # el vuelo privado no es comercial
    diario = con.execute(
        f"SELECT count(*), sum(pasajeros) FROM '{work}/marts/mart_mdq_diario.parquet'"
    ).fetchall()[0]
    assert diario[1] == 150 + 140 + 60 + 34 + 80 + 170   # solo comerciales


def test_no_crea_anio_previo_por_huso_horario(work: Path):
    [(anio_min,)] = q(work, "SELECT min(anio) FROM fct_movimiento")
    assert anio_min == 2025


def test_segmentos(work: Path):
    segs = dict(q(work, "SELECT aeronave, any_value(segmento) FROM fct_movimiento GROUP BY 1"))
    assert segs["CE-150-M"] == "privado"
    assert segs["BO-737-8"] == "linea_regular"
    # no regular con A320 de un operador de línea -> charter de línea
    assert segs["AIB-A320-232"] == "charter_linea"


def test_muestras_y_modelo(work: Path):
    from potenciar_mdq import muestras

    dest = muestras.run(work / "bd.duckdb", work / "qa")
    texto = dest.read_text(encoding="utf-8")
    assert "## 1. Vuelos oficiales" in texto and "## 6. Validación contra OpenSky" in texto
    modelos = dict(q(work, "SELECT aeronave, aeronave_modelo FROM fct_movimiento "
                           "WHERE aeronave IS NOT NULL"))
    assert modelos["BO-737-8"] == "Boeing 737 MAX 8"


def test_auditoria(work: Path):
    from potenciar_mdq import auditoria

    texto = auditoria.run(work / "bd.duckdb", work / "qa").read_text(encoding="utf-8")
    assert "## 1. Completitud por año" in texto and "## 2C." in texto and "## 3." in texto
