# Makefile for Multi-Agent CLM System

.PHONY: help install test lint format clean run setup

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Complete setup (install + env)"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean generated files"
	@echo "  make run        - Run the application"
	@echo "  make notebook   - Start Jupyter notebook"

install:
	pip install -r requirements.txt

setup: install
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your API keys."; \
	else \
		echo ".env file already exists"; \
	fi
	@echo "Setup complete!"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-fast:
	pytest tests/ -v --tb=short

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

run:
	python src/main.py

notebook:
	jupyter notebook notebooks/

# Development helpers
dev-install:
	pip install -e .
	pip install -r requirements.txt

check: format lint test
	@echo "All checks passed!"
