from os import environ
from sanic.config import Config
from sanic.exceptions import SanicException
from sanic.log import logger
from typing import Dict

from .location import CONFIG_LOCATION
from ...helpers.config import AppConfig, DepsConfig
from ...helpers.config.inst import loadappconfig, loaddepsconfig
from ...helpers.path import INSTANCE_PATH


def create_app_config(
    mode: str | None, use_instance: bool, app_id: str | int | None = None
) -> AppConfig:
    if mode == "dev":
        return AppConfig(
            name="Chestnut_dev",
            introduction="Dev mode.",
            installed=True,
        )
    elif mode == "test":
        return AppConfig(
            "Chestnut_test",
            introduction="Test mode.",
            installed=True,
        )
    else:
        prod_config = AppConfig(
            "Chestnut",
            introduction="Provice a simple UI iterface.",
            installed=False if use_instance else True,
        )

        # Load from instance.
        if use_instance:
            try:
                prod_config.load(
                    loadappconfig(
                        (
                            lambda app_id: "config.toml"
                            if not app_id
                            else ("config_" + str(app_id) + ".toml")
                        )(app_id),
                        INSTANCE_PATH,
                    )
                )
            except FileNotFoundError:
                raise SanicException(f"Wrong App's name {app_id}.")

            prod_config.load({"installed": True})

        # TODO: Update from enviornment with `APP_` prefix.

        return prod_config


def create_deps_config(
    mode: str, use_instance: bool, app_id: str | int | None = None
) -> Dict[str, DepsConfig]:
    deps_dict: Dict[str, DepsConfig] = {}

    # Different.
    if mode == "dev":
        from .dev import (
            database_dev as database,
            security_dev as security,
        )
    elif mode == "test":
        from .test import (
            database_test as database,
            security_test as security,
        )
    else:
        from .prod import (
            database_prod as database,
            security_prod as security,
        )

    # Common.
    from ...deps.message.settings import message

    for append_item in [database, security, message]:
        deps_dict[append_item.name.upper()] = append_item

    # Load from instance.
    if use_instance and mode not in ["dev", "test"]:
        try:
            deps_list_raw = loaddepsconfig(
                (
                    lambda app_id: "config.toml"
                    if not app_id
                    else ("config_" + str(app_id) + ".toml")
                )(app_id),
                INSTANCE_PATH,
            )
        except FileNotFoundError:
            if app_id:
                raise SanicException(f"Wrong App's name {app_id}.")
            raise SanicException("Instance not found.")

        # Only update some items.
        for dep in deps_list_raw:
            if deps_list_raw[dep]["enable"]:
                deps_dict[dep.upper()].load(True, deps_list_raw[dep])

    # TODO: Add ENV.

    return deps_dict


def create_config(
    mode: str | None,
    use_instance: bool = True,
    app_id: str | int | None = None,
    app_prefix: str = "APP_",
) -> Config:
    """Integrate app's config."""

    # Set mode.
    if mode:
        mode = mode
    else:
        # Flowchart(dev or test):
        # - Default => Environment.
        # Flowchart(prod):
        # - Default => Instance => Environment.
        # - Default => Environment.

        mode = environ.get(app_prefix + "ENV", "launch")
        # Mostly, A newbie who forget to set mode: => Launch mode(it belongs to prod mode).

    config = Config()

    # Application's config.
    app_config = create_app_config(mode, use_instance, app_id)

    if app_config.installed and mode and mode != "launch":
        config.update({CONFIG_LOCATION["app_config"]: app_config})

        # Dependencies' config.
        config.update(create_deps_config(mode, use_instance, app_id))
    else:
        # If not installed => make a app called `launch`.
        if not app_config.installed:
            logger.warning(
                "App does not installed, UI will returned a launch to guide installation."
            )
        app_config.name = "Chestnut-Launcher"

        # Using `dev` mode to mininum dependency.
        from ...deps.message.settings import message

        config.update(
            {
                CONFIG_LOCATION["app_config"]: app_config,
                CONFIG_LOCATION["sse_message"]: message,
            }
        )

    return config
