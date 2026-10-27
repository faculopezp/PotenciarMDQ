"""Audita una web pública para encontrar datos descargables y endpoints de consulta.

Pensado para correr en el CI (el entorno de desarrollo no llega a *.gob.ar). Para cada URL semilla:
baja el HTML, lista enlaces, iframes, formularios (acción, método y campos) y scripts; baja cada
script y busca rutas de consulta (servlets, .do/.jsp/.php/.aspx, /api/, json, ajax, fetch). Sigue
un nivel de enlaces dentro de los hosts permitidos y prueba con HEAD los archivos (xlsx, csv, pdf,
zip). Guarda las páginas y scripts crudos para leerlos después.

Salida: reports/fuentes/auditoria_web/<host>/ (crudos) y reports/fuentes/auditoria_web/informe.md.

Uso:
    python scripts/auditar_web.py URL [URL ...] --hosts host1,host2
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

OUT = Path(__file__).resolve().parents[1] / "reports" / "fuentes" / "auditoria_web"
UA = "PotenciarMDQ/0.1 (proyecto de datos abiertos; github.com/faculopezp/PotenciarMDQ)"
ARCHIVOS = re.compile(r"\.(xlsx?|csv|zip|pdf|json|geojson|kml|kmz|txt|ods)(\?|$)", re.I)
ENDPOINT = re.compile(
    r"""["'`]([^"'`\s<>]*?(?:\.do|\.jsp|\.php|\.aspx?|\.ashx|\.asmx|servlet|Servlet|/api/|/rest/|"""
    r"""\.json|consulta|Consulta|tmda|TMDA|censo|Censo|estacion|Estacion|permanente)[^"'`\s<>]*)["'`]"""
)
LLAMADAS = re.compile(
    r"(\$\.(?:ajax|get|post|getJSON)\s*\(|fetch\s*\(|XMLHttpRequest|\.open\s*\(\s*[\"'](?:GET|POST))"
)
MAX_TEXTO = 400_000


def nombre_local(url: str) -> Path:
    u = urlparse(url)
    ruta = (u.path.strip("/") or "index").replace("/", "__")
    if u.query:
        ruta += "__" + re.sub(r"[^\w=&.-]", "_", u.query)[:80]
    return OUT / u.netloc / ruta[:150]


def bajar(s: requests.Session, url: str) -> requests.Response | None:
    try:
        return s.get(url, timeout=(10, 60))
    except requests.RequestException as exc:
        print(f"  ✗ {url}: {exc}")
        return None


