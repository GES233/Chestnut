""" `chestnut.infra.web.app`

    Implement application factory.
"""
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.config import Config

try:
    import sanic_ext  # type: ignore

    EXTENSION_INSTLLED: bool = True
except (ModuleNotFoundError, ImportError):
    EXTENSION_INSTLLED: bool = False


def create_app(
    *,  # Avoid sanic's cli.
    mode: str | None = None,
    use_instance: bool = True,
    app_id: str | int | None = None,
) -> Sanic:
    """Create an application."""

    from .exception import configure_exceptions
    from .http_redir import add_http_redirect
    from .middleware import register_middleware
    from .settings import create_config
    from .settings.location import CONFIG_LOCATION
    from .sse import register_stream
    from ..log.config import LOGGING_CONFIG

    launch_mode = mode == "launch"

    # Create config firstly.
    config: Config = create_config(
        mode=mode,
        use_instance=use_instance if not launch_mode else False,
        app_id=app_id,
    )

    # Create app.
    app = Sanic(name=config.APP.name, config=config, log_config=LOGGING_CONFIG)

    if launch_mode or mode is None:
        # Launch app.
        from .blueprints.plain.launch import register_launch

        # Only used to launch app.
        register_launch(app)

        if EXTENSION_INSTLLED:
            from .extension import configure_extensions

            configure_extensions(app=app, launch=True)

    else:
        from .blueprints import register_blueprint
        from .dependency import register_dependencies

        # Extension.
        if not EXTENSION_INSTLLED:
            raise SanicException(
                "Package sanic_ext is required in main app, please install it."
            )
        # Normally, sanic_ext is required when running,
        # so it's not a good idea to RE-check extension.
        from .extension import configure_extensions

        configure_extensions(app=app)

        # Dependencies.
        register_dependencies(app)

        # Middleware
        register_middleware(app)

        # Blueprints.
        register_blueprint(app)

    # SSE.
    register_stream(app)

    # Exceptions.
    configure_exceptions(app)

    # HTTPS.
    if app.config[CONFIG_LOCATION["app_config"]].use_https and not launch_mode:
        add_http_redirect(app)

    return app
