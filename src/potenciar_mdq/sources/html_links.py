"""Descubrir links a archivos en páginas HTML (ANAC DNTA). Recorre 1 nivel de sub-páginas."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from potenciar_mdq.http import PoliteSession


def extract_links(html: str, base_url: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for a in soup.find_all("a", href=True):
        out.append((urljoin(base_url, a["href"]), a.get_text(" ", strip=True)))
    return out


def discover_files(
    http: PoliteSession, url: str, extensions: list[str], follow_pattern: str | None = None
) -> tuple[list[dict], list[str]]:
    """Devuelve (archivos, warnings). Si no hay links en el HTML, probablemente sea render JS."""
    exts = tuple(f".{e.lower()}" for e in extensions)
    warnings: list[str] = []
    pages = [url]
    r = http.get(url)
    r.raise_for_status()
    links = extract_links(r.text, url)
    if follow_pattern:
        pages += sorted({u for u, _ in links if follow_pattern in u and u != url})

    files: dict[str, dict] = {}
    for page in pages:
        page_links = links if page == url else extract_links(http.get(page).text, page)
        if not page_links:
            warnings.append(f"{page}: sin <a href>; posible render JS → scripts/capture_network.py")
        for href, text in page_links:
            if urlparse(href).path.lower().endswith(exts):
                files.setdefault(href, {"url": href, "text": text, "page": page})
    if not files:
        warnings.append(f"{url}: 0 archivos {extensions} encontrados")
    return list(files.values()), warnings
