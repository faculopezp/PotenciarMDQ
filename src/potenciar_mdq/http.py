"""Cliente HTTP "educado": rate limit por host, reintentos con backoff y descarga con manifest."""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from potenciar_mdq import __version__
from potenciar_mdq.settings import MANIFEST


def _user_agent() -> str:
    contact = os.environ.get("CONTACT", "")
    suffix = f"; {contact}" if contact else ""
    return f"PotenciarMDQ/{__version__} (proyecto de datos abiertos{suffix})"


class PoliteSession:
    def __init__(self, min_interval_s: float = 1.0, timeout: tuple[float, float] = (10, 120)):
        self.min_interval_s = min_interval_s
        self.timeout = timeout
        self._last_hit: dict[str, float] = {}
        self.session = requests.Session()
        self.session.headers["User-Agent"] = _user_agent()
        retry = Retry(
            total=5,
            backoff_factor=2,  # 2, 4, 8, 16, 32 s
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _throttle(self, url: str) -> None:
        host = urlparse(url).netloc
        wait = self.min_interval_s - (time.monotonic() - self._last_hit.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        self._last_hit[host] = time.monotonic()

    def get(self, url: str, **kwargs) -> requests.Response:
        self._throttle(url)
        kwargs.setdefault("timeout", self.timeout)
        return self.session.get(url, **kwargs)

    def get_json(self, url: str, **kwargs) -> dict:
        r = self.get(url, **kwargs)
        r.raise_for_status()
        return r.json()


@dataclass
class ManifestEntry:
    source_id: str
    url: str
    path: str
    fetched_at: str
    status: int
    bytes: int
    sha256: str
    etag: str | None = None
    last_modified: str | None = None
    remote_last_modified: str | None = None  # el de los metadatos CKAN, si existe


def read_manifest(path: Path = MANIFEST) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def latest_for_url(url: str, path: Path = MANIFEST) -> dict | None:
    hits = [e for e in read_manifest(path) if e["url"] == url and e["status"] == 200]
    return hits[-1] if hits else None


def append_manifest(entry: ManifestEntry, path: Path = MANIFEST) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def download(
    http: PoliteSession,
    url: str,
    dest_dir: Path,
    source_id: str,
    remote_last_modified: str | None = None,
    force: bool = False,
) -> Path | None:
    """Descarga `url` a dest_dir/<fecha>_<archivo>. None si no cambió desde la última vez."""
    prev = latest_for_url(url)
    if prev and not force:
        if remote_last_modified and prev.get("remote_last_modified") == remote_last_modified:
            return None
    headers = {}
    if prev and prev.get("etag") and not force:
        headers["If-None-Match"] = prev["etag"]

    dest_dir.mkdir(parents=True, exist_ok=True)
    name = Path(urlparse(url).path).name or "download"
    stamp = datetime.now(UTC).strftime("%Y%m%d")
    dest = dest_dir / f"{stamp}_{name}"

    r = http.get(url, headers=headers, stream=True)
    if r.status_code == 304:
        return None
    r.raise_for_status()

    h = hashlib.sha256()
    size = 0
    tmp = dest.with_suffix(dest.suffix + ".part")
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
            h.update(chunk)
            size += len(chunk)
    digest = h.hexdigest()
    if prev and prev.get("sha256") == digest and not force:
        tmp.unlink()
        return None
    tmp.rename(dest)

    append_manifest(
        ManifestEntry(
            source_id=source_id,
            url=url,
            path=str(dest),
            fetched_at=datetime.now(UTC).isoformat(timespec="seconds"),
            status=r.status_code,
            bytes=size,
            sha256=digest,
            etag=r.headers.get("ETag"),
            last_modified=r.headers.get("Last-Modified"),
            remote_last_modified=remote_last_modified,
        )
    )
    return dest
