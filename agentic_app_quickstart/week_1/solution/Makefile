.PHONY: help test lint format clean install-deps

# default target
help:
	@echo "available targets:"
	@echo "  test     - run all tests"
	@echo "  lint     - run linting checks"
	@echo "  format   - format code with black"
	@echo "  clean    - clean up temporary files"
	@echo "  install-deps - install development dependencies"

# install development dependencies
install-deps:
	@echo "installing development dependencies..."
	uv pip install black flake8 pytest

# run tests
test:
	@echo "running tests..."
	uv run python -m pytest tests/ -v

# run tests with coverage (if pytest-cov is installed)
test-cov:
	@echo "running tests with coverage..."
	uv run python -m pytest tests/ -v --cov=. --cov-report=term-missing

# run linting
lint:
	@echo "running linting checks..."
	uv run flake8 . --max-line-length=100 --ignore=E501,W503
	@echo "✓ linting passed"

# format code
format:
	@echo "formatting code with black..."
	uv run black . --line-length=100
	@echo "✓ code formatting complete"

# check formatting without changing files
format-check:
	@echo "checking code formatting..."
	uv run black . --line-length=100 --check
	@echo "✓ code formatting is correct"

# clean up temporary files
clean:
	@echo "cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✓ cleanup complete"

# run all quality checks
quality: lint format-check test
	@echo "✓ all quality checks passed"

# quick development cycle
dev: format lint test
	@echo "✓ development cycle complete" 