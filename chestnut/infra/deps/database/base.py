from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from typing import Iterable

from ...helpers.config import DepsConfig


def _config_validation(config: DepsConfig, assert_items: Iterable[str]) -> None:
    assert config.name in ["db", "database", "sqlalchemy"]

    for item in assert_items:
        assert item in config.values


def asyncsession_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False)
