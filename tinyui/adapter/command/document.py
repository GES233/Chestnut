import click
from typing import Any

from ...infrastructure.command import manage


@manage.group
def document():
    ...
