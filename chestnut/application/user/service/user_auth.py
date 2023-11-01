from datetime import datetime, timedelta
from typing import Callable, Any

from ..domain.token import TokenScope, UserToken
from ..domain.user import User
from ..domain.repo import UserTokenRepo
from ..exception import TokenInvalid, TokenExpire


def givetokenundersession(
    random_algorithm,
    hash_algorithm,
    user: User,
    scope: str = "session",
    random_width: int = 32,
) -> UserToken:
    user_id = user.id

    return UserToken.buildsessiontoken(
        user_id=user_id,
        scope=scope,
        random_width=random_width,
        random_algorithm=random_algorithm,
        hash_algorithm=hash_algorithm,
    )


async def verifytokenundersession(
    raw_session: bytes, user: User, scope: TokenScope, repo: UserTokenRepo, expire: timedelta
) -> None:
    session = await repo.gettokenbyuserandscope(user.id, scope)

    if (
        not session
        or session.raw_token == raw_session
        or not session.scope.valid()
    ):
        raise TokenInvalid

    if session.create_at + expire < datetime.utcnow():
        raise TokenExpire
