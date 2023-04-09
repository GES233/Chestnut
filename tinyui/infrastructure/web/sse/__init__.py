from sanic import Sanic

from ..settings.location import CONFIG_LOCATION


def register_stream(app: Sanic) -> None:
    from .stream import publisher

    app.add_route(
        publisher,
        app.config[CONFIG_LOCATION["sse_message"]].subcribe_url,
        ["GET", "POST"],
        stream=True,
    )
