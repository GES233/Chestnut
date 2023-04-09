from jinja2 import Template
from typing import Iterable

from .utils import convert
from ...config import AppConfig, DepsConfig


# Dependency.
SERVER_DEPENDENCY_TEMPLATE = r"""[deps.{{ name }}]
{% if enable -%}
enable = true
{% for key in values -%}
{% if values[key] -%}
{{ key }} = {{ convert(values[key]) }}
{% else -%}
{{ key }} = ""  # `{{ key.upper() }}` is None.
{% endif -%}
{% endfor -%}
{% else -%}
enable = false
{% endif -%}
"""


def createdepsconfig(deps: Iterable[DepsConfig]) -> str:
    """"""

    template = Template(SERVER_DEPENDENCY_TEMPLATE)

    res = "\n".join(
        [
            template.render(
                name=dep.name,
                enable=dep.enable,
                values=dep.values,
                convert=convert,
            )
            for dep in deps
        ]
    ).replace("\r\n", "\n")

    return res


APPLICATION_TEMPLATE = r"""# Generate automatically, please adjust!!
[app]
name = {{ convert(app.name) }}
installed = {{ convert(app.installed) }}
build = {{ convert(app.build) }}
use_https = {{ convert(app.use_https) }}
introduction = {{ convert(app.introduction) }}
website = {{ convert(app.website) }}
lang = {{ convert(app.lang) }}
{% if app.description -%}
description = {{ convert(app.description) }}
{%- endif -%}
"""


def createappconfig(app: AppConfig) -> str:
    """Renderer app's part."""

    template = Template(APPLICATION_TEMPLATE)

    return template.render(
        app=app,
        convert=convert,
    )


# Prerequisite.
PREREQUISITE_TEMPLATE = r"""[prerequisite.{{ name }}]
{{ multivaluecontent("check", prerequisite.check, convert) }}
{{ multivaluecontent("description", prerequisite.description, convert) }}
{{ multivaluecontent("url", prerequisite.url, convert) }}
"""
