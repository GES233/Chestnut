from sanic import Sanic
from sanic.request import Request
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from .base import DepsInterface
from ..settings.location import CONFIG_LOCATION
from ...deps.database import service


class DatabaseDep(DepsInterface):
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, engine: AsyncEngine) -> None:
        if not isinstance(engine, AsyncEngine):
            raise AttributeError(
                f"The engine object is a instance of {AsyncEngine.__name__}, "
                f"not a {engine.__class__.__name__}."
            )

        self.engine = engine
        self.session_maker = service.asyncsession_factory(self.engine)

    @classmethod
    def fromrequest(cls, request: Request) -> "DatabaseDep":
        return cls(engine=request.app.ctx.database_engine)


async def database_register(app: Sanic) -> None:
    app.ctx.database_engine = service.enginefromconfig(
        app.config[CONFIG_LOCATION["database"]]
    )  # Use upper.


async def database_dispose(app: Sanic) -> None:
    await app.ctx.database_engine.dispose()


def add_dependency_database(app: Sanic, enable: bool) -> None:
    app.register_listener(database_register, "before_server_start")
    app.register_listener(database_dispose, "before_server_stop")

    if enable:
        # Add `type` and `builder` of session.
        app.ext.add_dependency(DatabaseDep, DatabaseDep.fromrequest)
