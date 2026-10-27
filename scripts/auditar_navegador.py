"""Audita una web con navegador (Chromium headless): para sitios que cargan todo con JS o que
`requests` no puede abrir (certificados incompletos).

Para cada URL: registra todos los pedidos (método, URL, cuerpo POST, estado, tipo), guarda las
respuestas de texto (HTML, JS, JSON, XHR) y el DOM ya renderizado, lista formularios y selects con
sus opciones, recorre los ítems del menú indicados y prueba una consulta: elige en cada select la
opción que contenga --valor (ej. 0226), completa los campos de texto cuyo nombre contenga "ruta" y
aprieta el botón de consulta. Salida: reports/fuentes/auditoria_web/navegador/ + informe.md.

Uso:
    python scripts/auditar_navegador.py URL [URL ...] --menu "TMDA,Temporales" --valor 0226
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "reports" / "fuentes" / "auditoria_web" / "navegador"
TEXTO = ("html", "javascript", "json", "text", "xml", "csv")
BOTON = re.compile(r"consult|buscar|aceptar|ver|mostrar|enviar|generar", re.I)


def guardar(nombre: str, contenido: str) -> str:
    seguro = re.sub(r"[^\w.-]", "_", nombre)[:150]
    (OUT / seguro).write_text(contenido[:500_000], encoding="utf-8")
    return seguro


def controles(page) -> list[dict]:
    return page.evaluate("""() => [...document.querySelectorAll('input, select, textarea, button')]
      .map(e => ({tag: e.tagName.toLowerCase(), name: e.name || null, id: e.id || null,
                  type: e.type || null, value: (e.value || '').slice(0, 60),
                  text: (e.innerText || '').trim().slice(0, 60),
                  onclick: (e.getAttribute('onclick') || '').slice(0, 200),
                  opciones: e.tagName === 'SELECT'
                    ? [...e.options].slice(0, 40).map(o => [o.value, o.text.trim()]) : null}))""")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--menu", default="", help="textos del menú a cliquear (coma)")
    ap.add_argument("--valor", default="", help="valor a elegir en selects / campos de ruta")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    pedidos: list[dict] = []
    informe = ["# Auditoría con navegador", ""]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(ignore_https_errors=True)
        page = ctx.new_page()

        def on_response(resp):
            req = resp.request
            ctype = resp.headers.get("content-type", "")
            fila = {
                "etapa": etapa[0],
                "method": req.method,
                "url": req.url,
                "status": resp.status,
                "type": req.resource_type,
                "content_type": ctype,
                "post_data": req.post_data,
            }
            if any(t in ctype for t in TEXTO) and req.resource_type not in ("image", "font"):
                try:
                    fila["guardado"] = guardar(f"{etapa[0]}__{urlparse(req.url).path}", resp.text())
                except Exception as exc:  # noqa: BLE001 - algunas respuestas no tienen cuerpo
                    fila["error"] = str(exc)[:100]
            pedidos.append(fila)

        etapa = ["inicio"]
        page.on("response", on_response)
        for url in args.urls:
            etapa[0] = urlparse(url).path.strip("/").replace("/", "_") or "raiz"
            informe += [f"## {url}", ""]
            try:
                page.goto(url, wait_until="networkidle", timeout=60_000)
                page.wait_for_timeout(2000)
            except Exception as exc:  # noqa: BLE001
                informe += [f"- ✗ {exc}", ""]
                continue
            informe.append(f"- DOM: `{guardar(etapa[0] + '__dom.html', page.content())}`")
            informe += [f"- `{json.dumps(c, ensure_ascii=False)}`" for c in controles(page)]

            for item in [m for m in args.menu.split(",") if m]:
                etapa[0] = f"menu_{item}"
                try:
                    page.get_by_text(item, exact=True).first.click(timeout=5000)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(1500)
                    informe += [
                        f"### Menú «{item}»",
                        f"- URL: {page.url}",
                        f"- DOM: `{guardar(etapa[0] + '__dom.html', page.content())}`",
                    ]
                    informe += [f"- `{json.dumps(c, ensure_ascii=False)}`" for c in controles(page)]
                except Exception as exc:  # noqa: BLE001
                    informe.append(f"### Menú «{item}»: ✗ {str(exc)[:150]}")

            if args.valor:
                etapa[0] = f"consulta_{args.valor}"
                page.goto(url, wait_until="networkidle", timeout=60_000)
                page.wait_for_timeout(1500)
                hecho = []
                for sel in page.query_selector_all("select"):
                    opciones = sel.evaluate("s => [...s.options].map(o => [o.value, o.text])")
                    elegida = next(
                        (v for v, t in opciones if args.valor in v or args.valor in t), None
                    )
                    if elegida is not None:
                        sel.select_option(elegida)
                        page.wait_for_timeout(1500)
                        campo = sel.get_attribute("name") or sel.get_attribute("id")
                        hecho.append(f"select {campo}={elegida}")
                for inp in page.query_selector_all("input[type=text], input:not([type])"):
                    nombre = (inp.get_attribute("name") or "") + (inp.get_attribute("id") or "")
                    if "ruta" in nombre.lower():
                        inp.fill(args.valor)
                        hecho.append(f"input {nombre}={args.valor}")
                botones = [
                    b
                    for b in page.query_selector_all(
                        "button, input[type=submit], input[type=button], a"
                    )
                    if BOTON.search((b.inner_text() or "") + (b.get_attribute("value") or ""))
                ]
                if botones:
                    botones[0].click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000)
                    rotulo = botones[0].inner_text() or botones[0].get_attribute("value") or ""
                    hecho.append(f"click «{rotulo.strip()}»")
                informe += [
                    f"### Consulta de prueba ({args.valor})",
                    f"- Acciones: {hecho or 'ninguna'}",
                    f"- DOM: `{guardar(etapa[0] + '__dom.html', page.content())}`",
                ]
        browser.close()

    informe += ["", "## Pedidos de red", ""]
    for r in pedidos:
        if r["type"] in ("image", "font", "stylesheet"):
            continue
        cuerpo = f" · POST `{r['post_data'][:300]}`" if r.get("post_data") else ""
        informe.append(
            f"- [{r['etapa']}] {r['method']} {r['url']} → {r['status']} "
            f"`{r['content_type']}` ({r['type']}){cuerpo}"
            + (f" · guardado `{r['guardado']}`" if r.get("guardado") else "")
        )
    (OUT / "informe.md").write_text("\n".join(informe) + "\n", encoding="utf-8")
    (OUT / "pedidos.json").write_text(
        json.dumps(pedidos, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(f"{len(pedidos)} pedidos -> {OUT / 'informe.md'}")


if __name__ == "__main__":
    main()
