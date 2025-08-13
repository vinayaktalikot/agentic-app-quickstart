.PHONY: help install format lint lint-fix clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies using uv"
	@echo "  format       - Format code using black and isort"
	@echo "  lint         - Run linting checks (ruff)"
	@echo "  lint-fix     - Auto-fix linting issues"
	@echo "  clean        - Clean up generated files"

#install dependencies
install:
	@echo "Installing dependencies..."
	uv sync

#format code
format:
	@echo "Formatting code with black..."
	uv run black agentic_app_quickstart/ --line-length 88
	@echo "Sorting imports with isort..."
	uv run isort agentic_app_quickstart/ --profile black

#lint code
lint:
	@echo "Running ruff linter..."
	uv run ruff check agentic_app_quickstart/

#auto-fix linting issues
lint-fix:
	@echo "Auto-fixing linting issues..."
	uv run ruff check --fix agentic_app_quickstart/
	uv run isort agentic_app_quickstart/ --profile black

#cclean up generated files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pkl" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name ".ruff_cache" -delete
	@echo "Cleanup complete!"

#quick quality check
quality: format lint-fix
	@echo "Code quality improvements applied!" 