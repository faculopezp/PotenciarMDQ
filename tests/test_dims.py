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


@pytest.mark.parametrize(
    "codigo,modelo,icao,biplaza",
    [
        # 737: código de cliente = NG; "737-8" pelado o con MAX = MAX 8 (verificado por matrícula)
        ("BO-737-800", "Boeing 737-800", "B738", False),
        ("BO-B737-800", "Boeing 737-800", "B738", False),
        ("BO-737-8SH", "Boeing 737-800", "B738", False),
        ("BO-B737-8MB", "Boeing 737-800", "B738", False),
        ("BO-737-8", "Boeing 737 MAX 8", "B38M", False),
        ("BO-B737-8", "Boeing 737 MAX 8", "B38M", False),
        ("BO-737-8 MAX", "Boeing 737 MAX 8", "B38M", False),
        ("BO-B737-8MAX", "Boeing 737 MAX 8", "B38M", False),
        ("BO-B-737-76N", "Boeing 737-700", "B737", False),
        ("BO-737-7BD", "Boeing 737-700", "B737", False),
        # colisiones detectadas al revisar las 911 denominaciones
        ("BE-1900D", "Beechcraft 1900D", "B190", False),
        ("EUR-EC-145", "Airbus/MBB BK117/H145", None, False),
        ("MAX-MH-1521", "Otra", None, False),
        ("EMB-ERJ190100IGW", "Embraer E190", "E190", False),
        ("BE-B-200-GT", "Beechcraft King Air B200GT", "BE20", False),
        ("CE-150-M", "Cessna 150", "C150", True),
        ("TEA-P2002 SIERRA", "Tecnam P2002 Sierra", None, True),
        ("PA-PA-34-200-T", "Piper PA-34 Seneca", "PA34", False),
        ("PA-PA-31-T", "Piper Cheyenne (PA-31T/42)", None, False),
    ],
)
def test_modelo_aeronave(codigo, modelo, icao, biplaza):
    from potenciar_mdq.dims import modelo_aeronave

    cfg = load_yaml("aeronaves.yaml")
    _, familia, _ = classify_aeronave(codigo, cfg)
    assert modelo_aeronave(codigo, cfg, familia) == (modelo, icao, biplaza)


@pytest.mark.parametrize(
    "codigo,esperado",
    [
        ("PI-PC-24", ("Pilatus PC-24", "jet_ejecutivo")),
        ("PA-PA-31-T", ("Piper Cheyenne", "turbohelice_ejecutivo")),
        ("PA-PA-46-500TP", ("Piper M500/M600", "turbohelice_ejecutivo")),
        ("GU-GA-7", ("Grumman American", "aviacion_general_piston")),
        ("CIR-SF50", ("Cirrus Vision Jet", "jet_ejecutivo")),
    ],
)
def test_correcciones_clasificacion(codigo, esperado):
    _, familia, categoria = classify_aeronave(codigo, load_yaml("aeronaves.yaml"))
    assert (familia, categoria) == esperado
