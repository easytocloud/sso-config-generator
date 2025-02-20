.PHONY: clean build install test lint format

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

install: clean
	pip install -e .

test:
	pytest tests/

lint:
	flake8 src/
	pylint src/
	mypy src/

format:
	black src/
	isort src/

dev-setup:
	pip install -e ".[dev]"
	pre-commit install

# Default target
all: clean lint test build
