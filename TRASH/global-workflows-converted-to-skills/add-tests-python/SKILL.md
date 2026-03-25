---
name: add-tests-python
description: "Generate, execute, and refine unit tests for Python modules using `pytest`. Ensure the generated tests strictly adher..."
---

# Workflow: Add Python Tests (pytest)

## Objective
Generate, execute, and refine unit tests for Python modules using `pytest`. Ensure the generated tests strictly adhere to the project's Python coding conventions, utilizing `uv` for dependency and execution management, enforcing strict type hinting, and targeting a minimum of 80% test coverage.

## 1. Prerequisites & Environment Check
Before generating tests, verify the development environment:
- Ensure the project is using `uv`. Do NOT use `pip`, `venv`, or `requirements.txt`.
- Check if `pytest`, `pytest-cov`, `black`, `ruff`, and `mypy` are in `pyproject.toml` under `[project.optional-dependencies.dev]`.
- If missing, ask the user or automatically add them using:
  ```bash
  uv add --dev pytest pytest-cov
  ```

## 2. Analyze the Target Code
- Identify the functions, classes, and methods in the target file.
- Determine the required edge cases, expected exceptions, and happy paths.
- Identify dependencies (API clients, database calls, I/O) that must be mocked.

## 3. Test File Location and Naming
- Place tests in a `tests/` directory (or the designated test directory).
- Mirror the target module's name with a `test_` prefix (e.g., testing `core/logic.py` -> `tests/test_logic.py`).
- Use `snake_case` for test function names (e.g., `def test_calculate_total_with_valid_input() -> None:`).
- Use `PascalCase` if grouping tests in classes (e.g., `class TestCalculateTotal:`).

## 4. Test Implementation Rules (Strict Conventions)
When writing the test code, adhere to the following project guidelines:

### A. Imports
Group imports with a blank line between them exactly in this order:
1. Standard library imports (e.g., `import os`, `from unittest.mock import patch, MagicMock`)
2. Third-party imports (e.g., `import pytest`)
3. Local application imports (e.g., `from core.logic import calculate_total`)

### B. Type Hints & Docstrings
- **Mandatory**: Every test function must include a return type hint of `-> None`.
- **Mandatory**: Every fixture must include proper type hints for its return value.
- Include a descriptive docstring (PEP257) for test classes and complex test functions.

### C. `pytest` Features
- Use **`@pytest.fixture`** for reusable setup code, state, or mock objects.
- Use **`@pytest.mark.parametrize`** for testing multiple inputs/outputs to keep code DRY.
- Use `pytest.raises` to test expected exceptions.
- Prefer f-strings for customized assertion failure messages (if needed).

## 5. Execution & Validation
Once the tests are written, execute them using `uv` to ensure they pass and meet coverage requirements.

1. **Run the specific tests**:
   ```bash
   uv run pytest tests/test_<module_name>.py -v
   ```
2. **Check Test Coverage** (Must be >= 80%):
   ```bash
   uv run pytest tests/test_<module_name>.py --cov=<target_module_path> --cov-report=term-missing
   ```
3. **Quality Checks**:
   Ensure the newly written test file passes the project's formatting and linting rules:
   ```bash
   uv run black tests/test_<module_name>.py
   uv run ruff check tests/test_<module_name>.py
   uv run mypy tests/test_<module_name>.py
   ```

## 6. Template Example
Use this structure as a baseline for new test files:

```python
"""Tests for the <module_name> module."""

from unittest.mock import MagicMock, patch

import pytest

from <project_name>.<module_path> import <TargetClass>, <target_function>


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample data for testing."""
    return {"key": "value"}


def test_target_function_success(sample_data: dict[str, str]) -> None:
    """Test that target_function returns expected results given valid input."""
    # Arrange
    expected = "processed_value"
    
    # Act
    result = target_function(sample_data)
    
    # Assert
    assert result == expected, f"Expected {expected}, but got {result}"


@pytest.mark.parametrize(
    "input_val, expected_err",
    [
        ("", ValueError),
        (None, TypeError),
    ]
)
def test_target_function_exceptions(input_val: any, expected_err: type[Exception]) -> None:
    """Test that target_function raises proper exceptions on invalid input."""
    with pytest.raises(expected_err):
        target_function(input_val)
```

## 7. Iterate
If the tests fail, or if the test coverage for the target file is below 80%:
1. Analyze the failure or missing coverage lines.
2. Update the code or add new tests to cover missing branches.
3. Re-run Step 5 until the tests pass and >80% coverage is achieved.
