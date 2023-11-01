from datetime import timedelta
from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any

from ...auth.decorators import mountuserfromsession


@mountuserfromsession
async def returnuserprofile(request: Request) -> HTTPResponse:
    ...


async def editmyprofile(request: Request) -> HTTPResponse:
    ...
