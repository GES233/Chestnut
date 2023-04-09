import click


@click.group
def manage():
    """Manager of application."""

    ...


# Import commands here.
# Application-agnostic:
from .db import database
from .init import launch_simple_web_app, set_command
from .run import running


# Application related:
from ...adapter.command.prerequisite import prerequisite
from ...adapter.command.required import required