def auditar_html(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    enlaces = sorted({urljoin(url, a["href"]) for a in soup.find_all("a", href=True)})
    iframes = sorted({urljoin(url, f["src"]) for f in soup.find_all(["iframe", "frame"], src=True)})
    scripts = sorted({urljoin(url, sc["src"]) for sc in soup.find_all("script", src=True)})
    forms = []
    for f in soup.find_all("form"):
        campos = []
        for c in f.find_all(["input", "select", "textarea"]):
            opciones = [o.get("value", o.text.strip()) for o in c.find_all("option")][:15]
            campos.append({"tag": c.name, "name": c.get("name"), "id": c.get("id"),
                           "type": c.get("type"), "value": c.get("value"), "opciones": opciones})
        forms.append({"action": urljoin(url, f.get("action") or url),
                      "method": (f.get("method") or "GET").upper(), "campos": campos})
    inline = "\n".join(sc.get_text() for sc in soup.find_all("script", src=False))
    return {"titulo": soup.title.get_text(strip=True) if soup.title else "", "enlaces": enlaces,
            "iframes": iframes, "scripts": scripts, "forms": forms, "inline": inline}


def endpoints(texto: str) -> list[str]:
    return sorted({m.group(1) for m in ENDPOINT.finditer(texto)})[:80]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--hosts", default="", help="hosts permitidos para seguir enlaces (coma)")
    ap.add_argument("--max-paginas", type=int, default=40)
    args = ap.parse_args()
    # Solo se siguen enlaces (y se bajan scripts) de estos hosts; por defecto, los de las semillas.
    hosts = {h for h in args.hosts.split(",") if h} or {urlparse(u).netloc for u in args.urls}
    s = requests.Session()
    s.headers["User-Agent"] = UA
    OUT.mkdir(parents=True, exist_ok=True)

    informe = ["# Auditoría web", "", f"Semillas: {', '.join(args.urls)}",
               f"Hosts: {', '.join(sorted(hosts))}", ""]
    pendientes, vistos, archivos = list(args.urls), set(), {}
    while pendientes and len(vistos) < args.max_paginas:
        url = pendientes.pop(0)
        if url in vistos:
            continue
        vistos.add(url)
        r = bajar(s, url)
        if r is None:
            informe += [f"## {url}", "", "- ✗ no responde", ""]
            continue
        ctype = r.headers.get("content-type", "")
        redir = f" · redirige a {r.url}" if r.url != url else ""
        informe += [f"## {url}", "",
                    f"- HTTP {r.status_code} · `{ctype}` · {len(r.content):,} bytes{redir}"]
        if "html" not in ctype:
            informe.append("")
            continue
        destino = nombre_local(url).with_suffix(".html")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(r.text[:MAX_TEXTO], encoding="utf-8")
        a = auditar_html(r.url, r.text)
        informe += [f"- Título: {a['titulo']}", f"- Guardado: `{destino.relative_to(OUT)}`"]
        for f in a["forms"]:
            informe += [f"- **Formulario** {f['method']} `{f['action']}`"]
            informe += [f"  - `{c['tag']}` name=`{c['name']}` id=`{c['id']}` type=`{c['type']}` "
                        f"value=`{c['value']}` opciones={c['opciones']}" for c in f["campos"]]
        informe += [f"- iframe: {u}" for u in a["iframes"]]
        informe += [f"- script: {u}" for u in a["scripts"]]
        ep = endpoints(r.text)
        if ep:
            informe += ["- Rutas mencionadas en el HTML:"] + [f"  - `{e}`" for e in ep]
        if LLAMADAS.search(a["inline"]):
            informe.append("- El JS en línea hace llamadas (ajax/fetch): ver el HTML guardado")
        for sc in a["scripts"]:
            if urlparse(sc).netloc not in hosts or sc in vistos:
                continue
            vistos.add(sc)
            rs = bajar(s, sc)
            if rs is None or rs.status_code != 200:
                continue
            dj = nombre_local(sc).with_suffix(".js")
            dj.parent.mkdir(parents=True, exist_ok=True)
            dj.write_text(rs.text[:MAX_TEXTO], encoding="utf-8")
            ejs = endpoints(rs.text)
            informe.append(f"- script `{sc}` ({len(rs.content):,} bytes, llamadas: "
                           f"{'sí' if LLAMADAS.search(rs.text) else 'no'})")
            informe += [f"  - `{e}`" for e in ejs]
        for u in a["enlaces"] + a["iframes"]:
            host = urlparse(u).netloc
            if ARCHIVOS.search(urlparse(u).path):
                archivos.setdefault(u, url)
            elif host in hosts and u not in vistos and u.split("#")[0] not in vistos:
                pendientes.append(u.split("#")[0])
        informe.append("")

    informe += ["## Archivos enlazados", ""]
    for u, origen in sorted(archivos.items()):
        try:
            h = s.head(u, timeout=(10, 30), allow_redirects=True)
            meta = (f"HTTP {h.status_code} · `{h.headers.get('content-type', '')}` · "
                    f"{h.headers.get('content-length', '?')} bytes")
        except requests.RequestException as exc:
            meta = f"✗ {exc}"
        informe.append(f"- {u} — {meta} (en {origen})")
    (OUT / "informe.md").write_text("\n".join(informe) + "\n", encoding="utf-8")
    print(f"informe: {OUT / 'informe.md'} ({len(vistos)} URLs)")


if __name__ == "__main__":
    main()
