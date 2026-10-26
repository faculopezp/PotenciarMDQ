"""PDF de ANAC -> CSV en data/reference (se corre a mano cuando ANAC publica un listado nuevo).

- Empresas de transporte aerocomercial regulares y no regulares (Partes 121/135, con CESA).
- Titulares de certificado de explotador de trabajo aéreo (CETA).

Requiere pdftotext (poppler-utils). Uso: uv run python scripts/listados_anac.py
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "data" / "reference"
PDF = REF / "anac_pdf"


def _texto(pdf: Path) -> list[str]:
    salida = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True,
                            capture_output=True, text=True).stdout
    return salida.splitlines()


def empresas_121_135(pdf: Path) -> list[dict]:
    fila = re.compile(r"^\s*(?P<empresa>\S.*?)\s{2,}(?P<cesa>ANAC\s*[-–]\s*\d+.*?)\s+"
                      r"(?P<desde>\d{2}-\w{2,3}-\d{4})\s+(?P<hasta>\d{2}-\w{2,3}-\d{4})\s*$")
    return [m.groupdict() for linea in _texto(pdf) if (m := fila.match(linea))]


def ceta(pdf: Path) -> list[dict]:
    """Titulares de CETA. Algunos nombres ocupan dos líneas (el estado queda en la primera)."""
    filas, actual = [], None
    fila = re.compile(r"^\s*(\d+)\.\s+(?P<titular>\S.*?)\s*(?P<estado>VIGENTE|VENCIDO)?\s*$")
    for linea in _texto(pdf):
        if m := fila.match(linea):
            actual = {"titular": m["titular"].strip(), "estado": m["estado"] or ""}
            filas.append(actual)
        elif actual and linea.strip() and not re.search(r"TITULAR|EMPRESAS|CERTIFICADO", linea):
            resto = linea.strip()
            if resto in ("VIGENTE", "VENCIDO"):
                actual["estado"] = resto
            elif re.fullmatch(r"[A-ZÁÉÍÓÚÑ .,'&()-]+", resto) and len(resto) < 40:
                actual["titular"] += " " + resto
    return filas


def _guardar(nombre: str, filas: list[dict]) -> None:
    with open(REF / nombre, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"{nombre}: {len(filas)} filas")


if __name__ == "__main__":
    _guardar("anac_empresas_121_135.csv", empresas_121_135(PDF / "empresas_121_135_2024-04-12.pdf"))
    _guardar("anac_ceta.csv", ceta(PDF / "ceta_2024-11-19.pdf"))
