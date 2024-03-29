import click
from typing import Any

from ...application.document.domain.document import Document
from ...application.document.domain.meta import DocumentMeta
from ...application.document.domain.repo import DocRepo, DocMetaRepo
from ...application.document.usecase.format import *
from ...infra.cmd import manage
from ...infra.cmd.db import initializedb


@manage.group
def document():
    ...


@document.command("update")
def update() -> None:
    """Load from file, and write to database."""

    ...
