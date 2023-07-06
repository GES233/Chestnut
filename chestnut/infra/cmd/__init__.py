import click


@click.group
def manage():
    """Manager of application."""

    ...


# Import commands here.
# Application-agnostic:
from .db import database
from .init import launchsimplewebapp, set_command
from .run import running


# Application related:
from ...adapter.document.command import document
from ...adapter.dependent_item.command.required import required
from ...adapter.dependent_item.command.prerequisite import prerequisite
