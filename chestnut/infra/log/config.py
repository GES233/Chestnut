import sys
import logging

from typing import Dict, Any


LOGGING_CONFIG: Dict[str, Any] = dict(  # no cov
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
        "sanic.server": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
            "qualname": "sanic.server",
        },
        "chestnut.root": {"level": "INFO", "handlers": ["console"]},
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
    },
    formatters={
        "generic": {
            "format": "%(levelname)-8s    %(asctime)s :: %(process)-6s :: %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S %z",
            "class": "chestnut.infra.log.service.ChestnutFormatter",
        },
        "access": {
            "format": "%(levelname)-8s    %(asctime)s :: [%(name)s@%(host)s]: "
            + "%(request)s %(message)s %(status)s %(byte)s",
            "datefmt": "%y-%m-%d %H:%M:%S %z",
            "class": "chestnut.infra.log.service.ChestnutFormatter",  # logging.Formatter
        },
    },
)
