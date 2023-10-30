from sqlalchemy import MetaData

from .base import chestnut_sqlite_metadata

# Import tables to adapt alembic's autogenerate here.
# repository also required.
from .user import UserDAO


# Import DAO's here.
...
