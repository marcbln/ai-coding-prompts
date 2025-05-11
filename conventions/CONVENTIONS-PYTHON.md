# Python Coding Conventions

## General

- **Python version**: 3.10+
- **Type hints**: Mandatory for functions and class methods
- **Style**: Follow [PEP8](https://peps.python.org/pep-0008/) and [PEP257](https://peps.python.org/pep-0257/)
- **Documentation**: Use docstrings for modules, classes, and functions
- **Naming**:
  - `snake_case` for functions/variables/modules
  - `PascalCase` for classes
  - `UPPERCASE` for constants
- **F-strings**: Preferred for string formatting
- **Imports**: Group imports in the following order with a blank line between groups:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

## Project Structure

- Organize code in a modular structure with clear separation of concerns
- Use package layout with properly defined `__init__.py` files
- Follow the structure:
  ```
  git_summarize/
  ├── __init__.py
  ├── cli.py          # Command-line interface
  ├── core/           # Core business logic
  ├── utils/          # Utility functions
  └── config.py       # Configuration handling
  ```
- Avoid placing all code into a single file; organize into multiple modules

## Testing and Quality

- **Unit tests**: Required for all new functionality
- **Test framework**: pytest
- **Coverage**: Aim for at least 80% test coverage
- **Code quality**: Use tools like flake8, mypy, and black

## Dependencies

- Keep dependencies minimal and justified
- Use the specified frameworks/libraries where appropriate:
  - **Typer**: CLI interface with type hints (as used in project)
  - **Rich**: Terminal output formatting (as used in project)
  - **Inquirer**: Interactive CLI prompts (as used in project)
  - **PyYAML**: Configuration file handling (as used in project)
  - **FastAPI**: For web APIs (if needed)
  - **Pydantic**: Data validation (recommended for OpenAI API interactions)
  - **SQLAlchemy**: For database interactions (if needed)

## CLI Development

- Use Typer for all CLI functionality
- Implement comprehensive `--help` documentation
- Provide meaningful error messages
- Support configuration via both CLI arguments and config files
- Follow the pattern established in `cli.py` with the app object

## API Interactions

- Isolate API client code into dedicated modules
- Use environment variables for API keys and configuration
- Implement proper error handling and rate limiting awareness
- Cache results where appropriate to reduce API calls

## Configuration

- Use YAML for configuration files
- Support both global (user home) and local (project directory) configuration
- Implement fallbacks for missing configuration values

## Example pyproject.toml

A minimal working example:

```toml
# pyproject.toml
[project]
name = "topdata-package-release-builder"
version = "0.1.0"
description = "Build and package Shopware 6 plugins for release"
requires-python = ">=3.8"
dependencies = [
    "rich>=13.0.0",
    "click>=8.0.0",
    "pytz",
    "python-dotenv",
    "InquirerPy>=0.3.4",
    "requests",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
sw-build = "topdata_package_release_builder.cli:main"
```

