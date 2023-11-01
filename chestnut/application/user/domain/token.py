from enum import Enum
from datetime import date, datetime
from dataclasses import dataclass
from typing import Any, Callable

from ...core.domain import ValueObject


class TokenScope(str, Enum):
    session = "session"
    token = "token"
    nil = "nil"

    def valid(self):
        return self.value != TokenScope.nil

    def usesession(self):
        return self.value == TokenScope.session

    def usertoken(self):
        return self.value == TokenScope.token
    
    @classmethod
    def fromvalue(cls, value: str | Any) -> "TokenScope":
        if isinstance(value, str):
            return cls(value)
        else:
            for item in cls:
                if item.value == value:
                    return item
            return cls.nil


@dataclass
class UserToken(ValueObject):
    raw_token: bytes
    user_id: int
    scope: TokenScope
    create_at: datetime

    @classmethod
    def buildsessiontoken(
        cls,
        user_id: int,
        scope: str,
        random_width: int,
        random_algorithm: Callable[[int], bytes],
        hash_algorithm: Callable[[bytes], bytes],
    ) -> "UserToken":
        token = hash_algorithm(random_algorithm(random_width))

        return UserToken(
            raw_token=token,
            user_id=user_id,
            scope=TokenScope.fromvalue(scope),  # type: ignore
            create_at=datetime.utcnow()
        )

    def verifysessiontoken(self, request_scope: TokenScope, user_id: int):
        return (
            request_scope in self.scope
            and user_id == self.user_id
        )

    @staticmethod
    def buildhash(hash_algorithm: Callable[..., bytes], source: str | int | bytes):
        if isinstance(source, str):
            source = bytes(source, encoding="utf-8")
        
        return hash_algorithm(source)

    @staticmethod
    def buildencrypt(encrypt_algorithm: Callable[..., bytes]):
        ...
