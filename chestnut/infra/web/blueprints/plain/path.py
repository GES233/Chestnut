""" `chestnut.adapter.plain.path`
    ~~~~

    Some file path related to render-template.
"""
from pathlib import Path
from sanic import Blueprint

from ....helpers.path import MAIN_PUBLIC_PATH, ASSETS_PATH, STATIC_PATH


CSS_PATH = Path(STATIC_PATH / "css")
JS_PATH = Path(STATIC_PATH / "js")
FONTS_PATH = Path(MAIN_PUBLIC_PATH / "fonts")  # Common.


plain_static = Blueprint("launch")

# Add static.
plain_static.static("/static/css", CSS_PATH, name="css")
plain_static.static("/static/js", JS_PATH, name="js")
plain_static.static("/static/fonts", FONTS_PATH, name="fonts")
plain_static.static("/assets", ASSETS_PATH, name="assets")
