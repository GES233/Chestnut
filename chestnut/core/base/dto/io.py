from abc import ABC, abstractmethod
from typing import Dict, Any


class InputSchemaMixin(ABC):
    @classmethod
    @abstractmethod
    def fromdict(cls, input_dict: Dict) -> "InputSchemaMixin" | Any:
        """Load DTO from dict."""

        raise NotImplementedError

    @abstractmethod
    def toentity(self) -> Any:
        """Send DTO to entity or value-object."""

        raise NotImplementedError


class OutputSchemaMixin(ABC):
    @classmethod
    @abstractmethod
    def fromentity(cls, entity: Any) -> "OutputSchemaMixin" | Any:
        """Load DTO from from entity or value-object."""

        raise NotImplementedError
