"""Normalización de nombres de columnas y valores categóricos."""

from __future__ import annotations

import re
import unicodedata


def slug(text: str) -> str:
    """'Clasificación Vuelo ' -> 'clasificacion_vuelo'."""
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower())
    return text.strip("_")


# slug de la columna original -> nombre canónico. Agregar acá cada variante nueva que aparezca.
# Encabezado real 2023–2025: Fecha UTC;Hora UTC;Clase de Vuelo (todos los vuelos);
#   Clasificación Vuelo;Tipo de Movimiento;Aeropuerto;Origen / Destino;Aerolinea Nombre;
#   Aeronave;Pasajeros;PAX;Calidad dato
# 2026 agrega "Matrícula" entre Aeronave y Pasajeros.
ANAC_MOVIMIENTOS_ALIASES: dict[str, str] = {
    "fecha": "fecha",
    "fecha_utc": "fecha",
    "hora_utc": "hora_utc",
    "hora": "hora_utc",
    "clase_de_vuelo": "clase_vuelo",
    "clase_de_vuelo_todos_los_vuelos": "clase_vuelo",
    "clase_vuelo": "clase_vuelo",
    "clasificacion_vuelo": "clasificacion_vuelo",
    "clasificacion_de_vuelo": "clasificacion_vuelo",
    "tipo_de_movimiento": "tipo_movimiento",
    "tipo_movimiento": "tipo_movimiento",
    "aeropuerto": "aeropuerto",
    "origen_destino": "origen_destino",
    "aerolinea_nombre": "aerolinea",
    "aerolineas_nombre": "aerolinea",
    "aerolinea": "aerolinea",
    "aeronave": "aeronave",
    "matricula": "matricula",
    "pasajeros": "pasajeros",
    # PAX = pasajeros prorrateados para totales país: en cabotaje vale Pasajeros/2
    # (cada vuelo aparece en 2 aeropuertos), en internacional = Pasajeros.
    "pax": "pax_nacional",
    "calidad_dato": "calidad_dato",
    "calidad_del_dato": "calidad_dato",
}

ANAC_REQUIRED = ["fecha", "tipo_movimiento", "aeropuerto", "pasajeros"]


class SchemaError(ValueError):
    pass


def map_columns(columns: list[str], aliases: dict[str, str]) -> dict[str, str]:
    """Devuelve {columna_original: canónica}. Falla si hay columnas desconocidas o duplicadas."""
    unknown = [c for c in columns if slug(c) not in aliases]
    if unknown:
        raise SchemaError(
            f"Columnas sin mapear: {unknown}. Agregar alias en standardize/columns.py"
        )
    mapping = {c: aliases[slug(c)] for c in columns}
    canon = list(mapping.values())
    dupes = sorted({c for c in canon if canon.count(c) > 1})
    if dupes:
        raise SchemaError(f"Varias columnas mapean a {dupes}: {columns}")
    return mapping


VOCAB = {
    "clasificacion_vuelo": {
        "domestico": "cabotaje",
        "dom": "cabotaje",
        "cabotaje": "cabotaje",
        "internacional": "internacional",
        "int": "internacional",
    },
    "tipo_movimiento": {"aterrizaje": "aterrizaje", "despegue": "despegue"},
    "calidad_dato": {"definitivo": "definitivo", "provisorio": "provisorio"},
}

# Valores que ANAC usa como "sin dato".
SIN_DATO = ["0", "", "-", "S/D", "SD", "N/A"]
