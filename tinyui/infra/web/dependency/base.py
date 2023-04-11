from abc import ABCMeta, abstractmethod
from sanic import Request


class DepsInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def fromrequest(cls, request: Request) -> None:
        """Fetch dependency from request."""

        raise NotImplementedError
