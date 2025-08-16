# Technology Stack

## Language & Runtime
- **Python 3.12+**: Core implementation language (modern Python features)
- **Standard Library Only**: No external dependencies for maximum compatibility
- **uv**: Modern Python package manager for development

## Build System
- **uv**: Package management and virtual environment handling
- **Hatchling**: Build backend for PyPI distribution
- **pyproject.toml**: Modern Python project configuration
- **GitHub Actions**: CI/CD pipeline with automated testing and releases

## Development Environment
- VS Code configuration present
- Kiro AI assistant integration configured
- Git version control initialized
- Pre-commit hooks for code quality
- **uv** for dependency management and virtual environments

## Package Management
```bash
# Install dependencies
uv sync --dev

# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Run commands in virtual environment
uv run command
```

## Common Commands

### Development Setup
```bash
# Setup development environment
make setup-dev

# Install dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Development Workflow
```bash
# Run tests
make test
uv run pytest

# Run linting and formatting
make lint
make format
uv run ruff check --fix .
uv run ruff format .

# Type checking
make type-check
uv run mypy license_header_hook.py

# Run all CI checks
make ci
```

### Building and Release
```bash
# Build package
make build
uv build

# Prepare release
make release
./scripts/release.sh

# Manual PyPI upload (if needed)
uv publish --token $PYPI_TOKEN
```

### Hook Usage
```bash
# Run the hook directly
uv run python license_header_hook.py --template license-header.txt --copyright-holder "Company" file.py

# Install as pre-commit hook
uv run pre-commit install
uv run pre-commit run license-header --all-files
```

## Dependencies
- **Runtime**: Python standard library only
- **Development**: pytest, ruff (linting + formatting), mypy, pre-commit
- **Build**: hatchling for PyPI packaging
- **CI/CD**: GitHub Actions with release-please automation

## Release Process
- **release-please**: Automated version bumping and changelog generation
- **Conventional Commits**: Semantic versioning based on commit messages
- **PyPI Publishing**: Automated publication on release creation
- **GitHub Releases**: Automatic release notes and asset management

## File Extensions Supported
Python (.py), JavaScript (.js, .ts), Java (.java), C/C++ (.c, .cpp, .h), Go (.go), Rust (.rs), Shell (.sh), CSS (.css), HTML (.html), YAML (.yml)

## Quality Metrics
- **Test Coverage**: 80% with comprehensive test suite
- **Code Quality**: All ruff and mypy checks passing (ruff-only formatting)
- **CI/CD**: Automated testing across Python 3.12-3.13
- **Documentation**: Complete README with usage examples
- **Modern Python**: Uses Python 3.12+ features and type annotations