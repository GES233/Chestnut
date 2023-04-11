"""Used to register Dependency Injection for Sanic app."""
from sanic import Sanic

from .database import add_dependency_database
from .security import add_dependency_crypt


def register_dependencies(app: Sanic, extension_enable: bool = True) -> None:
    """Register all dependencies."""

    # Crypt.
    add_dependency_crypt(app, extension_enable)

    # Database.
    add_dependency_database(app, extension_enable)
