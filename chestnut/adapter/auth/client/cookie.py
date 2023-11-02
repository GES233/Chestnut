import base64
from datetime import datetime, timedelta
from sanic.request import Request
from sanic.response import HTTPResponse

# from ..service.session import

SESSION_KEY = "Authentication"
SESSION_FROM_ = lambda cookie_jar: cookie_jar.get(SESSION_KEY)


def setsession(
    response: HTTPResponse, session_token: bytes, expire: timedelta | None
) -> HTTPResponse:
    response.add_cookie(
        SESSION_KEY,
        sessionbytes2str(session_token),
        secure=False,
        expires=datetime.utcnow() + expire if expire else None,
    )

    return response

def releasesession(
    response: HTTPResponse
) -> HTTPResponse:
    response.delete_cookie(SESSION_KEY)

    return response


def fetchsession(request: Request) -> bytes:
    return sessionstr2bytes(SESSION_FROM_(request.cookies))


def sessionstr2bytes(cookie: str) -> bytes:
    return base64.b64decode(bytes(cookie, encoding="utf-8"))


def sessionbytes2str(en: bytes) -> str:
    return str(base64.b64encode(en), encoding="utf-8")
