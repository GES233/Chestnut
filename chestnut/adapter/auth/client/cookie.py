import base64
from datetime import datetime, timedelta
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.cookies import Cookie

# from ..service.session import

SESSION_KEY = "Authentication"
SESSION_FROM_ = lambda cookie_jar: cookie_jar[SESSION_KEY]


def setsession(
    response: HTTPResponse, session_token: bytes, expire: timedelta | None
) -> HTTPResponse:
    response.add_cookie(
        SESSION_KEY,
        str(base64.b64encode(session_token), encoding="utf-8"),
        expires=datetime.utcnow() + expire if expire else None,
    )

    return response


def fetchsession(request: Request) -> bytes:
    return base64.b64decode(bytes(SESSION_FROM_(request.cookies), encoding="utf-8"))
