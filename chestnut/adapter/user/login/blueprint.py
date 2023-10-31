from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from typing import Any


async def loginpresentation(request: Request) -> HTTPResponse:
    ...


async def login(request: Request) -> HTTPResponse:
    ...


async def logout(request: Request) -> HTTPResponse:
    ...
