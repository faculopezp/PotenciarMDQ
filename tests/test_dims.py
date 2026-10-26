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
    "CE-C-152": ("Cessna", "aviacion_general_piston"),
    "CIR-SR-22": ("Cirrus", "aviacion_general_piston"),
    "AIR-AT-802": ("Air Tractor", "agricola"),
    "RO-R44": ("Robinson", "helicoptero"),
    # tipos de las series estatales (config/estatales.yaml)
    "EMB-ERJ-140LR": ("Embraer ERJ145", "jet_regional"),
    "EUR-AS-365-N2": ("Airbus Helicopters", "helicoptero"),
    "BOM-CL-600-2B19": ("Bombardier CRJ", "jet_regional"),     # CRJ200, no Challenger
    "BOM-CL-600-2B16": ("Bombardier Challenger", "jet_ejecutivo"),
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
        ("TENIL S.A.", ("Tenil", "otra")),
        ("L.A.D.E.", ("LADE", "estatal")),
        ("AVIANCA", ("Avianca", "extranjera")),
        ("AVIAN LINEAS AEREAS S.A.", ("Avian (Avianca Argentina)", "regional")),
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
        + [("Cessna", "aviacion_general_piston", False, 3)] * 40
        + [("Learjet", "jet_ejecutivo", False, 6)] * 40
        + [("Boeing 737", "jet_fuselaje_angosto", True, 150)] * 40
    )
    con.execute("CREATE TABLE fct_movimiento (aeronave_familia VARCHAR, aeronave_categoria VARCHAR,"
                " es_linea BOOLEAN, pasajeros INT)")
    con.executemany("INSERT INTO fct_movimiento VALUES (?, ?, ?, ?)", filas)
    con.execute((SQL / "bd" / "70_dim_perfil.sql").read_text())
    perfil = dict(con.execute("SELECT aeronave_familia, perfil FROM dim_perfil_familia").fetchall())
    assert perfil == {
        "Beech King Air": "turbohelice",
        "Daher TBM": "turbohelice",
        "Cessna": "piston",
        "Learjet": "jet_ejecutivo",
        "Boeing 737": "avion_de_linea",
    }


@pytest.mark.parametrize(
    "codigo,modelo,icao,plazas",
    [
        # 737: código de cliente = NG; "737-8" pelado o con MAX = MAX 8 (verificado por matrícula)
        ("BO-737-800", "Boeing 737-800", "B738", None),
        ("BO-B737-800", "Boeing 737-800", "B738", None),
        ("BO-737-8SH", "Boeing 737-800", "B738", None),
        ("BO-B737-8MB", "Boeing 737-800", "B738", None),
        ("BO-737-8", "Boeing 737 MAX 8", "B38M", None),
        ("BO-B737-8", "Boeing 737 MAX 8", "B38M", None),
        ("BO-737-8 MAX", "Boeing 737 MAX 8", "B38M", None),
        ("BO-B737-8MAX", "Boeing 737 MAX 8", "B38M", None),
        ("BO-B-737-76N", "Boeing 737-700", "B737", None),
        ("BO-737-7BD", "Boeing 737-700", "B737", None),
        # colisiones detectadas al revisar las 911 denominaciones
        ("BE-1900D", "Beechcraft 1900D", "B190", None),
        ("EUR-EC-145", "Airbus/MBB BK117/H145", None, None),
        ("MAX-MH-1521", "Max Holste MH.1521 Broussard", None, None),
        ("EMB-ERJ190100IGW", "Embraer E190", "E190", None),
        ("BE-B-200-GT", "Beechcraft King Air B200GT", "BE20", None),
        ("CE-150-M", "Cessna 150", "C150", 2),
        ("TEA-P2002 SIERRA", "Tecnam P2002 Sierra", None, 2),
        ("PA-PA-34-200-T", "Piper PA-34 Seneca", "PA34", 6),
        ("PA-PA-31-T", "Piper Cheyenne (PA-31T/42)", None, None),
        ("PAA-PA-A-31-T", "Piper Cheyenne (PA-31T/42)", None, None),
        ("BE-B-300", "Beechcraft King Air 350 (B300)", "B350", None),
        ("CIR-SR 22T", "Cirrus SR22T", "S22T", 5),
    ],
)
def test_modelo_aeronave(codigo, modelo, icao, plazas):
    from potenciar_mdq.dims import modelo_aeronave

    cfg = load_yaml("aeronaves.yaml")
    _, familia, _ = classify_aeronave(codigo, cfg)
    assert modelo_aeronave(codigo, cfg, familia) == (modelo, icao, plazas)


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


@pytest.mark.parametrize(
    "a,b",
    [
        ("LADE", "L.A.D.E."),
        ("HANGAR UNO S.A", "HANGAR UNO S.A."),
        ("BANCO SAFRA S.A.", "BANCO SAFRA S. A."),
        ("CENTRO AVIACION CIVIL SAN JUAN", "CENTRO DE AVIACION CIVIL SAN JUAN"),
        ("MD HELICÓPTEROS S.A.", "MD. HELICOPTEROS"),
        ("VOLAR", "VOLAR S.R.L"),
        ("ENRIQUE PINEYRO", "ENRIQUE PIÑEYRO"),
        ("SERVICIOS  AEREOS SUDAMERICANOS S.A.", "SERVICIOS AEREOS SUDAMERICANOS S.A"),
    ],
)
def test_clave_operador_agrupa_variantes(a, b):
    from potenciar_mdq.dims import clave_operador

    assert clave_operador(a) == clave_operador(b)


@pytest.mark.parametrize(
    "ident,operador",
    [("T99", "FUERZA AEREA ARGENTINA"), ("TC53", "FUERZA AEREA ARGENTINA"),
     ("PG380", "FUERZA AEREA ARGENTINA"), ("AE471", "EJERCITO ARGENTINO"),
     ("1G50", "ARMADA ARGENTINA"), ("2H243", "ARMADA ARGENTINA"),
     ("GN919", "GENDARMERIA NACIONAL ARGENTINA"), ("PA43", "PREFECTURA NAVAL ARGENTINA"),
     ("PF19", "POLICIA FEDERAL ARGENTINA"),
     # civiles y estatales sin fuerza: no coinciden
     ("LVABC", None), ("LQBEN", None), ("CCBAE", None), ("A6ALN", None), ("N12345", None),
     ("PRABC", None), ("FAU541", None)],
)
def test_prefijos_estatales(ident, operador):
    import re

    reglas = load_yaml("estatales.yaml")["prefijos"]
    hallado = next((r["operador"] for r in reglas if re.search(r["patron"], ident)), None)
    assert hallado == operador
