""" `chestnut.infra.helpers.link`

    Some link related to app.
"""
from typing import Callable


# If you want to update, replace this to your website or repository.
APP_LINK: str = "https://github.com/GES233/Chestnut"
"""The link of application's website."""


DEPLOY_LINK: Callable[
    [bool, str, str | int], str
] = (
    lambda https, host, port: f"{'https' if https else 'http'}://{host}{':'+str(port) if port else ''}"
)
"""Return link from infos of website: `(https?, host, port => link)`"""
