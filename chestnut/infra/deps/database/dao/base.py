from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


# To adapt alembic's autogenerate.
chestnut_sqlite_metadata: MetaData = MetaData()

class ChestnutBase(DeclarativeBase):
    metadata = chestnut_sqlite_metadata
