PY := uv run
.PHONY: setup probe ingest standardize bd qa marts web-data all test lint web-install web-dev web-build

setup:
	uv venv && uv pip install -e ".[dev,pdf]"

probe:
	$(PY) pmdq probe

ingest:
	$(PY) pmdq ingest

standardize:
	$(PY) pmdq standardize

bd:
	$(PY) pmdq bd

qa:
	$(PY) pmdq qa

marts:
	$(PY) pmdq marts

web-data:
	$(PY) pmdq web-data

all:
	$(PY) pmdq all

test:
	$(PY) pytest -q

lint:
	$(PY) ruff check src tests scripts

web-install:
	cd web && npm install

web-dev:
	cd web && npm run dev

web-build:
	cd web && npm run build
