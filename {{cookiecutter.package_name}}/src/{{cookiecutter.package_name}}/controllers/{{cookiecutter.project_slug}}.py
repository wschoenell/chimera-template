# SPDX-FileCopyrightText: {{ cookiecutter.year }}-present {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
# SPDX-License-Identifier: {{ cookiecutter.license }}
"""{{ cookiecutter.controller_class_name }} controller implementation."""

from chimera.core.chimeraobject import ChimeraObject


class {{ cookiecutter.controller_class_name }}(ChimeraObject):
    """{{ cookiecutter.project_short_description }}"""

    __config__ = {"param1": "a string parameter"}

    def __init__(self) -> None:
        """Initialize the controller."""
        super().__init__()

    def __start__(self) -> None:
        """Start the controller and perform initial operations."""
        self.do_something("test argument")

    def do_something(self, arg: str) -> None:
        """Perform a sample operation.

        Args:
            arg: The argument to process
        """
        self.log.warning("Hi, I'm doing something.")
        self.log.warning(f"My arg={arg}")
        self.log.warning(f"My param1={self['param1']}")
