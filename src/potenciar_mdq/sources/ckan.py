"""Cliente mínimo CKAN / Portal Andino (datos.gob.ar, datos.transporte, datos.yvera)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from potenciar_mdq.http import PoliteSession


class CkanError(RuntimeError):
    pass


@dataclass
class Resource:
    id: str
    name: str
    format: str
    url: str
    last_modified: str | None
    size: int | None


class CkanClient:
    def __init__(self, base_url: str, http: PoliteSession, api_prefix: str = "/api/3/action"):
        self.base_url = base_url.rstrip("/")
        self.api = f"{self.base_url}{api_prefix}"
        self.http = http

    def action(self, name: str, **params) -> dict | list:
        payload = self.http.get_json(f"{self.api}/{name}", params=params)
        if not payload.get("success", False):
            raise CkanError(f"{name} falló en {self.base_url}: {payload.get('error')}")
        return payload["result"]

    def status(self) -> dict:
        return self.action("status_show")

    def package_show(self, dataset: str) -> dict:
        return self.action("package_show", id=dataset)

    def package_search(
        self, q: str = "*:*", fq: str | None = None, rows: int = 100
    ) -> Iterator[dict]:
        start = 0
        while True:
            params = {"q": q, "rows": rows, "start": start}
            if fq:
                params["fq"] = fq
            result = self.action("package_search", **params)
            yield from result["results"]
            start += rows
            if start >= result["count"]:
                break

    def resources(self, dataset: str, formats: list[str] | None = None) -> list[Resource]:
        pkg = self.package_show(dataset)
        wanted = {f.lower() for f in formats} if formats else None
        out = []
        for r in pkg.get("resources", []):
            fmt = (r.get("format") or "").lower()
            if wanted and fmt not in wanted:
                continue
            out.append(
                Resource(
                    id=r["id"],
                    name=r.get("name") or r["id"],
                    format=fmt,
                    url=r["url"],
                    last_modified=r.get("last_modified") or r.get("metadata_modified"),
                    size=r.get("size"),
                )
            )
        return out

    def datastore_search(self, resource_id: str, limit: int = 1000) -> Iterator[dict]:
        """Filas vía API (solo si el recurso está en DataStore)."""
        offset = 0
        while True:
            result = self.action(
                "datastore_search", resource_id=resource_id, limit=limit, offset=offset
            )
            records = result.get("records", [])
            yield from records
            offset += limit
            if not records or offset >= result.get("total", 0):
                break

    def dcat_catalog(self) -> dict:
        """Catálogo completo en DCAT (Portal Andino expone /data.json)."""
        return self.http.get_json(f"{self.base_url}/data.json")
