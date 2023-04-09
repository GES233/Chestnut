from abc import ABC, abstractmethod
from typing import Dict, Any


class DataAccessObjectMixin(ABC):
    @classmethod
    @abstractmethod
    def fromentity(cls, entity: Any) -> "DataAccessObjectMixin":
        """Entity/VO -> DAO"""

        raise NotImplementedError

    @abstractmethod
    def squeeze(self) -> Any:
        """DAO -> dict"""

        raise NotImplementedError
