"""Probe de endpoints e ingesta raw según config/sources.yaml."""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from potenciar_mdq.http import PoliteSession, download
from potenciar_mdq.settings import RAW, REPORTS, sources
from potenciar_mdq.sources.ckan import CkanClient
from potenciar_mdq.sources.dkan import DkanClient
from potenciar_mdq.sources.html_links import discover_files

log = logging.getLogger(__name__)


def _session() -> PoliteSession:
    d = sources()["defaults"]
    return PoliteSession(d["min_interval_s"], (d["timeout_connect_s"], d["timeout_read_s"]))


def _ckan_with_fallback(cfg: dict, http: PoliteSession) -> tuple[CkanClient, str]:
    """Devuelve (cliente, dataset) del primer portal que responda package_show."""
    candidates = [(cfg["base_url"], cfg["dataset"])]
    if fb := cfg.get("fallback"):
        candidates.append((fb["base_url"], fb["dataset"]))
    last_exc: Exception | None = None
    for base, dataset in candidates:
        client = CkanClient(base, http)
        try:
            client.package_show(dataset)
            return client, dataset
        except Exception as exc:  # noqa: BLE001 - queremos probar el fallback ante cualquier error
            log.warning("CKAN %s/%s no disponible: %s", base, dataset, exc)
            last_exc = exc
    raise RuntimeError(f"Ningún portal respondió para {cfg['dataset']}") from last_exc


def expand_pattern(cfg: dict) -> list[str]:
    """Plantilla {yyyy}/{yyyymm} -> lista de URLs entre `desde` y `hasta` (YYYY-MM)."""
    y0, m0 = map(int, str(cfg["desde"]).split("-"))
    y1, m1 = map(int, str(cfg["hasta"]).split("-"))
    tpl = cfg["template"]
    urls: list[str] = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        url = tpl.format(yyyy=f"{y:04d}", yyyymm=f"{y:04d}{m:02d}")
        if url not in urls:
            urls.append(url)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return urls


def openmeteo_url(cfg: dict) -> str:
    from datetime import date, timedelta
    from urllib.parse import urlencode

    params = {
        "latitude": cfg["latitud"], "longitude": cfg["longitud"],
        "start_date": str(cfg["desde"]), "end_date": str(date.today() - timedelta(days=6)),
        "daily": ",".join(cfg["diario"]), "timezone": cfg["zona_horaria"],
    }
    return f"{cfg['url']}?{urlencode(params)}"


def _exists(http: PoliteSession, url: str) -> bool:
    r = http.get(url, stream=True)
    r.close()
    return r.status_code == 200


def _preview(http: PoliteSession, url: str, n_lines: int = 3) -> list[str]:
    """Primeras líneas de un archivo de texto (para ver encabezados sin bajarlo entero)."""
    try:
        r = http.get(url, stream=True)
        raw = b""
        for chunk in r.iter_content(chunk_size=4096):
            raw += chunk
            if raw.count(b"\n") >= n_lines or len(raw) > 32_768:
                break
        r.close()
    except Exception as exc:  # noqa: BLE001 - es solo una vista previa
        return [f"(sin vista previa: {type(exc).__name__})"]
    text = raw.decode("utf-8", errors="replace") if raw[:3] != b"PK\x03" else "(archivo zip/xlsx)"
    return [line[:300] for line in text.splitlines()[:n_lines]]


_URL_RX = re.compile(
    r"""(?:src|href|action|url|fetch|get|post|ajax)\s*[:=(]\s*["'`]([^"'`\s]{3,200})["'`]""", re.I
)


def _scan(http: PoliteSession, url: str, follow_js: bool = True) -> list[str]:
    """URLs referenciadas por una página (y sus .js): para descubrir endpoints sin documentar."""
    try:
        html = http.get(url).text
    except Exception as exc:  # noqa: BLE001 - es solo exploración
        return [f"- (scan falló: {type(exc).__name__})"]
    found = {u for u in _URL_RX.findall(html)}
    if follow_js:
        for js in [u for u in found if u.split("?")[0].endswith(".js")][:15]:
            try:
                found |= set(_URL_RX.findall(http.get(urljoin(url, js)).text))
            except Exception:  # noqa: BLE001, S112
                continue
    interesantes = sorted(u for u in found if not u.endswith((".css", ".png", ".svg", ".ico",
                                                               ".jpg", ".woff", ".woff2")))
    return ["- URLs encontradas:", *[f"  - `{u}`" for u in interesantes[:120]]]


