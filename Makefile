PYTHON ?= python
PYTHON_MINOR := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')")
LOCK_FILE ?= requirements/lock-py$(PYTHON_MINOR).txt

.PHONY: install install-editable download pipeline analysis test lint format-check audit \
	evidence-check notebook-check quality build wheel-smoke reproduce all clean

install:
	$(PYTHON) -m pip install -r $(LOCK_FILE)
	$(PYTHON) -m pip install --no-deps --no-build-isolation .

install-editable:
	$(PYTHON) -m pip install -r $(LOCK_FILE)
	$(PYTHON) -m pip install --no-deps --no-build-isolation -e .

download:
	$(PYTHON) scripts/download_data.py

pipeline:
	$(PYTHON) scripts/run_pipeline.py

analysis:
	$(PYTHON) scripts/run_analysis.py

test:
	$(PYTHON) -m pytest -q -W error

lint:
	$(PYTHON) -m ruff check .

format-check:
	$(PYTHON) -m ruff format --check .

audit:
	$(PYTHON) scripts/audit_repository.py

evidence-check:
	$(PYTHON) scripts/validate_reports.py

notebook-check:
	$(PYTHON) scripts/execute_notebook.py

quality: lint format-check test audit evidence-check notebook-check

build:
	$(PYTHON) -m build --no-isolation

wheel-smoke: build
	$(PYTHON) scripts/wheel_smoke.py

reproduce: evidence-check notebook-check

all: quality build

clean:
	rm -rf .pytest_cache .ruff_cache build dist htmlcov
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -f .coverage
