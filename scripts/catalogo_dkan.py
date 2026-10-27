"""Vuelca el catálogo completo de un portal DKAN/CKAN: cada dataset con título, grupos, etiquetas,
descripción y recursos (nombre, formato, URL, última modificación).

Salida: reports/fuentes/catalogo_<host>.md (legible) y .json (completo).

Uso:
    python scripts/catalogo_dkan.py https://datos.mardelplata.gob.ar
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from potenciar_mdq.http import PoliteSession
from potenciar_mdq.sources.dkan import DkanClient

OUT = Path(__file__).resolve().parents[1] / "reports" / "fuentes"


def _lista(valor) -> list[str]:
    if not valor:
        return []
    return [v.get("title") or v.get("name") or str(v) if isinstance(v, dict) else str(v)
            for v in valor]


def main(base_url: str) -> Path:
    cliente = DkanClient(base_url, PoliteSession(min_interval_s=0.5))
    slugs = cliente.package_list()
    print(f"{len(slugs)} datasets")
    fichas = []
    for i, slug in enumerate(slugs, 1):
        try:
            r = cliente.action("package_show", id=slug)
            ficha = r[0] if isinstance(r, list) else r
        except Exception as exc:  # noqa: BLE001 - un dataset roto no corta el volcado
            ficha = {"name": slug, "error": str(exc)[:200]}
        fichas.append(ficha)
        if i % 50 == 0:
            print(f"  {i}/{len(slugs)}")

    host = urlparse(base_url).netloc
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"catalogo_{host}.json").write_text(
        json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf-8")
    lineas = [f"# Catálogo de {host}", "", f"{len(fichas)} datasets.", ""]
    for f in sorted(fichas, key=lambda f: (f.get("title") or f.get("name") or "").lower()):
        lineas.append(f"## {f.get('title') or f.get('name')}")
        lineas.append(f"- slug: `{f.get('name')}` · modificado: {f.get('metadata_modified', '?')}")
        if f.get("error"):
            lineas.append(f"- ✗ {f['error']}")
        grupos, tags = _lista(f.get("groups")), _lista(f.get("tags"))
        if grupos or tags:
            lineas.append(f"- grupos: {', '.join(grupos) or '—'} · "
                          f"etiquetas: {', '.join(tags) or '—'}")
        org = f.get("organization")
        if isinstance(org, dict):
            lineas.append(f"- organización: {org.get('title') or org.get('name')}")
        notas = " ".join((f.get("notes") or "").split())
        if notas:
            lineas.append(f"- {notas[:300]}")
        for r in f.get("resources") or []:
            lineas.append(f"  - `{(r.get('format') or '?').lower()}` {r.get('name') or ''} — "
                          f"{r.get('url')} ({r.get('last_modified') or r.get('created') or '?'})")
        lineas.append("")
    dest = OUT / f"catalogo_{host}.md"
    dest.write_text("\n".join(lineas), encoding="utf-8")
    print(f"-> {dest}")
    return dest


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
