import click

from . import manage
from ..helpers.config import AppConfig, DepsConfig


def configure_app(customize: bool, app_id: int | str | None = None) -> AppConfig:
    """A helper function to generate AppConfig."""

    app_config = AppConfig(name="Tiny UI.", introduction="", installed=False)

    if customize:
        info_of_app = (
            "As before, if you need to write a lot of stuff or a line break, "
            + "go to `... /instance/config.toml` when configure finished and change manually."
        )
        click.secho(
            "Next, you need to manually configure the application-related content.",
            fg="cyan",
        )
        click.secho(info_of_app, fg="cyan")
        app_name = click.prompt(
            "Please type the name of the app (preferably in Latin-1 character with _ or -)"
        )
        if app_id:
            _use_app_id = click.prompt(
                "Would you like to write `app_id` to the name of app[Y/n]",
                type=bool,
                default=True,
            )
            if _use_app_id:
                app_name = app_name + "_" + app_id

        app_intro = click.prompt(
            "Please enter more information about the app (preferably in a few tens of words, "
            "and utf-8 encoded characters are acceptable)"
        )
        app_website = click.prompt("Bla bla...")

        app_config.name = app_name
        app_config.introduction = app_intro
        # app_config.website = app_website

    # TODO: Add language.

    return app_config


def set_inst_func(
    customize: bool,
    app_id: str | int | None,
) -> None:
    """Configure and set instance."""

    from ..helpers.config.inst.render import createdepsconfig, createappconfig
    from ..helpers.path import INSTANCE_PATH, INSTANCE_CONFIG_PATH
    from ..dependencies.security.settings import set_security_inst_setting

    # Create instance firstly.
    if not INSTANCE_PATH.exists():
        INSTANCE_PATH.mkdir()
        click.secho("[INFO]    Created instance folder.", fg="green")

    # Security
    security_config: DepsConfig = set_security_inst_setting(INSTANCE_PATH)
    click.secho("[INFO]    App's crypt config is setted.", fg="green")

    # Markdown
    # TODO: add it.

    # Integrate all deps config.
    deps_config_list = [security_config]
    deps_config = createdepsconfig(deps_config_list)

    # App
    app_config = configure_app(customize, app_id=app_id)

    if not INSTANCE_CONFIG_PATH(app_id).exists():
        INSTANCE_CONFIG_PATH(app_id).touch()

    INSTANCE_CONFIG_PATH(app_id).write_text(
        "\n\n".join([createappconfig(app_config), deps_config]), "utf-8"
    )

    # TODO: Update docs to database.

    click.secho("[INFO]    All has done.", fg="green")


set_command = click.option(
    "--id",
    "app_id",
    help="Identity of application when you wanna serve multi apps[Optional].",
)(
    click.option("-c", "--customize", "customize", is_flag=True)(
        manage.command("set")(set_inst_func)
    )
)


@manage.command("launch")
@click.option("--host", "host", default="127.0.0.1")
@click.option("--port", "port")
@click.option("--dev", "mode", flag_value="dev")
@click.option("--pro", "mode", flag_value="prod", default=True)
def launch_simple_web_app(host: str, port: str | int | None, mode: str) -> None:
    """Launch user to install all dependencies(web solution of set)."""

    from functools import partial
    from sanic import Sanic
    from sanic.log import logger
    from sanic.worker.loader import AppLoader
    from ..web.app import create_app
    from ..web.blueprints import reload_paths

    loader = AppLoader(
        factory=partial(
            create_app,
            mode="launch",
            use_instance=False,
            app_id=None,
        )
    )
    app: Sanic = loader.load()
    app.prepare(
        host=host,
        port=int(port) if port else 6699,
        dev=True if (mode == "dev") else False,
        reload_dir=reload_paths(),
    )

    if host not in ["localhost", "127.0.0.1"]:
        logger.warn(
            (
                "This Sanic app instance can present some sentitive info, "
                "please ensure it is running on Local Area Network."
            ),
        )

    Sanic.serve(app, app_loader=loader)
