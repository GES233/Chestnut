"""Exception warpper."""
from abc import ABC, abstractmethod
from typing import Any

from ..exception import AppExcBase


class ExceptionSchemaMixin(ABC):
    """Exception presented to user."""

    exc: Exception
    msg: str | None

    @classmethod
    @abstractmethod
    def set(cls, exc_: AppExcBase) -> "ExceptionSchemaMixin" | Any:
        raise NotImplementedError

    @abstractmethod
    def display(self) -> Any:
        raise NotImplementedError
