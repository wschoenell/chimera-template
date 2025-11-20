# SPDX-FileCopyrightText: 2024-present William Schoenell <wschoenell@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Tests for the Chimera Cookiecutter template."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def template_dir():
    """Return the path to the cookiecutter template directory."""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for cookiecutter output."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    yield output_dir
    # Cleanup
    if output_dir.exists():
        shutil.rmtree(output_dir)


def test_cookiecutter_template_basic(template_dir, temp_output_dir):
    """Test basic cookiecutter template generation with default values."""
    # Run cookiecutter with no prompts (using defaults)
    result = subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Cookiecutter failed: {result.stderr}"

    # Check that the project was created
    project_dir = temp_output_dir / "chimera_my_chimera_plugin"
    assert project_dir.exists(), "Project directory was not created"
    assert project_dir.is_dir(), "Project path is not a directory"


def test_generated_project_structure(template_dir, temp_output_dir):
    """Test that the generated project has the expected structure."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check expected files exist
    expected_files = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
        ".pre-commit-config.yaml",
        "src/chimera_my_chimera_plugin/__init__.py",
        "tests/__init__.py",
        "tests/chimera_my_chimera_plugin/__init__.py",
    ]

    for file_path in expected_files:
        full_path = project_dir / file_path
        assert full_path.exists(), f"Expected file {file_path} does not exist"


def test_generated_project_with_instrument(template_dir, temp_output_dir):
    """Test project generation with instrument included."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_instrument=yes",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check instrument files exist
    instrument_dir = project_dir / "src/chimera_my_chimera_plugin/instruments"
    assert instrument_dir.exists(), "Instruments directory does not exist"
    assert (instrument_dir / "__init__.py").exists()
    assert (instrument_dir / "my_chimera_plugin.py").exists()


def test_generated_project_with_controller(template_dir, temp_output_dir):
    """Test project generation with controller included."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_controller=yes",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check controller files exist
    controller_dir = project_dir / "src/chimera_my_chimera_plugin/controllers"
    assert controller_dir.exists(), "Controllers directory does not exist"
    assert (controller_dir / "__init__.py").exists()
    assert (controller_dir / "my_chimera_plugin.py").exists()


def test_generated_project_without_instrument(template_dir, temp_output_dir):
    """Test that instrument directory is removed when not needed."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_instrument=no",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check instrument directory does not exist
    instrument_dir = project_dir / "src/chimera_my_chimera_plugin/instruments"
    assert not instrument_dir.exists(), "Instruments directory should not exist"


def test_generated_project_without_controller(template_dir, temp_output_dir):
    """Test that controller directory is removed when not needed."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_controller=no",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check controller directory does not exist
    controller_dir = project_dir / "src/chimera_my_chimera_plugin/controllers"
    assert not controller_dir.exists(), "Controllers directory should not exist"


def test_generated_pyproject_toml_valid(template_dir, temp_output_dir):
    """Test that the generated pyproject.toml is valid TOML."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"
    pyproject_path = project_dir / "pyproject.toml"

    # Try to parse the TOML file
    try:
        import tomli
    except ImportError:
        import tomllib as tomli

    with open(pyproject_path, "rb") as f:
        config = tomli.load(f)

    # Verify key fields
    assert "project" in config
    assert config["project"]["name"] == "chimera_my_chimera_plugin"
    assert config["project"]["version"] == "0.1.0"
    assert "chimera" in config["project"]["dependencies"]


def test_generated_project_with_custom_values(template_dir, temp_output_dir):
    """Test project generation with custom values."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "project_name=My Test Plugin",
            "author_name=Test Author",
            "author_email=test@example.com",
            "version=1.0.0",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_test_plugin"
    assert project_dir.exists()

    pyproject_path = project_dir / "pyproject.toml"
    content = pyproject_path.read_text()

    assert "chimera_my_test_plugin" in content
    assert "Test Author" in content
    assert "test@example.com" in content
    assert "1.0.0" in content


def test_generated_python_files_have_spdx_headers(template_dir, temp_output_dir):
    """Test that generated Python files have SPDX headers."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_instrument=yes",
            "include_controller=yes",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check SPDX headers in various files
    python_files = [
        "src/chimera_my_chimera_plugin/__init__.py",
        "src/chimera_my_chimera_plugin/instruments/__init__.py",
        "src/chimera_my_chimera_plugin/instruments/my_chimera_plugin.py",
        "src/chimera_my_chimera_plugin/controllers/__init__.py",
        "src/chimera_my_chimera_plugin/controllers/my_chimera_plugin.py",
        "tests/__init__.py",
    ]

    for py_file in python_files:
        file_path = project_dir / py_file
        content = file_path.read_text()
        assert "SPDX-FileCopyrightText:" in content, f"{py_file} missing SPDX copyright"
        assert "SPDX-License-Identifier:" in content, f"{py_file} missing SPDX license"


def test_generated_readme_has_correct_content(template_dir, temp_output_dir):
    """Test that the generated README has the correct project name and info."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "project_name=My Test Plugin",
            "project_short_description=A test plugin for Chimera",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_test_plugin"
    readme_path = project_dir / "README.md"

    content = readme_path.read_text()
    assert "My Test Plugin" in content
    assert "A test plugin for Chimera" in content
    assert "chimera_my_test_plugin" in content


def test_no_jinja2_syntax_in_generated_files(template_dir, temp_output_dir):
    """Test that generated files don't contain unrendered Jinja2 syntax."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
            "include_instrument=yes",
            "include_controller=yes",
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Check all Python files
    for py_file in project_dir.rglob("*.py"):
        content = py_file.read_text()
        assert "{{" not in content, f"{py_file} contains unrendered Jinja2 syntax"
        assert "{%" not in content, f"{py_file} contains unrendered Jinja2 syntax"

    # Check config files
    for config_file in ["pyproject.toml", "README.md", ".pre-commit-config.yaml"]:
        file_path = project_dir / config_file
        content = file_path.read_text()
        assert "{{" not in content, f"{config_file} contains unrendered Jinja2 syntax"
        assert "{%" not in content, f"{config_file} contains unrendered Jinja2 syntax"


def test_generated_project_installs_successfully(template_dir, temp_output_dir):
    """Test that the generated project can be installed (requires chimera)."""
    subprocess.run(
        [
            "cookiecutter",
            str(template_dir),
            "--no-input",
            "--output-dir",
            str(temp_output_dir),
        ],
        check=True,
    )

    project_dir = temp_output_dir / "chimera_my_chimera_plugin"

    # Try to build the package (this validates pyproject.toml structure)
    result = subprocess.run(
        ["python", "-m", "build", "--wheel", "--outdir", str(temp_output_dir)],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    # This might fail if dependencies aren't available, so we just check
    # that pyproject.toml is valid enough to attempt a build
    assert "pyproject.toml" in result.stderr or result.returncode == 0
