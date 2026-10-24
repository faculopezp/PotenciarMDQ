"""Cliente DKAN 7.x (datos.mardelplata.gob.ar). API compatible CKAN + DataStore propio."""

from __future__ import annotations

from collections.abc import Iterator

from potenciar_mdq.http import PoliteSession
from potenciar_mdq.sources.ckan import CkanClient, CkanError


class DkanClient(CkanClient):
    def __init__(self, base_url: str, http: PoliteSession):
        super().__init__(base_url, http)
        self._resolved = False

    def action(self, name: str, **params) -> dict | list:
        # Drupal sin clean URLs responde en /?q=api/3/action/...; probamos ambas una vez.
        try:
            return super().action(name, **params)
        except Exception:
            if self._resolved:
                raise
            self._resolved = True
            self.api = f"{self.base_url}/?q=api/3/action"
            return super().action(name, **params)

    def package_list(self) -> list[str]:
        return self.action("package_list")

    def search_titles(self, terms: list[str]) -> list[str]:
        terms = [t.lower() for t in terms]
        return [slug for slug in self.package_list() if any(t in slug.lower() for t in terms)]

    def datastore_search(self, resource_id: str, limit: int = 100) -> Iterator[dict]:
        offset = 0
        url = f"{self.base_url}/api/action/datastore/search.json"
        while True:
            payload = self.http.get_json(
                url, params={"resource_id": resource_id, "limit": limit, "offset": offset}
            )
            if not payload.get("success", False):
                raise CkanError(f"datastore DKAN falló: {payload.get('error')}")
            records = payload["result"].get("records", [])
            yield from records
            offset += limit
            if not records or offset >= int(payload["result"].get("total", 0)):
                break
