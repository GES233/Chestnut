""" `tinyui.infra.web.exception`
    ~~~~

    Implementation some Exceptions.
"""
from sanic import Sanic

from .errorhandler import CustomeErrorHandler


def configure_exceptions(app: Sanic) -> None:
    app.error_handler = CustomeErrorHandler()
