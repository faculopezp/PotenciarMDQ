"""Abre una URL en Chromium headless y registra las requests XHR/fetch y descargas.

Sirve para descubrir la API interna que usa una web que renderiza con JS
(ej. consultas-publicas.anac.gob.ar). Salida: reports/network_<host>.json

Uso:
    uv pip install playwright && playwright install chromium   # una vez
    python scripts/capture_network.py https://consultas-publicas.anac.gob.ar/estadisticas-dnta/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

INTERESTING = ("xhr", "fetch", "document")


def main(url: str, wait_ms: int = 5000) -> Path:
    hits: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        def on_response(resp):
            req = resp.request
            ctype = resp.headers.get("content-type", "")
            if req.resource_type in INTERESTING or any(
                k in ctype for k in ("json", "csv", "spreadsheet", "excel", "pdf")
            ):
                hits.append(
                    {
                        "method": req.method,
                        "url": req.url,
                        "status": resp.status,
                        "type": req.resource_type,
                        "content_type": ctype,
                        "post_data": req.post_data,
                    }
                )

        page.on("response", on_response)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(wait_ms)
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText])")
        browser.close()

    out = Path("reports") / f"network_{urlparse(url).netloc}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps({"url": url, "requests": hits, "links": links}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"{len(hits)} requests, {len(links)} links -> {out}")
    for h in hits:
        if "json" in h["content_type"]:
            print(f"  JSON {h['method']} {h['url']}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
