.PHONY: help install dev test lint format clean runserver migrate create-superuser

# Variables
PYTHON := python
PIP := pip
MANAGE := python manage.py

help:
	@echo "YatraAI Development Commands"
	@echo "============================"
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Install dev dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make create-superuser - Create admin user"
	@echo ""
	@echo "Development:"
	@echo "  make runserver     - Start development server"
	@echo "  make test          - Run test suite"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run linters (Flake8)"
	@echo "  make format        - Format code with Black"
	@echo "  make format-check  - Check formatting without changes"
	@echo "  make sort-imports  - Sort imports with isort"
	@echo ""
	@echo "Database:"
	@echo "  make migrations    - Create new migrations"
	@echo "  make load-fixtures - Load sample Nepal data"
	@echo "  make reset-db      - Reset database (dev only)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove Python cache files"
	@echo "  make clean-all     - Remove all generated files and cache"

install:
	$(PIP) install -r requirements.txt

dev:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

migrate:
	$(MANAGE) migrate

create-superuser:
	$(MANAGE) createsuperuser

runserver:
	$(MANAGE) runserver

test:
	$(MANAGE) test

test-coverage:
	pytest --cov=apps --cov=config --cov-report=html --cov-report=term-missing

lint:
	flake8 apps config --max-line-length=100

format:
	black apps config templates static

format-check:
	black --check apps config templates static

sort-imports:
	isort apps config

migrations:
	$(MANAGE) makemigrations

load-fixtures:
	$(MANAGE) loaddata fixtures/nepal_locations.json

reset-db:
	rm -f db.sqlite3
	$(MANAGE) migrate
	$(MANAGE) createsuperuser

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

.DEFAULT_GOAL := help
