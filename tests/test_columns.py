import pytest

from potenciar_mdq.standardize.columns import (
    ANAC_MOVIMIENTOS_ALIASES,
    SchemaError,
    map_columns,
    slug,
)


def test_slug_quita_acentos_y_simbolos():
    assert slug(" Clasificación Vuelo ") == "clasificacion_vuelo"
    assert slug("Origen / Destino") == "origen_destino"
    assert slug("Clase de Vuelo (todos los vuelos)") == "clase_de_vuelo_todos_los_vuelos"


def test_map_columns_variantes():
    m = map_columns(["Fecha UTC", "Aerolíneas Nombre", "Pasajeros"], ANAC_MOVIMIENTOS_ALIASES)
    assert m == {"Fecha UTC": "fecha", "Aerolíneas Nombre": "aerolinea", "Pasajeros": "pasajeros"}


def test_columnas_duplicadas_fallan():
    with pytest.raises(SchemaError, match="fecha"):
        map_columns(["Fecha", "Fecha UTC"], ANAC_MOVIMIENTOS_ALIASES)


def test_columna_desconocida_falla():
    with pytest.raises(SchemaError, match="Columna Nueva"):
        map_columns(["Fecha", "Columna Nueva"], ANAC_MOVIMIENTOS_ALIASES)


def test_pax_y_matricula_son_columnas_distintas():
    cols = ["Fecha UTC", "Aeronave", "Matrícula", "Pasajeros", "PAX"]
    m = map_columns(cols, ANAC_MOVIMIENTOS_ALIASES)
    assert m["PAX"] == "pax_nacional" and m["Pasajeros"] == "pasajeros"
    assert m["Matrícula"] == "matricula"
