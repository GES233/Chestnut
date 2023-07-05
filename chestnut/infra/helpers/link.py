from typing import Callable


APP_LINK: str = "https://www.bing.com/new/"
"""The link of application's website."""

DEPLOY_LINK: Callable[
    [bool, str, str | int], str
] = (
    lambda https, host, port: f"{'https' if https else 'http'}://{host}{':'+str(port) if port else ''}"
)
"""Return link from infos of website: `(https?, host, port => link)`"""
