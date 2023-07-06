""" `chestnut.application.core.dto.exc`

    Exception warpper.
"""
from abc import ABC, abstractmethod
from typing import Any

from ..exception import AppExcBase


class ExceptionSchemaMixin(ABC):
    """A container to store exception and it can present exception to user."""

    exc: Exception
    msg: str | None

    def __init__(self, *args, **kwds) -> None:
        self = self.__class__.set(*args, **kwds)

    @classmethod
    @abstractmethod
    def set(cls, exc_: AppExcBase) -> "ExceptionSchemaMixin" | Any:
        # TODO: Desine and update here.
        raise NotImplementedError

    @abstractmethod
    def display(self) -> Any:
        raise NotImplementedError
