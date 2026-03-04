---
title: Python Coding Conventions
description: Standard operating procedures for Python development, including `uv` workflow, modular architecture, and preferred libraries (Rich, LiteLLM, HTTPX).
last_updated: 2025-12-17
version: 2.0
tags:
  - python
  - conventions
  - uv
  - architecture
  - best-practices
---
# Python Coding Conventions

## General

- **Python version**: 3.12+
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

## Development Workflow & `uv` Usage

This project uses **`uv`** as the all-in-one tool for managing the virtual environment and dependencies. It is the required replacement for `pip`, `venv`, and `requirements.txt`.

### 1. Initial Project Setup

Run these commands only once after cloning the repository.

1.  **Create the Virtual Environment:** `uv` will create a `.venv` directory in the project root.
    ```bash
    uv venv
    ```

2.  **Activate the Environment:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Install All Dependencies:** This installs the project in editable mode (`-e`) along with all development dependencies (`[dev]`) defined in `pyproject.toml`.
    ```bash
    uv pip install -e ".[dev]"
    ```
    *(Note: Do not run `uv init`. The project is already initialized.)*

**Alternatively (Recommended One-Liner):**

After creating the environment with `uv venv`, you can activate and install in a single step:
```bash
source .venv/bin/activate && uv pip install -e ".[dev]"