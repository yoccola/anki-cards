.PHONY: help install test lint format clean run check-all

help:
	@echo "Available commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run flake8 linter"
	@echo "  make format     - Format code with black"
	@echo "  make mypy       - Run type checking"
	@echo "  make clean      - Remove cache files"
	@echo "  make run        - Run the main script"
	@echo "  make check-all  - Run all checks (lint, format check, mypy, test)"

install:
	pip install -r requirements.txt

test:
	pytest -v --cov=. --cov-report=html --cov-report=term-missing

lint:
	flake8 . --max-line-length=100 --exclude=venv,__pycache__

format:
	black . --line-length=100 --exclude=venv

format-check:
	black . --line-length=100 --check --exclude=venv

mypy:
	mypy . --ignore-missing-imports

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

run:
	python update_etymology.py

check-all: format-check lint mypy test