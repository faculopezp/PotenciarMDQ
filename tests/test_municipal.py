"""Parsers del portal municipal, con fragmentos reales de las planillas."""

from pathlib import Path

from potenciar_mdq.standardize.municipal import (
    decimal,
    entero,
    filas_mes_x_anio,
    filas_por_mes,
    mes_de,
    normalizar_ruta,
)


def test_numeros():
    assert entero("1.422.547") == 1422547
    assert entero('"1,073"') == 1073
    assert entero("n/h") is None and entero("") is None and entero("-") is None
    assert decimal("6,3") == 6.3 and decimal("6.3") == 6.3 and decimal("-") is None


def test_meses():
    assert mes_de("Ene") == 1 and mes_de("ene-19") == 1 and mes_de("Diciembre") == 12
    assert mes_de("Ruta") is None


def test_rutas():
    assert normalizar_ruta("Córdoba - Mar del Plata") == "CBA"
    assert normalizar_ruta("Mar del Plata - Tucumán") == "TUC"
    assert normalizar_ruta("Aeroparque - Mar del Plata") == "AER"


def test_corrige_escala_x1000(tmp_path: Path):
    p = tmp_path / "movimientos-aeropuerto-2019_0.csv"
    p.write_text(",Ene,Feb\nCabotaje,1023000,800000\nInternacional,15000,5000\n", encoding="utf-8")
    filas = filas_por_mes(p, "movimientos", "movimientos", escala_max=50_000)
    assert [(f[1], f[2], f[3], f[4]) for f in filas][:2] == [("Cabotaje", 2019, 1, 1023),
                                                             ("Cabotaje", 2019, 2, 800)]


def test_latin1_y_punto_y_coma(tmp_path: Path):
    p = tmp_path / "pasajeros-tramo-2024.csv"
    p.write_bytes("Ruta;Ene;Feb\nC\xf3rdoba - Mar del Plata;1902;1693\n".encode("latin-1"))
    filas = filas_por_mes(p, "pasajeros_tramo", "x")
    assert filas[0][1] == "Córdoba - Mar del Plata" and filas[0][4] == 1902


def test_meses_por_anio(tmp_path: Path):
    p = tmp_path / "arribos.csv"
    p.write_text("Mes;2007;2008\nEnero;1.422.547;1.337.838\n", encoding="utf-8")
    assert filas_mes_x_anio(p, "arribos_turistas", "turistas")[1][2:5] == [2008, 1, 1337838]
