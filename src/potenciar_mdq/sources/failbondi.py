"""failbondi.fail: estado de vuelos de los aeropuertos de AA2000 (todas las aerolíneas, desde
dic-2024), recopilado cada 3 horas de la web de Aeropuertos Argentina por Nulo Science.

El dump (/api/dump) es un arreglo JSON con el último estado de cada vuelo; pesa cientos de MB, así
que se lee en streaming y se guardan solo los aeropuertos pedidos (JSON por línea).
Código del scraper: github.com/catdevnull/flybondi.fail. El sitio no garantiza la estabilidad del
endpoint.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import requests

URL = "https://failbondi.fail/api/dump"


_SEP = re.compile(r"[\s,]*")


def objetos(resp: requests.Response, max_seg: float = 900) -> Iterator[dict]:
    """Objetos de un arreglo JSON a medida que llegan (sin cargarlo entero en memoria).

    Avanza con un índice dentro del bloque y recorta el texto una sola vez por bloque: lineal en
    el tamaño del dump."""
    dec = json.JSONDecoder()
    buf, inicio, t0 = "", True, time.time()
    for chunk in resp.iter_content(chunk_size=1 << 20, decode_unicode=True):
        buf += chunk
        pos = 0
        if inicio:
            pos = _SEP.match(buf, pos).end()
            if pos < len(buf) and buf[pos] == "[":
                pos, inicio = pos + 1, False
        while True:
            pos = _SEP.match(buf, pos).end()
            if pos >= len(buf) or buf[pos] == "]":
                break
            try:
                obj, pos_fin = dec.raw_decode(buf, pos)
            except json.JSONDecodeError:
                break  # objeto incompleto: esperar más bytes
            yield obj
            pos = pos_fin
        buf = buf[pos:]
        if time.time() - t0 > max_seg:
            raise TimeoutError(f"dump de failbondi incompleto tras {max_seg:.0f} s")


def descargar(dest_dir: Path, aeropuertos: list[str], user_agent: str) -> Path:
    """Baja el dump y guarda los vuelos de `aeropuertos` en dest_dir/<fecha>_dump.jsonl."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{datetime.now(UTC):%Y%m%d}_dump.jsonl"
    tmp = dest.with_suffix(".part")
    n = total = 0
    with requests.get(URL, stream=True, timeout=(15, 120),
                      headers={"User-Agent": user_agent}) as r, open(tmp, "w") as f:
        r.raise_for_status()
        r.encoding = "utf-8"
        for o in objetos(r):
            total += 1
            if (o.get("json") or {}).get("arpt") in aeropuertos:
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
                n += 1
    if total == 0:
        tmp.unlink()
        raise ValueError("el dump de failbondi vino vacío")
    tmp.rename(dest)
    return dest
