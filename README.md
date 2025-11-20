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
cookiecutter gh:astroufsc/chimera-template
```

Or if you've cloned this repository locally:

```bash
cookiecutter /path/to/chimera-template
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
