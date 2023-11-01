from sanic import Request, HTTPResponse
from typing import Callable, Any

from ..render import plain_render as render
from .....deps.document.language import nametoroute
from .....deps.markdown.service import DocumentMarkdown
from .....helpers.config.page import PageConfig


def add_router(content: str, name: str | None = None) -> Callable[..., Any]:
    # TODO: Add language detection => language from `app.config.APP.lang`.
    # TODO: Update name to route.
    # TODO: Path replace content.
    async def present_docs(request: Request) -> HTTPResponse:
        if name:
            request.ctx.page_config.load_items(**PageConfig.addtitle(title=name))

        markdown = DocumentMarkdown()
        # There're two methods to implement markdown file detection and language change:
        # - Parse HTML file after rendered
        # - Re-design markdown renderer
        result = markdown(content)

        return await render(request, "docs.html", context=dict(content=result))

    return present_docs
