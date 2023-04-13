from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, AsyncSession


# Create DAOBase.
class DAOBase:
    table: Table
    engine: AsyncEngine

    def __init__(self, engine: AsyncEngine, table: Table) -> None:
        self.engine = engine
        self.table = table

    ...
