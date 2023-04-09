from sanic import Sanic
from sanic_ext.extensions.http.extension import HTTPExtension
from sanic_ext.extensions.openapi.extension import OpenAPIExtension
from sanic_ext.extensions.injection.extension import InjectionExtension
from typing import List

from .extend import CustomeExtend as Extend
from .template.extension import CustomeTemplatingExtension


def configure_extensions(app: Sanic, launch: bool = False) -> None:
    """Configure some Sanic extensions."""

    extensions: List = (
        [
            HTTPExtension,
            OpenAPIExtension,
            InjectionExtension,
            CustomeTemplatingExtension,
        ]
        if not launch
        else [CustomeTemplatingExtension]
    )

    Extend(
        app=app,
        extensions=extensions,  # type: ignore
        built_in_extensions=False,
    )
