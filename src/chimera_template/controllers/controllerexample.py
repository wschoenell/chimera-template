# SPDX-FileCopyrightText: 2024-present William Schoenell <wschoenell@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Example controller implementation."""

from chimera.core.chimeraobject import ChimeraObject


class ControllerExample(ChimeraObject):
    """Example controller class demonstrating basic chimera controller structure."""

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
