from jinja2 import (
    Environment,
    select_autoescape,
    FileSystemLoader,
)
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.errorpages import HTMLRenderer
from typing import Any, Dict, List
from tracerite.trace import extract_exception

from ....helpers.path import TEMPLATE_PATH
from ....dependencies.html import returnloaderandenv
from ....dependencies.highlight import rendercode


def launch_render_sync(
    request: Request,
    template_name: str = "",
    status: int = 200,
    headers: Dict[str, str] | None = None,
    content_type: str = "text/html; charset=utf-8",
    context: Dict[str, Any] = {},
) -> HTTPResponse:
    """Only in errorhander."""

    appended_context = context

    # Fetch some content registed on middleware.
    appended_context.update(app_config=request.ctx.app_config)
    appended_context.update(page_config=request.ctx.page_config)

    loader, launch_environment = returnloaderandenv(TEMPLATE_PATH, False)

    kwargs = context if context else {}
    template = launch_environment.get_template(template_name)

    render = template.render
    content = render(**kwargs)

    return HTTPResponse(
        content, status=status, headers=headers, content_type=content_type
    )


APOLOGIZE_CONTENT = """\
We're sorry, but it looks like something went wrong. Please try refreshing \
the page or navigating back to the homepage. If the issue persists, please \
report to {0}, our technical team is working to resolve it as soon as possible. \
We apologize for the inconvenience and appreciate your patience.\
"""


class CustomeHTMLRenderer(HTMLRenderer):
    def full(self, full=True) -> HTTPResponse:
        """Default runner."""

        debug = self.debug
        title = super().title
        text = super().text
        request: Request = self.request
        exc: Exception = self.exception

        # Update PageConfig.
        request.ctx.page_config.load_items(title=title)

        template_context_dict = parse_error(
            debug=debug, full=full, request=request, title=title, text=text, exc=exc
        )

        return launch_render_sync(
            request=request,
            template_name="exception.html",
            status=self.status,
            headers=self.headers,
            context={"exc_dict": template_context_dict},
        )

    def minimal(self) -> HTTPResponse:
        return self.full(full=False)


def parse_error(
    debug: bool, full: bool, request: Request, title: str, text: str, exc: Exception
) -> Dict[str, str | bool | dict | None]:
    template_context_dict: Dict[str, str | bool | dict | None] = dict(
        debug=debug, full=full, name=request.app.name, title=title, content=text
    )

    # Exception detail.
    exc_chain: List[Exception] = []
    while exc:
        exc_chain.append(exc)
        if getattr(exc, "__suppress_context__", False):
            break
        exc = getattr(exc, "__cause__") or getattr(exc, "__context__")
    parsed_exc_chain = [extract_exception(e) for e in exc_chain]
    # Decorate process.
    exc_chain_html = []
    for idx, exc_ in enumerate(parsed_exc_chain):
        exc_chain_html.append(
            dict(
                type=exc_["type"],
                message=exc_["message"],
                summary=exc_["summary"],
                repr=exc_["repr"],
                frames=[],
            )
        )
        if not debug:
            continue
        for frame in exc_["frames"]:
            exc_chain_html[idx]["frames"].append(
                dict(
                    relevance=frame["relevance"],
                    filename=frame["filename"],
                    location=frame["location"],
                    # codeline=frame["codeline"],
                    lineno=frame["lineno"],
                    linenostart=frame["linenostart"],
                    lines=rendercode(frame["lines"], "python", frame["linenostart"]),
                    function=frame["function"],
                    urls=frame["urls"],
                    variables=frame["variables"],
                )
            )

    if template_context_dict["debug"]:
        template_context_dict["abstract"] = None
        template_context_dict["detail"] = dict(
            # Header in detail, for presentation.
            # Details for developers (DEBUG mode only)
            route=(
                request.name or "[route not found]"
            ),  # f"Exception in {route_name}:"
            extra=getattr(exc, "extra", None),
            # Traceback in exception.
            exc_frames=exc_chain_html,
            # Request info.
            request=f"{request.method} {request.path}",
            # Request info.
            headers={k: request.headers[k] for k in request.headers.keys()},
        )
    else:
        template_context_dict["detail"] = None
        template_context_dict["abstract"] = dict(
            content=APOLOGIZE_CONTENT.format(
                f"<a href='{request.ctx.app_config.website}'>our website</a>"
            ),
            exc_info=dict(
                type=exc_chain_html[-1]["type"],
                summary=exc_chain_html[-1]["summary"],
            ),
        )

    # Extra.
    template_context_dict["extra"] = getattr(exc, "extra", None)

    return template_context_dict
