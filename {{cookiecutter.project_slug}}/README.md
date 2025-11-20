# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

This is a plugin for the [Chimera observatory control system](https://github.com/astroufsc/chimera).

## Installation

```bash
pip install -U {{ cookiecutter.package_name }}
```

Or install from source:

```bash
pip install -U git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

## Configuration Example

Add the following to your `chimera.config` file:

{% if cookiecutter.include_instrument == "yes" %}
```yaml
instrument:
    name: {{ cookiecutter.project_slug }}
    type: {{ cookiecutter.__instrument_class_name }}
```
{% endif %}

{% if cookiecutter.include_controller == "yes" %}
```yaml
controller:
    name: {{ cookiecutter.project_slug }}
    type: {{ cookiecutter.__controller_class_name }}
```
{% endif %}

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

This project uses:
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [pre-commit](https://pre-commit.com/) for automated checks

```bash
# Run linter
uv run ruff check

# Run formatter
uv run ruff format

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

## License

{{ cookiecutter.license }}

## Contact

For more information, contact us on chimera's discussion list:
https://groups.google.com/forum/#!forum/chimera-discuss

Bug reports and patches are welcome and can be sent over our GitHub page:
https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
