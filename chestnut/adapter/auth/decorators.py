from sanic import Request
from functools import wraps

from .client.cookie import fetchsession
from .service.session import return_user_usecase_from_session
from ...infra.web.dependency.database import DatabaseDep
from ...infra.deps.database.dao.token import defaultUserTokenRepo
from ...application.user.usecase.token import ReturnUserUsecase


# TODO: Only use when acces web.
async def returncurrentuserwithsession(request: Request) -> None:
    return_user = return_user_usecase_from_session(
        DatabaseDep.fromrequest(request).session_maker, fetchsession
    )

    user = await return_user.request2user_slience(request)
    # print(f"User: {user}")
    request.ctx.current_user = user


def mountuserfromsession(wrapped):
    def decorate(func):
        @wraps(func)
        async def inner_func(request: Request, *args, **kwargs):
            await returncurrentuserwithsession(request)

            response = await func(request, *args, **kwargs)
            return response
        
        return inner_func
    
    return decorate(wrapped)
