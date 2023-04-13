import click

from . import manage


@manage.command("run")
@click.argument("name", required=False)
@click.option("--dev", "mode", flag_value="dev")
@click.option("--test", "mode", flag_value="test")
@click.option("--pro", "mode", flag_value="prod", default=True)
def running(mode: str, name: str | None) -> None:
    """Run application."""

    from functools import partial
    from sanic import Sanic
    from sanic.worker.loader import AppLoader
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
    click.secho("INFO     :: Sanic instance created.", fg="green")

    if mode == "prod":
        use_https: bool = app.config[CONFIG_LOCATION['app_config']].use_https
        app.prepare(
            host="0.0.0.0",
            port=80 if not use_https else 443,
            debug=False,
            auto_reload=False,
            motd=False,
        )
        click.secho("INFO     :: App in `prod` mode.", fg="green")
        click.secho(
            f"INFO     :: Deploy on {'http' if not use_https else 'https'}://0.0.0.0:{str(80 if not use_https else 443)}",
            fg="green",
        )
        server_location = f"{'http' if not use_https else 'https'}://0.0.0.0:{str(80 if not use_https else 443)}"
    elif mode == "test":
        app.prepare(
            host="0.0.0.0",
            port=80,
            debug=True,
            coffee=True,
        )
        click.secho("INFO     :: App in `test` mode.", fg="green")
        click.secho(
            "INFO     :: Deploy on http://0.0.0.0:80",
            fg="green",
        )
        server_location = "http://0.0.0.0:80"
    else:
        # Run as dev mode, same as `create_app()`.
        app.prepare(
            host="127.0.0.1",
            port=6969,
            dev=True,
            reload_dir=reload_paths(),
            motd=False,
        )
        click.secho("INFO     :: App in `dev` mode.", fg="green")
        click.secho(
            "INFO     :: Deploy on http://127.0.0.1:6969",
            fg="green",
        )
        server_location = "http://127.0.0.1:6969"

    Sanic.serve(app, app_loader=loader)
