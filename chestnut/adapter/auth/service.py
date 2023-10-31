import secrets, base64, hashlib
from datetime import timedelta
from typing import Callable

from ...application.user.exception import TokenExpire, TokenInvalid
from ...application.user.domain.user import User
from ...application.user.domain.token import UserToken
from ...application.user.service.user_auth import (
    givetokenundersession,
    verifytokenundersession,
)
from ...infra.deps.database.dao.token import defaultUserTokenRepo


def random_char_adpter() -> Callable[[int], bytes]:
    return lambda width: base64.b64encode(secrets.token_bytes(width))


def hash_sha256_adapter() -> Callable[[bytes], bytes]:
    return lambda raw: hashlib.sha256(raw).digest()


CHAR_WIDTH = 32


def givesessionfromuser(user: User) -> UserToken:
    return givetokenundersession(
        random_algorithm=random_char_adpter(),
        hash_algorithm=hash_sha256_adapter(),
        user=user,
    )


async def checksession(raw_session: bytes, user: User, session_fac, exp: timedelta) -> bool:
    try:
        await verifytokenundersession(
            raw_session=raw_session,
            user=user,
            repo=defaultUserTokenRepo(session=session_fac),
            expire=exp
        )
    except (TokenInvalid, TokenExpire):
        return False
    else:
        return True
