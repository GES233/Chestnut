from typing import Any, Dict
from enum import Enum


languege = (
    lambda content, lang: content if not isinstance(content, dict) else content[lang]
)


class PrerequisiteConfig:
    """Load object from config or database."""

    name: str
    type: str
    check: Dict[str, Any]
    url: Dict[str, str]
    description: Dict[str, Any] | str

    __slots__ = (
        "name",
        "type",
        "check",
        "url",
        "description",
    )

    def __init__(
        self,
        name: str,
        type: str,
        check: Dict[str, Any],
        url: Dict[str, str],
        desctiption: Dict[str, str] | str,
    ) -> None:
        self.name = name
        self.type = type
        self.check = check
        self.url = url
        self.description = desctiption

    @staticmethod
    def _loadrequire(required_str: str) -> Any:
        ...

    @staticmethod
    def _loaddescription(content: str) -> Any:
        ...

    @staticmethod
    def _loadurl(raw_url: str) -> Any:
        ...

    @classmethod
    def loadfromdict(cls, content: Dict) -> "PrerequisiteConfig":
        ...
        # Some preperation process.

        return PrerequisiteConfig(
            name=content["name"],
            type=content["type"],
            check=content["check"],
            url=content["url"],
            desctiption=content["description"],
        )

    @classmethod
    def loadfromtable(cls, object: Any) -> "PrerequisiteConfig":
        ...
