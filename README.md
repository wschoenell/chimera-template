# Chimera Plugin Template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for creating [Chimera](https://github.com/astroufsc/chimera) observatory control system plugins.

This template provides a modern, fully-configured project structure following current Python best practices, including:

- **Modern src/ layout** for better packaging
- **Type hints** on all method definitions
- **Ruff** for linting and formatting
- **Pre-commit hooks** for automated code quality checks
- **SPDX license identifiers** for clear licensing
- **Comprehensive documentation** structure
- **Test structure** ready to use

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

## Quick Start

### Install Cookiecutter

```bash
# Using uv (recommended)
uv tool install cookiecutter

# Or using pip
pip install cookiecutter
```

### Create a New Plugin

```bash
uv tool run cookiecutter gh:astroufsc/chimera-template
```

Or if you've cloned this repository locally:

```bash
uv tool run cookiecutter /path/to/chimera-template
```

### Follow the Prompts

You'll be asked to provide:

- **project_name**: Human-readable name (e.g., "My Telescope Controller")
- **project_slug**: URL/import-friendly version (auto-generated)
- **package_name**: Python package name with `chimera_` prefix (auto-generated)
- **project_short_description**: Brief description of your plugin
- **author_name**: Your name
- **author_email**: Your email address
- **github_username**: Your GitHub username
- **version**: Initial version (default: 0.1.0)
- **license**: Choose from GPL-2.0-or-later, MIT, BSD-3-Clause, Apache-2.0
- **python_version**: Minimum Python version (default: 3.13)
- **include_instrument**: Include an instrument template? (yes/no)
- **include_controller**: Include a controller template? (yes/no)

### Initialize Your New Plugin

After generation, follow these steps:

```bash
cd your-package-name
git init
uv sync
uv run pre-commit install --install-hooks
git add .
git commit -m "Initial commit"
```

## Migrating an Existing Plugin

If you have an existing Chimera plugin and want to adopt this template structure, the best approach is to set it up from scratch in the existing plugin directory:

```bash
# Navigate to your existing plugin directory
cd /path/to/your-existing-plugin

# Run cookiecutter to set up the template
uv tool run cookiecutter gh:astroufsc/chimera-template
```

Cookiecutter will ask you questions about your plugin. Answer them according to your existing plugin's configuration. After generation, you can:

1. Review the generated files in the new directory
2. Manually merge your existing code into the new structure
3. Adopt the modern `src/` layout
4. Add pre-commit hooks and update to `pyproject.toml` configuration
5. Integrate SPDX license headers and type hints

This approach gives you full control over the migration process and allows you to selectively adopt new features while preserving your existing code.

## Project Structure

The generated project will have this structure:

```
your-package-name/
├── src/
│   └── chimera_your_plugin/
│       ├── __init__.py
│       ├── instruments/          # If included
│       │   ├── __init__.py
│       │   └── your_plugin.py
│       └── controllers/          # If included
│           ├── __init__.py
│           └── your_plugin.py
├── tests/
│   ├── __init__.py
│   └── chimera_your_plugin/
│       └── __init__.py
├── pyproject.toml
├── README.md
├── .pre-commit-config.yaml
└── .gitignore
```

## Development Workflow

### Code Quality

The template includes pre-configured tools:

```bash
# Run linter
uv run ruff check

# Auto-fix issues
uv run ruff check --fix

# Format code
uv run ruff format

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### Testing

```bash
# Run tests (when you add them)
uv run pytest
```

## Features

### Modern Python Practices

- **Type annotations**: All methods include type hints
- **f-strings**: Modern string formatting throughout
- **super()**: Modern inheritance patterns
- **Docstrings**: Google-style docstrings for all classes and methods

### Code Quality Tools

- **Ruff**: Fast Python linter and formatter
- **Pre-commit**: Automated checks before each commit
- **SPDX identifiers**: Clear license and copyright information

### Project Structure

- **src/ layout**: Modern packaging best practice
- **tests/ directory**: Parallel structure for test organization
- **pyproject.toml**: Modern Python project configuration (no setup.py)

## Chimera Plugin Development

For detailed information about developing Chimera plugins:

- [Chimera Documentation](https://github.com/astroufsc/chimera)
- [Chimera Developer Guide](https://github.com/astroufsc/chimera/blob/master/docs/site/chimerafordevs.rst)

### Important Notes

- Plugin package names **must** start with `chimera_` to be discovered by Chimera
- Instrument files go in `src/chimera_yourplugin/instruments/`
- Controller files go in `src/chimera_yourplugin/controllers/`
- Class names should use CamelCase (e.g., `MyTelescopeController`)

## Contributing to This Template

Found a bug or have a suggestion? Please open an issue or submit a pull request!

## License

This template is licensed under GPL-2.0-or-later.

Generated projects can use any license selected during generation.

## Contact

For more information:

- Chimera discussion list: https://groups.google.com/forum/#!forum/chimera-discuss
- GitHub: https://github.com/astroufsc/chimera-template

## Development & Testing

This template itself is tested to ensure generated projects are valid and working.

### Running Template Tests

```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

See `tests/README.md` for more information about the test suite.
