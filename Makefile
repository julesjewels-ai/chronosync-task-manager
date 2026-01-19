.PHONY: help install lint format test coverage build clean

help:
	@echo "Available targets:"
	@echo "  make install  - Install dependencies"
	@echo "  make lint     - Run linting"
	@echo "  make format   - Format code"
	@echo "  make test     - Run tests"
	@echo "  make coverage - Run tests with coverage"
	@echo "  make build    - Build package"

install:
	pip install -r requirements.txt
	pip install ruff black isort pytest pytest-cov

lint:
	@echo "Running ruff..."
	ruff check src/ tests/ --fix || ruff check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

test:
	pytest tests/ -v --tb=short

coverage:
	pytest tests/ -v --cov=src --cov-report=term-missing

coverage-check:
	pytest tests/ --cov=src --cov-fail-under=80

build:
	@if [ -f "pyproject.toml" ]; then python -m build; else python -c "import src"; fi

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
