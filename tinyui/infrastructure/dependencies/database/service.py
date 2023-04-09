from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops

from .base import asyncsession_factory, _config_validation
from ...helpers.config import DepsConfig


def enginefromconfig(config: DepsConfig) -> AsyncEngine:
    _config_validation(config, ["uri", "encoding", "echo"])

    return create_async_engine(
        url=config.uri,
        echo=config.echo,
    )
