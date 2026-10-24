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
