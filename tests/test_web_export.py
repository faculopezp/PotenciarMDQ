import json
from datetime import date

from potenciar_mdq.web_export import _default


def test_fechas_y_decimales_serializables():
    assert json.dumps({"f": date(2025, 1, 2)}, default=_default) == '{"f": "2025-01-02"}'
