import secrets, base64, hashlib
from datetime import timedelta
from typing import Callable

from ...application.user.exception import TokenExpire, TokenInvalid, NoUserMatched
from ...application.user.domain.user import User
from ...application.user.domain.token import UserToken
from ...application.user.domain.repo import UserTokenRepo
from ...application.user.service.user_auth import (
    givetokenundersession,
    verifytokenundersession,
)


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


async def checksession(raw_session: bytes, user: User, repo: UserTokenRepo, exp: timedelta) -> bool:
    try:
        await verifytokenundersession(
            raw_session=raw_session,
            user=user,
            repo=repo,
            expire=exp
        )
    except (TokenInvalid, TokenExpire):
        return False
    else:
        return True


async def returnuserfromsession(raw_session: bytes, repo: UserTokenRepo) -> User | None:
    try:
        user = await repo.getuserbytoken(raw_session)
    except NoUserMatched:
        return None
    return user
