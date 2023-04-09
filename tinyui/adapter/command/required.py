"""`tinyui.adapter.command.required`"""
import click

from ...infrastructure.command import manage


@manage.group
def required():
    """Command interface for change required item."""

    pass


@required.command("add")
def add() -> None:
    pass


@required.command("del")
def delete() -> None:
    pass


@required.command("edit")
def edit() -> None:
    pass
