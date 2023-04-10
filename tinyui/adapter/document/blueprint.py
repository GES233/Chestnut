from sanic import Blueprint, Request, HTTPResponse

from ...infrastructure.dependencies.markdown.service import DocumentMarkdown


def registerdocs(bp: Blueprint) -> None:
    ...

    # Load ALL for Repository.
    ...

    # Register router.
    ...
