# Tests for Chimera Cookiecutter Template

This directory contains tests for the Cookiecutter template to ensure generated projects are valid and working correctly.

## Running Tests

### Using uv (recommended)

```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_template.py::test_cookiecutter_template_basic -v
```

### Using pip

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## What Gets Tested

The test suite validates:

1. **Template Generation**: Basic cookiecutter execution works
2. **Project Structure**: All expected files and directories are created
3. **Conditional Components**: Instruments/controllers are included/excluded based on settings
4. **File Content**: Generated files have correct content with no Jinja2 artifacts
5. **SPDX Headers**: All Python files have proper license identifiers
6. **Configuration Files**: pyproject.toml is valid TOML
7. **Custom Values**: Template variables are properly substituted
8. **Package Build**: Generated project structure is valid for building

## Test Organization

- `test_template.py`: Main test suite for the Cookiecutter template
- Fixtures provide temporary directories for cookiecutter output
- Each test cleans up after itself

## Continuous Integration

Tests run automatically on:
- Push to master/main branches
- Pull requests to master/main branches

See `.github/workflows/test.yml` for CI configuration.
