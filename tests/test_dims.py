import pytest

from potenciar_mdq.dims import classify_aerolinea, classify_aeronave
from potenciar_mdq.settings import load_yaml

# Códigos reales de ANAC 2023–2026.
CASOS_AERONAVE = {
    "EMB-ERJ190100IGW": ("Embraer E190", "jet_regional"),
    "BO-737-8Q8": ("Boeing 737", "jet_fuselaje_angosto"),
    "BO-B-737-76N": ("Boeing 737", "jet_fuselaje_angosto"),
    "AIB-A320-232": ("Airbus A320", "jet_fuselaje_angosto"),
    "AIB-A330-202": ("Airbus A330", "jet_fuselaje_ancho"),
    "BE-1900D": ("Beech 1900", "turbohelice_regional"),
    "LJ-60": ("Learjet", "jet_ejecutivo"),
    "BE-C-90-A": ("Beech King Air", "turbohelice_ejecutivo"),
    "CE-C-152": ("Cessna (pistón)", "aviacion_general_piston"),
    "CIR-SR-22": ("Cirrus", "aviacion_general_piston"),
    "AIR-AT-802": ("Air Tractor", "agricola"),
    "RO-R44": ("Robinson", "helicoptero"),
}


@pytest.mark.parametrize("codigo,esperado", CASOS_AERONAVE.items())
def test_classify_aeronave(codigo, esperado):
    _, familia, categoria = classify_aeronave(codigo, load_yaml("aeronaves.yaml"))
    assert (familia, categoria) == esperado


@pytest.mark.parametrize(
    "nombre,esperado",
    [
        ("AEROLINEAS ARGENTINAS SA", ("Aerolíneas Argentinas", "bandera")),
        ("FB LÍNEAS AÉREAS - FLYBONDI", ("Flybondi", "low_cost")),
        ("JETSMART AIRLINES S.A.", ("JetSMART", "low_cost")),
        ("COMPAÑIA PANAMEÑA DE AVIACION", ("Copa Airlines", "extranjera")),
        ("TENIL S.A.", ("Tenil S.A.", "otra")),
    ],
)
def test_classify_aerolinea(nombre, esperado):
    assert classify_aerolinea(nombre, load_yaml("aerolineas.yaml")["aerolineas"]) == esperado


def test_perfil_aeronave_basico_taxi():
    import duckdb

    from potenciar_mdq import bd
    from potenciar_mdq.settings import SQL

    con = duckdb.connect()
    bd.set_variables(con)
    filas = (
        [("Beech King Air", "turbohelice_ejecutivo", False, 7)] * 40      # 5+ pax: básico
        + [("Daher TBM", "turbohelice_ejecutivo", False, 3)] * 40         # < 5 pax
        + [("Cessna (pistón)", "aviacion_general_piston", False, 3)] * 40
        + [("Learjet", "jet_ejecutivo", False, 6)] * 40
        + [("Boeing 737", "jet_fuselaje_angosto", True, 150)] * 40
    )
    con.execute("CREATE TABLE fct_movimiento (aeronave_familia VARCHAR, aeronave_categoria VARCHAR,"
                " es_linea BOOLEAN, pasajeros INT)")
    con.executemany("INSERT INTO fct_movimiento VALUES (?, ?, ?, ?)", filas)
    con.execute((SQL / "bd" / "70_dim_perfil.sql").read_text())
    perfil = dict(con.execute("SELECT aeronave_familia, perfil FROM dim_perfil_familia").fetchall())
    assert perfil == {
        "Beech King Air": "turbohelice_basico",
        "Daher TBM": "turbohelice_chico",
        "Cessna (pistón)": "piston",
        "Learjet": "jet_ejecutivo",
        "Boeing 737": "avion_de_linea",
    }
