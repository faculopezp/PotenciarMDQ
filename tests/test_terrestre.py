"""Tren (planilla CNRT) y micros (pares origen-destino de Yvera)."""

from pathlib import Path

import duckdb
import openpyxl

from potenciar_mdq.settings import SQL
from potenciar_mdq.standardize import generic


def test_build_tren_lee_solo_filas_de_datos(tmp_path: Path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "DATOS"
    ws.append(["Año", "Mes", "Línea", "Operador", "Tipo de Servicio", "Jurisdicción", "Servicio",
               "PAX", None, None, None, "PAX"])
    ws.append([2008, "Enero", "Roca", "FERROBAIRES", "Larga Distancia", "Provincial",
               "P. Constitución-Mar del Plata-Miramar (Buenos Aires)", 110541, None, None, None,
               "Dato"])
    ws.append([2026, "Septiembre", "Roca", "SOFSE", "Larga Distancia", "Nacional",
               "P. Constitución-Mar del Plata (Buenos Aires)", 39233])
    ws.append([None, None, None, None, None, None, None, None, None, None, None, "Var %"])
    (tmp_path / "raw").mkdir()
    wb.save(tmp_path / "raw" / "20261026_pax.xlsx")
    dest = generic.build_tren(tmp_path / "raw", tmp_path)
    filas = duckdb.sql(f"SELECT anio, mes, pax FROM '{dest}' ORDER BY anio").fetchall()
    assert filas == [(2008, 1, 110541), (2026, 9, 39233)]


def test_pares_de_micro_separan_sentido_y_unifican_nombres():
    con = duckdb.connect()
    vacia = ("indice_tiempo DATE, localidad_origen VARCHAR, provincia_origen VARCHAR, "
             "localidad_destino VARCHAR, provincia_destino VARCHAR, ruta_clasificacion VARCHAR, "
             "{m} VARCHAR, asientos INT, pasajeros INT")
    con.execute(f"CREATE TABLE stg_bus_base_microdatos ({vacia.format(m='descripcion')})")
    con.execute(f"CREATE TABLE stg_bus_base_microdatos_dut ({vacia.format(m='clase_modalidad')})")
    for t in ("viajes_asientos_pasajeros", "viajes_asientos_pasajeros_dut"):
        con.execute(f"CREATE TABLE stg_bus_{t} (indice_tiempo DATE, viajes INT, asientos INT, "
                    "pasajeros INT)")
    con.execute("CREATE TABLE stg_bus_magnitudes_por_ruta AS SELECT * FROM (VALUES "
                "(2019, 'Caba-Mar Del Plata', 1, 60, 50), "
                "(2019, 'Mar Del Plata-Ciudad Autónoma De Buenos Aires', 1, 60, 40), "
                "(2019, 'Rosario-Córdoba', 1, 60, 40)) "
                "t(indice_tiempo, par_origen_destino, viajes, asientos, pasajeros)")
    con.execute("CREATE TABLE stg_bus_magnitudes_por_ruta_dut AS "
                "SELECT * FROM stg_bus_magnitudes_por_ruta LIMIT 0")
    con.execute((SQL / "bd" / "80_omnibus.sql").read_text(encoding="utf-8"))
    filas = con.execute("SELECT sentido, extremo_clave, pasajeros, fuente FROM fct_bus_ruta_anual "
                        "ORDER BY sentido").fetchall()
    assert filas == [("llegada", "ciudad autonoma de buenos aires", 50, "anual_por_ruta"),
                     ("salida", "ciudad autonoma de buenos aires", 40, "anual_por_ruta")]
    [(nombre,)] = con.execute("SELECT nombre FROM dim_bus_localidad").fetchall()
    assert nombre == "Ciudad Autónoma de Buenos Aires"


def test_filas_medio_lee_ambos_formatos(tmp_path: Path):
    from potenciar_mdq.standardize.municipal import filas_medio

    viejo = tmp_path / "arribos-medio-transporte-2013.csv"
    viejo.write_text('Mes,AVION,TREN,OMNIBUS,AUTO\nEnero,"9,720","22,035","293,160","1,080,070"\n')
    nuevo = tmp_path / "Arribo-de-Turistas-por-Medio-de-Transporte-2025.csv"
    nuevo.write_text("Mes;AVION;TREN;OMNIBUS;AUTO\nMayo;8965;15.881;42.088;378.806\n")
    assert [f[1:5] for f in filas_medio(viejo)] == [
        ["avion", 2013, 1, 9720], ["tren", 2013, 1, 22035], ["omnibus", 2013, 1, 293160],
        ["auto", 2013, 1, 1080070]]
    assert [f[1:5] for f in filas_medio(nuevo)][0] == ["avion", 2025, 5, 8965]


def test_filas_procedencia_unifica_regiones(tmp_path: Path):
    from potenciar_mdq.standardize.municipal import filas_procedencia

    viejo = tmp_path / "procedencia-turistas-2007.csv"
    viejo.write_text("Mes,Ciudad de Buenos Aires,Gran Bs As,Pcia Bs As,Resto del país,Exterior\n"
                     "Enero,34.3,25.5,16.2,22.0,1.6\n", encoding="latin-1")
    nuevo = tmp_path / "procedencia-turistas-2024.csv"
    nuevo.write_text("Mes;CABA;GBA;Resto PBA;Resto del país\nEnero;21,70%;39,50%;12,50%;26,30%\n")
    assert {f[1] for f in filas_procedencia(viejo)} == {
        "CABA", "Conurbano", "Resto de la provincia", "Resto del país", "Exterior"}
    assert [f[1:5] for f in filas_procedencia(nuevo)][0] == ["CABA", 2024, 1, 21.7]
