from datetime import timedelta
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from typing import Callable

from .encrypt import random_char_adpter, hash_sha256_adapter
from ....application.user.exception import TokenExpire, TokenInvalid, NoUserMatched
from ....application.user.domain.user import User
from ....application.user.domain.token import UserToken, TokenScope
from ....application.user.domain.repo import UserTokenRepo
from ....application.user.service.user_auth import (
    givetokenundersession,
    verifytokenundersession,
)
from ....application.user.usecase.token import (
    AppendTokenUsecase,
    RemoveTokenUsecase,
    CheckTokenUsecase,
    ReturnUserUsecase,
)
from ....infra.deps.database.dao.token import defaultUserTokenRepo


def givesessionfromuser(user: User) -> UserToken:
    return givetokenundersession(
        random_algorithm=random_char_adpter(),
        hash_algorithm=hash_sha256_adapter(),
        user=user,
        scope=TokenScope.session.value
    )


async def checksession(raw_session: bytes, user: User, repo: UserTokenRepo, exp: timedelta) -> bool:
    try:
        await verifytokenundersession(
            raw_session=raw_session,
            user=user,
            repo=repo,
            expire=exp,
            scope=TokenScope.session
        )
    except (TokenInvalid, TokenExpire):
        return False
    else:
        return True


async def returnuserfromsession(raw_session: bytes, repo: UserTokenRepo) -> User | None:
    try:
        user = await repo.getuserbytokenandscope(raw_session, scope=TokenScope.session)
    except NoUserMatched:
        return None
    return user


append_session_usecase = lambda db_session_fac: AppendTokenUsecase(
    repo=defaultUserTokenRepo(db_session_fac),
    service_user2session=givesessionfromuser
)  # type: Callable[[async_sessionmaker], AppendTokenUsecase]


remove_session_usecase = lambda db_session_fac: RemoveTokenUsecase(
    repo=defaultUserTokenRepo(db_session_fac)
)  # type: Callable[[async_sessionmaker], RemoveTokenUsecase]


check_session_usecase = lambda db_session_fac: CheckTokenUsecase(
    repo=defaultUserTokenRepo(db_session_fac),
    default_scope=TokenScope.session,
)  # type: Callable[[async_sessionmaker], CheckTokenUsecase]

return_user_usecase_from_session = lambda db_session_fec, parse_req_service: ReturnUserUsecase(
    repo=defaultUserTokenRepo(db_session_fec),
    current_scope=TokenScope.session,
    analyse_request=parse_req_service
)  # type: Callable[[async_sessionmaker, Callable[..., bytes]], ReturnUserUsecase]
