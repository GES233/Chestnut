import click
from typing import Any

from ...core.document.domain.document import Document
from ...core.document.domain.meta import DocumentMeta
from ...core.document.domain.repo import DocRepo, DocMetaRepo
from ...infra.cmd import manage
from ...infra.cmd.db import initializedb


@manage.group
def document():
    ...


@document.command("update")
def update() -> None:
    """Load from file, and write to database."""

    ...
