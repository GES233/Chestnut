from pathlib import Path
from jinja2 import (
    Environment,
    select_autoescape,
    FileSystemLoader,
    BaseLoader,
)
from typing import Tuple


def returnloaderandenv(
    path: Path, enable_async: bool
) -> Tuple[BaseLoader, Environment]:
    loader = FileSystemLoader(path)

    environment = Environment(
        loader=loader,
        autoescape=select_autoescape(),
        enable_async=enable_async,
        extensions=["jinja2.ext.i18n"],
    )

    return loader, environment
