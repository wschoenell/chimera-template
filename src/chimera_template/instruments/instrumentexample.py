# SPDX-FileCopyrightText: 2024-present William Schoenell <wschoenell@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Example instrument implementation."""

from chimera.core.chimeraobject import ChimeraObject


class InstrumentExample(ChimeraObject):
    """Example instrument class demonstrating basic chimera instrument structure."""

    __config__ = {"param1": "a string parameter"}

    def __init__(self) -> None:
        """Initialize the instrument."""
        super().__init__()

    def __start__(self) -> None:
        """Start the instrument and perform initial operations."""
        self.do_something("test argument")

    def do_something(self, arg: str) -> None:
        """Perform a sample operation.

        Args:
            arg: The argument to process
        """
        self.log.warning("Hi, I'm doing something.")
        self.log.warning(f"My arg={arg}")
        self.log.warning(f"My param1={self['param1']}")
