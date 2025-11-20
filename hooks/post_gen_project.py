#!/usr/bin/env python
"""Post-generation hook for cookiecutter template."""

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    """Remove a file."""
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dirpath):
    """Remove a directory."""
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))


if __name__ == "__main__":
    # Remove instrument files if not needed
    if "{{ cookiecutter.include_instrument }}" != "yes":
        remove_dir("src/{{ cookiecutter.package_name }}/instruments")

    # Remove controller files if not needed
    if "{{ cookiecutter.include_controller }}" != "yes":
        remove_dir("src/{{ cookiecutter.package_name }}/controllers")

    print()
    print("=" * 60)
    print("Your Chimera plugin has been created successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. cd {{ cookiecutter.package_name }}")
    print("  2. git init")
    print("  3. uv sync")
    print("  4. uv run pre-commit install --install-hooks")
    print("  5. git add .")
    print("  6. git commit -m 'Initial commit'")
    print()
    print("Happy coding!")
    print()
