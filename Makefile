.PHONY: clean build install test lint format uv-venv uv-install uv-run

# UV environment variables
UV_VENV := .venv
PYTHON := $(UV_VENV)/bin/python

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(UV_VENV)

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

# UV-specific targets
uv-venv:
	uv venv $(UV_VENV)

uv-install: uv-venv
	uv pip install -e .
	uv pip install boto3 click pyyaml

uv-run: uv-install
	VIRTUAL_ENV=$(UV_VENV) PATH=$(UV_VENV)/bin:$$PATH AWS_DEFAULT_REGION=eu-west-1 python -m sso_config_generator.cli generate

uv-clean:
	rm -rf $(UV_VENV)

# Default target
all: clean lint test build

# UV default target
uv: uv-run
