"""Resolución de códigos de aeropuerto: lista ANAC + OurAirports."""

from pathlib import Path

import duckdb
import pytest

from potenciar_mdq import bd
from potenciar_mdq.settings import SQL
from potenciar_mdq.standardize import generic


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("-34.5594", -34.5594),
        ("-34,5594", -34.5594),
        ("34°33'32\"S", -(34 + 33 / 60 + 32 / 3600)),
        ("58 24 58 O", -(58 + 24 / 60 + 58 / 3600)),
        ("12°30'N", 12.5),
        ("", None),
        (None, None),
    ],
)
def test_coordenada(texto, esperado):
    v = generic.coordenada(texto)
    assert v == pytest.approx(esperado) if esperado is not None else v is None


def test_lista_anac_csv(tmp_path: Path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "20261024_aeropuertos_detalle.csv").write_text(
        "local;oaci;iata;tipo;denominacion;coordenadas;latitud;longitud;provincia\n"
        "MDP;SAZM;MDQ;Aeródromo;MAR DEL PLATA;;-37,9342;-57,5733;BUENOS AIRES\n"
        "2278;;;Helipuerto;HELIPUERTO X;37°50'00\"S 57°30'00\"O;;;BUENOS AIRES\n"
        "999;;;Aeródromo;ROTO;;45,0;10,0;X\n",
        encoding="latin-1",
    )
    dest = generic.build_anac_aeropuertos(raw, tmp_path)
    rows = {r[0]: r for r in duckdb.sql(f"SELECT codigo, lat, lon FROM '{dest}'").fetchall()}
    assert rows["MDP"][1:] == pytest.approx((-37.9342, -57.5733))
    assert rows["2278"][1:] == pytest.approx((-(37 + 50 / 60), -57.5))  # desde "coordenadas"
    assert rows["999"][1:] == (None, None)  # fuera de rango


def test_dim_aeropuerto_resuelve_por_fuente():
    con = duckdb.connect()
    bd.set_variables(con)
    con.execute(f"CREATE TABLE ourairports ({bd.OURAIRPORTS_COLS})")
    con.execute("""INSERT INTO ourairports VALUES
        ('SAZM','medium_airport','Astor Piazzolla',-37.93,-57.57,'AR','AR-B',
         'Mar del Plata','SAZM','MDQ','MDP'),
        ('SPIM','large_airport','Jorge Chávez',-12.02,-77.11,
         'PE','PE-LIM','Lima','SPJC','LIM',NULL),
        ('SAWB','small_airport','Marambio',-64.24,-56.63,'AQ','AQ-U-A','Marambio','SAWB',NULL,'MBI'),
        ('KHNR','small_airport','Harlan',41.58,-95.34,'US','US-IA','Harlan','KHNR',NULL,'HNR')""")
    con.execute("""CREATE TABLE anac_aeropuertos AS SELECT * FROM (VALUES
        ('2278', NULL, NULL, 'HELIPUERTO X', 'Helipuerto', 'BUENOS AIRES', -37.8, -57.5, 'f'),
        ('HNR', NULL, NULL, 'AERÓDROMO ARG', 'Aeródromo', 'CHUBUT', -43.0, -65.0, 'f'),
        ('MDP', 'SAZM', 'MDQ', 'MAR DEL PLATA', 'Aeródromo', 'BUENOS AIRES', -37.95, -57.58, 'f')
      ) t(codigo, oaci, iata, nombre, tipo, provincia, lat, lon, archivo)""")
    con.execute((SQL / "bd" / "00_macros.sql").read_text())
    con.execute((SQL / "bd" / "10_dim_aeropuerto.sql").read_text())
    d = dict(con.execute("SELECT codigo, fuente_coord FROM dim_aeropuerto").fetchall())
    assert d["MDP"] == "ourairports_local"  # OurAirports AR gana si existe
    assert d["2278"] == "anac"  # numérico: solo en la lista ANAC
    assert d["HNR"] == "anac"  # código local AR, no el aeródromo de EE.UU.
    assert d["MBI"] == "ourairports_local"  # Antártida
    assert d["SPJC"] == "ourairports_oaci"  # OACI nuevo vía gps_code
    [(n, km)] = con.execute(
        "SELECT count(*), max(distancia_km) FROM ref_aeropuerto_cruce"
    ).fetchall()
    assert n == 1 and km < 5
