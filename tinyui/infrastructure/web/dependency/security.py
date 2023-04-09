from sanic import Sanic
from sanic.request import Request
from typing import Dict, Any

from .base import DepsInterface
from ..settings.location import CONFIG_LOCATION
from ...dependencies.security import service


class SecurityDep(DepsInterface):
    def __init__(self, crypto_dict: dict) -> None:
        ...

    @classmethod
    def fromrequest(cls, request: Request) -> "SecurityDep":
        assert "crypto_dict" in request.app.ctx and isinstance(
            request.app.ctx.crypto_dict, dict
        )

        return SecurityDep(crypto_dict=request.app.ctx.crypto_dict)


def add_dependency_crypt(app: Sanic, enable: bool) -> None:
    app.ctx.crypto_dict = service.cryptfromconfig(
        app.config[CONFIG_LOCATION["security"]]
    )

    if enable:
        # Add `type` and `builder` of session.
        app.ext.add_dependency(SecurityDep, SecurityDep.fromrequest)
