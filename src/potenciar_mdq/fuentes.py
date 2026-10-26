"""Muestras de fuentes nuevas -> reports/fuentes/ (el CI las commitea).

El entorno de desarrollo no llega a *.gob.ar: para diseñar un parser hace falta ver el archivo
real. Este paso deja en el repo el encabezado, algunas filas y las filas del foco de cada CSV, y el
texto de cada PDF (solo las páginas que nombran al foco, más la primera).
"""

from __future__ import annotations

import csv
import io
import logging
from pathlib import Path

from potenciar_mdq.settings import RAW, REPORTS

log = logging.getLogger(__name__)
FOCO = ("mar del plata", "mardel", "general pueyrredon", "sazm")


def _csv(path: Path, n: int = 8, n_foco: int = 40) -> list[str]:
    raw = path.read_bytes()
    texto = next((raw.decode(enc) for enc in ("utf-8-sig", "latin-1") if _decodifica(raw, enc)), "")
    filas = list(csv.reader(io.StringIO(texto)))
    foco = [f for f in filas[1:] if any(k in ",".join(f).lower() for k in FOCO)]
    out = [f"### `{path.relative_to(RAW)}` — {len(filas) - 1} filas, {len(foco)} del foco", "```"]
    out += [",".join(f) for f in filas[: n + 1]]
    out += ["... (filas del foco)"] + [",".join(f) for f in foco[:n_foco]] + ["```", ""]
    return out


def _decodifica(raw: bytes, enc: str) -> bool:
    try:
        raw.decode(enc)
        return True
    except UnicodeDecodeError:
        return False


def _pdf(path: Path, dest: Path) -> str:
    import pdfplumber

    partes = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text() or ""
            if i == 0 or any(k in texto.lower() for k in FOCO):
                partes.append(f"=== página {i + 1} de {len(pdf.pages)} ===\n{texto}")
    dest.write_text("\n\n".join(partes), encoding="utf-8")
    return f"- `{path.name}` → `{dest.relative_to(REPORTS)}` ({len(partes)} páginas)"


def run(out: Path = REPORTS / "fuentes") -> Path:
    out.mkdir(parents=True, exist_ok=True)
    lineas = ["# Muestras de fuentes nuevas", ""]
    for sid in ("yvera_terrestre",):
        lineas.append(f"## {sid}")
        for p in sorted((RAW / sid).rglob("*.csv")):
            try:
                lineas += _csv(p)
            except Exception as exc:  # noqa: BLE001 - muestra, no corta
                lineas.append(f"- ❌ {p.name}: {type(exc).__name__}: {exc}")
    lineas.append("## cnrt_ferroviario")
    (out / "cnrt").mkdir(exist_ok=True)
    for p in sorted((RAW / "cnrt_ferroviario").rglob("*.pdf")):
        try:
            lineas.append(_pdf(p, out / "cnrt" / f"{p.stem}.txt"))
        except Exception as exc:  # noqa: BLE001
            lineas.append(f"- ❌ {p.name}: {type(exc).__name__}: {exc}")
    dest = out / "muestras.md"
    dest.write_text("\n".join(lineas), encoding="utf-8")
    return dest
