.PHONY: help install dev test lint format type-check build clean release

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	uv sync

dev: ## Install development dependencies
	uv sync --dev

test: ## Run tests
	uv run pytest --cov=license_header_hook --cov-report=term-missing

test-verbose: ## Run tests with verbose output
	uv run pytest -v --cov=license_header_hook --cov-report=term-missing

lint: ## Run linting
	uv run ruff check .

lint-fix: ## Run linting with auto-fix
	uv run ruff check --fix .

format: ## Format code
	uv run ruff format .

format-check: ## Check code formatting
	uv run ruff format --check .

type-check: ## Run type checking
	uv run mypy license_header_hook.py

pre-commit: ## Run pre-commit hooks
	uv run pre-commit run --all-files

build: ## Build the package
	uv build

clean: ## Clean build artifacts
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

release: ## Prepare for release (run tests, linting, build)
	./scripts/release.sh

ci: lint format-check type-check test ## Run all CI checks

setup-dev: dev ## Setup development environment
	uv run pre-commit install
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands."
