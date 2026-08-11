.PHONY: \
	install \
	download \
	pipeline \
	analysis \
	test \
	test-strict \
	lint \
	quality \
	all \
	reproduce \
	clean

install:
	python -m pip install -e ".[dev]"

download:
	python scripts/download_data.py

pipeline:
	python scripts/run_pipeline.py

analysis:
	python scripts/run_analysis.py

test:
	pytest -q

test-strict:
	pytest -q -W error

lint:
	ruff check .

quality: lint test-strict

all: quality

reproduce: pipeline

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -f .coverage
