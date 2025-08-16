# Project Structure

## Current Organization

```text
.
├── .git/                          # Git version control
├── .github/                       # GitHub workflows and configuration
│   └── workflows/                 # CI/CD pipelines
│       ├── ci.yml                 # Continuous integration
│       └── release-please.yml     # Automated releases
├── .kiro/                         # Kiro AI assistant configuration
│   └── steering/                  # AI guidance documents
├── .vscode/                       # VS Code editor settings
├── scripts/                       # Development and release scripts
│   └── release.sh                 # Release preparation script
├── tests/                         # Test suite
│   └── test_license_header_hook.py
├── license_header_hook.py         # Main hook implementation
├── license-header.txt             # Default license template
├── pyproject.toml                 # Python project configuration
├── uv.lock                        # Dependency lock file
├── .pre-commit-config.yaml        # Pre-commit configuration
├── .pre-commit-hooks.yaml         # Hook definition for distribution
├── release-please-config.json     # Release automation configuration
├── .release-please-manifest.json  # Version tracking
├── Makefile                       # Development commands
├── CHANGELOG.md                   # Release history
└── README.md                      # Project documentation
```

## Core Files

- **license_header_hook.py**: Main Python script containing all hook logic
- **license-header.txt**: Template file for license headers with placeholders
- **pyproject.toml**: Modern Python project configuration with dependencies and metadata
- **uv.lock**: Dependency lock file for reproducible builds

## Configuration Files

- **.pre-commit-config.yaml**: Pre-commit hooks for development workflow
- **.pre-commit-hooks.yaml**: Hook definition for external usage
- **release-please-config.json**: Automated release configuration
- **Makefile**: Development workflow commands

## Architecture Components

- **CommentRegistry**: Maps file extensions to comment styles
- **LicenseHeaderManager**: Core logic for header detection, removal, and insertion
- **CLI Interface**: Argument parsing and file processing coordination

## File Naming Conventions

- Snake_case for Python files following PEP 8
- Kebab-case for configuration files (license-header.txt)
- Clear, descriptive names indicating purpose
- Standard Python project structure with pyproject.toml

## Code Organization Principles

- Single-file implementation for easy deployment
- Class-based architecture with clear separation of concerns
- Minimal external dependencies (Python standard library only)
- Extensible design for adding new comment styles
- Modern Python packaging with uv and pyproject.toml

## Development Workflow

- **uv** for dependency management and virtual environments
- **pytest** for testing with coverage reporting
- **ruff** and **black** for code formatting and linting
- **mypy** for static type checking
- **pre-commit** for automated code quality checks
- **release-please** for automated versioning and releases

## Best Practices

- Keep the main script self-contained for easy distribution
- Template files use clear placeholder syntax ({year}, {copyright_holder})
- Configuration files follow standard formats (TOML, YAML)
- Comprehensive test coverage with pytest
- Automated quality checks with pre-commit hooks
- Semantic versioning with conventional commits
