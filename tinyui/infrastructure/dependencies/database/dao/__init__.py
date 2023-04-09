from sqlalchemy import MetaData

from .base import tiny_sqlite_metadata

# Import tables to adapt alembic's autogenerate here.
# repository also required.
from .document import document_table

# from .required import required_table
# from .prerequisite import prerequisite_table

# Import DAO's here.
...
