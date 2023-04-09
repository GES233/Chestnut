# In https://sanic.dev/en/guide/how-to/tls.html#redirect-http-to-https-with-certificate-requests-still-over-http.
from pathlib import Path
from sanic import exceptions, response
from sanic.app import Sanic
from sanic.request import Request
from sanic.server.async_server import AsyncioServer

from ..helpers.path import PROJECT_PATH


redir = Sanic("http_redir")

# Serve ACME/certbot files without HTTPS, for certificate renewals
redir.static("/.well-known", Path(PROJECT_PATH / ".well-known"), resource_type="dir")


@redir.exception(exceptions.NotFound, exceptions.MethodNotSupported)
def redirect_everything_else(request: Request, exception):
    server, path = request.server_name, request.path
    if server and path.startswith("/"):
        return response.redirect(f"https://{server}{path}", status=308)
    return response.text("Bad Request. Please use HTTPS!", status=400)


async def runner(app: Sanic, app_server: AsyncioServer):
    app.is_running = True
    try:
        app.signalize()
        app.finalize()
        app.state.is_started = True
        await app_server.serve_forever()  # type: ignore
    finally:
        app.is_running = False
        app.is_stopping = True


async def start_redir(app: Sanic, _):
    app.ctx.redirect = await redir.create_server(port=80, return_asyncio_server=True)
    app.add_task(runner(redir, app.ctx.redirect))  # type: ignore


async def stop_redir(app: Sanic, _):
    await app.ctx.redirect.close()


def add_http_redirect(app: Sanic):
    app.register_listener(start_redir, "before_server_start")
    app.register_listener(stop_redir, "before_server_stop")
