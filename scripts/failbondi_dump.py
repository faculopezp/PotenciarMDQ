"""Explora el dump de failbondi.fail (vuelos de los aeropuertos de AA2000 desde dic-2024, todas las
aerolíneas, último estado de cada vuelo): lo lee en streaming, se queda con un aeropuerto y
resume tamaño, período, aerolíneas y estados.

Fuente: https://failbondi.fail/acerca (dump en /api/dump; no garantizan su estabilidad).
Código del scraper: github.com/catdevnull/flybondi.fail (API all-flights de AA2000).

Salida: reports/fuentes/failbondi/<iata>.csv y resumen.md

Uso:
    python scripts/failbondi_dump.py MDQ [--max-minutos 15]
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import time
from pathlib import Path

import requests

URL = "https://failbondi.fail/api/dump"
OUT = Path(__file__).resolve().parents[1] / "reports" / "fuentes" / "failbondi"
CAMPOS = ["aerolineas_flight_id", "last_updated", "stda", "atda", "delta", "matricula"]
CAMPOS_JSON = ["arpt", "mov", "aerolinea", "idaerolinea", "nro", "IATAdestorig", "destorig",
               "stda", "etda", "atda", "estes", "estin", "acftype", "matricula", "pasajeros",
               "tipoVuelo", "via", "x_date"]


def filas(resp, max_seg: float):
    """Objetos del arreglo JSON a medida que llegan (sin cargar todo en memoria)."""
    dec = json.JSONDecoder()
    buf, inicio, t0 = "", True, time.time()
    for chunk in resp.iter_content(chunk_size=1 << 20, decode_unicode=True):
        buf += chunk
        if inicio:
            buf = buf.lstrip()
            if buf.startswith("["):
                buf, inicio = buf[1:], False
        while True:
            buf = buf.lstrip(", \n\r\t")
            if not buf or buf[0] == "]":
                break
            try:
                obj, fin = dec.raw_decode(buf)
            except json.JSONDecodeError:
                break  # objeto incompleto: esperar más bytes
            yield obj
            buf = buf[fin:]
        if time.time() - t0 > max_seg:
            yield None  # corte por tiempo
            return


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("iata")
    ap.add_argument("--max-minutos", type=float, default=15)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    total, foco, cortado = 0, [], False
    fechas, aerolineas = [], collections.Counter()
    estados, aeropuertos = collections.Counter(), collections.Counter()
    with requests.get(URL, stream=True, timeout=(15, 120),
                      headers={"User-Agent": "PotenciarMDQ (datos abiertos)"}) as r:
        r.raise_for_status()
        r.encoding = "utf-8"
        for o in filas(r, args.max_minutos * 60):
            if o is None:
                cortado = True
                break
            total += 1
            j = o.get("json") or {}
            aeropuertos[j.get("arpt")] += 1
            if j.get("arpt") == args.iata:
                fila = {c: o.get(c) for c in CAMPOS}
                fila.update({f"j_{c}": j.get(c) for c in CAMPOS_JSON})
                foco.append(fila)
                fechas.append(str(o.get("stda") or "")[:10])
                aerolineas[j.get("aerolinea")] += 1
                estados[j.get("estes")] += 1
    with open(OUT / f"{args.iata}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(foco[0].keys()) if foco else CAMPOS)
        w.writeheader()
        w.writerows(foco)
    fechas = sorted(x for x in fechas if x)
    corte = " (corte por tiempo: dump incompleto)" if cortado else ""
    periodo = f"{fechas[0]} a {fechas[-1]}" if fechas else "—"
    lineas = ["# Dump de failbondi.fail", "",
              f"- Filas leídas: {total:,}{corte}",
              f"- Tiempo: {time.time() - t0:.0f} s", f"- Filas de {args.iata}: {len(foco):,}",
              f"- Período {args.iata} (stda): {periodo}",
              "", "## Aerolíneas en " + args.iata, ""]
    lineas += [f"- {k}: {v:,}" for k, v in aerolineas.most_common()]
    lineas += ["", "## Estados (estes) en " + args.iata, ""]
    lineas += [f"- {k}: {v:,}" for k, v in estados.most_common()]
    lineas += ["", "## Aeropuertos en lo leído (top 40)", ""]
    lineas += [f"- {k}: {v:,}" for k, v in aeropuertos.most_common(40)]
    if foco:
        lineas += ["", "## Muestra (5 filas)", "", "```"]
        lineas += [json.dumps(x, ensure_ascii=False, default=str) for x in foco[:5]] + ["```"]
    (OUT / "resumen.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas[:8]))


if __name__ == "__main__":
    main()
