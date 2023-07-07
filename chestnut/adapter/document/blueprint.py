from typing import Any, Callable
from sanic import Blueprint, Request, HTTPResponse

from ...infra.web.settings.location import CONFIG_LOCATION
from ...infra.deps.markdown.service import DocumentMarkdown


def registerdocs(bp: Blueprint) -> None:
    ...

    # Load ALL for Repository.
    ...

    # Register router.
    ...


def addrouter(bp: Blueprint, route: Callable[..., Any], uri: str) -> None:
    if route:
        bp.add_route(route, uri)
