""" `tinyui.adapter.command.prerequisite`

    Set it to `adapter` because it's close to application.
"""
import click

from ...infrastructure.command import manage


@manage.group
def prerequisite():
    """Command interface for change prerequisite item."""

    pass


@prerequisite.command("show")
def show() -> None:
    pass


@prerequisite.command("list")
def list_() -> None:
    pass


@prerequisite.command("check")
def check() -> None:
    pass
