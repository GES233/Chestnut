try:
    import sqlalchemy

    SQLALCHEMY_INSTALLED = True
except (ModuleNotFoundError, ImportError):
    SQLALCHEMY_INSTALLED = False
