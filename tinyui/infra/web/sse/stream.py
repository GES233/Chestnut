from sanic.request import Request
from sanic.compat import Header
from typing import NoReturn

from .event import EventItem


sse_header: Header = Header(
    {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
)


async def publisher(request: Request) -> NoReturn:
    response = await request.respond(
        headers=sse_header,
        content_type="text/event-stream; charset=utf-8",
    )
    # Push message to front-end.
    retry = request.app.config.KEEP_ALIVE_TIMEOUT * 1000

    # TODO: Add a classifier to check the session.
    ...

    # First message from server: Pong.
    await response.send(EventItem.event(0, "site", None, ["Pong"]))  # type: ignore

    # Set here to recieve singals.
    while True:
        # Recieve singals.
        ...