def probe() -> Path:
    """Valida cada fuente y escribe reports/probe.md (no descarga datos)."""
    http = _session()
    lines = [f"# Probe de fuentes — {datetime.now(UTC):%Y-%m-%d %H:%M} UTC", ""]
    for sid, cfg in sources()["sources"].items():
        lines.append(f"## `{sid}` ({cfg['kind']})")
        try:
            if cfg["kind"] == "ckan_package":
                client, dataset = _ckan_with_fallback(cfg, http)
                res = client.resources(dataset)
                lines.append(f"- OK `{client.base_url}` dataset `{dataset}`: {len(res)} recursos")
                for r in res:
                    lines.append(f"  - `{r.format}` {r.name} — `{r.id}` — mod {r.last_modified}")
                    if r.format in ("csv", "xml", "txt") or r.url.lower().endswith(".csv"):
                        lines += [f"    > {x}" for x in _preview(http, r.url)]
            elif cfg["kind"] == "dkan_package":
                client = DkanClient(cfg["base_url"], http)
                slugs = client.package_list()
                hits = [s for s in slugs if any(t in s for t in cfg.get("search_terms", []))]
                lines.append(f"- OK `{client.api}`: {len(slugs)} datasets; coinciden: {hits}")
                for slug in cfg.get("datasets", []):
                    lines.append(f"### `{slug}`")
                    for r in client.resources(slug):
                        lines.append(f"  - `{r.format}` {r.name} — {r.url} — mod {r.last_modified}")
                        if r.format in ("csv", "txt") or r.url.lower().endswith(".csv"):
                            lines += [f"    > {x}" for x in _preview(http, r.url, 4)]
            elif cfg["kind"] == "html_links":
                files, warns = discover_files(
                    http, cfg["url"], cfg["file_extensions"], cfg.get("follow_pattern")
                )
                lines.append(f"- {len(files)} archivos encontrados")
                lines += [f"  - [{f['text'] or 'sin texto'}]({f['url']})" for f in files[:200]]
                lines += [f"- ⚠️ {w}" for w in warns]
            elif cfg["kind"] == "url_pattern":
                urls = expand_pattern(cfg)
                ok = [u for u in urls if _exists(http, u)]
                lines.append(f"- {len(ok)}/{len(urls)} URLs existen")
                lines += [f"  - {u}" for u in ok]
            elif cfg["kind"] == "static_files":
                ok = [u for u in cfg["urls"] if _exists(http, u)]
                lines.append(f"- {len(ok)}/{len(cfg['urls'])} URLs responden 200")
            elif cfg["kind"] == "openmeteo":
                r = http.get(openmeteo_url(cfg), stream=True)
                lines.append(f"- HTTP {r.status_code} `{openmeteo_url(cfg)[:160]}`")
                r.close()
            elif cfg["kind"] == "static_file":
                r = http.get(cfg["url"], stream=True)
                lines.append(
                    f"- HTTP {r.status_code}, content-type `{r.headers.get('Content-Type')}`"
                )
                r.close()
                if cfg.get("preview"):
                    lines += ["```", *_preview(http, cfg["url"], n_lines=6), "```"]
                if cfg.get("scan"):
                    lines += _scan(http, cfg["url"], cfg.get("scan_follow_js", True))
        except Exception as exc:  # noqa: BLE001 - el probe reporta, no corta
            lines.append(f"- ❌ {type(exc).__name__}: {exc}")
        lines.append("")
    out = REPORTS / "probe.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def ingest(only: list[str] | None = None, force: bool = False) -> list[Path]:
    """Descarga cada fuente; una fuente caída no corta las demás.

    Si después de la corrida no hay CSV de movimientos ANAC (portal caído o bloqueado),
    se baja el espejo `anac_movimientos_espejo` como respaldo.
    """
    http = _session()
    new_files: list[Path] = []
    for sid, cfg in sources()["sources"].items():
        if (only and sid not in only) or (not only and not cfg.get("enabled")):
            continue
        try:
            new_files += _ingest_source(http, sid, cfg, force)
        except Exception as exc:  # noqa: BLE001 - se registra y se sigue con la próxima fuente
            log.error("Fuente %s falló: %s: %s", sid, type(exc).__name__, exc)
    movs = RAW / "anac_movimientos"
    hay_csv = any(p.name.lower().endswith((".csv", ".csv.gz")) for p in movs.rglob("*"))
    if not only and not hay_csv:
        log.warning("Sin CSV oficiales de ANAC: usando el espejo de respaldo")
        espejo = sources()["sources"]["anac_movimientos_espejo"]
        new_files += _ingest_source(http, "anac_movimientos_espejo", espejo, force)
    return new_files


def _ingest_source(http: PoliteSession, sid: str, cfg: dict, force: bool) -> list[Path]:
    new_files: list[Path] = []
    dest_dir = RAW / sid
    if cfg["kind"] == "ckan_package":
        client, dataset = _ckan_with_fallback(cfg, http)
        for r in client.resources(dataset, cfg.get("resource_formats")):
            p = download(http, r.url, dest_dir / r.id, sid, r.last_modified, force)
            if p:
                new_files.append(p)
    elif cfg["kind"] == "html_links":
        files, warns = discover_files(
            http, cfg["url"], cfg["file_extensions"], cfg.get("follow_pattern")
        )
        for w in warns:
            log.warning(w)
        for f in files:
            p = download(http, f["url"], dest_dir, sid, force=force)
            if p:
                new_files.append(p)
    elif cfg["kind"] == "dkan_package":
        client = DkanClient(cfg["base_url"], http)
        for slug in cfg.get("datasets", []):
            for r in client.resources(slug, cfg.get("resource_formats")):
                p = download(http, r.url, dest_dir / slug / r.id, sid, r.last_modified, force)
                if p:
                    new_files.append(p)
    elif cfg["kind"] == "openmeteo":
        p = download(http, openmeteo_url(cfg), dest_dir, sid, force=force)
        if p:
            new_files.append(p)
    elif cfg["kind"] == "static_file":
        p = download(http, cfg["url"], dest_dir, sid, force=force)
        if p:
            new_files.append(p)
    elif cfg["kind"] == "url_pattern":
        for url in expand_pattern(cfg):
            if not _exists(http, url):
                continue
            p = download(http, url, dest_dir, sid, force=force)
            if p:
                new_files.append(p)
    elif cfg["kind"] == "static_files":
        target = RAW / cfg.get("dest_source", sid)
        for url in cfg["urls"]:
            name = Path(urlparse(url).path).name.split(".")[0]
            p = download(http, url, target / f"espejo_{name}", sid, force=force)
            if p:
                new_files.append(p)
    else:
        log.info("%s: kind %s solo exploratorio, se saltea en ingest", sid, cfg["kind"])
    return new_files
