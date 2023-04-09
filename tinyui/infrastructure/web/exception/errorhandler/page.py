from sanic import HTTPResponse
from sanic.errorpages import HTMLRenderer

from .plain import launch_render_sync, parse_error


class WebAppHTMLRenderer(HTMLRenderer):
    """HTMLRenderer with WebApp style."""

    def full(self) -> HTTPResponse:
        ...
        return super().full()

    def minimal(self) -> HTTPResponse:
        ...
        return super().minimal()
