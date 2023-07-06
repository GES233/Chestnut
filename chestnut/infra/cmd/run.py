import click

from . import manage
from ..log.service import chestnut_logger


@manage.command("run")
@click.option("--dev", "mode", flag_value="dev")
@click.option("--test", "mode", flag_value="test")
@click.option("--pro", "mode", flag_value="prod", default=True)
@click.argument("name", required=False)
@click.option("--host", "host", default="127.0.0.1")
@click.option("--port", "port", default=6699)
@click.option("--public", "-p", "public", default=False)
def running(
    mode: str, name: str | None, host: str, port: int | str, public: bool
) -> None:
    """Run application."""

    from functools import partial
    from sanic import Sanic
    from sanic.worker.loader import AppLoader

    from ..helpers.link import DEPLOY_LINK
    from ..web.app import create_app
    from ..web.blueprints import reload_paths
    from ..web.settings.location import CONFIG_LOCATION

    loader = AppLoader(
        factory=partial(
            create_app,
            mode=mode,
            use_instance=True,
            app_id=name,
        )
    )
    app: Sanic = loader.load()
    chestnut_logger.info("Sanic instance created.")

    use_https: bool = app.config[CONFIG_LOCATION["app_config"]].use_https
    server_host = host
    server_port = int(port) if not public else (80 if not use_https else 443)
    server_location = DEPLOY_LINK(use_https, server_host, server_port)

    if mode == "prod":
        app.prepare(
            host=server_host,
            port=server_port,
            debug=False,
            auto_reload=False,
            motd=False,
        )
    elif mode == "test":
        app.prepare(
            host="127.0.0.1",
            port=80,
            debug=True,
            coffee=True,
        )
        server_location = "http://127.0.0.1:80"  # Re-write.
    else:
        # Run as dev mode, same as `create_app()`.
        app.prepare(
            host=server_host,
            port=server_port,
            dev=True,
            reload_dir=reload_paths(),
            motd=False,
        )
        mode = "dev"
    chestnut_logger.info(f"App in `{mode}` mode.")
    chestnut_logger.info(f"Deploy on {server_location}")

    Sanic.serve(app, app_loader=loader)
