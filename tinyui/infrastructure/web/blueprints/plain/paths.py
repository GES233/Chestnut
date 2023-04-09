""" `tinyui.adapter.plain.paths`
    ~~~~

    Some file path related to render-template.
"""
from pathlib import Path
from sanic import Blueprint

from ....helpers.path import MAIN_PUBLIC_PATH, ASSETS_PATH


# Configure Paths(it is stable).
PLAIN_PATH = Path(MAIN_PUBLIC_PATH / "plain")

# Add to `reload_dir`!
TEMPLATE_PATH = Path(PLAIN_PATH / "template")

STATIC_PATH = Path(PLAIN_PATH / "static")
CSS_PATH = Path(STATIC_PATH / "css")
JS_PATH = Path(STATIC_PATH / "js")
FONTS_PATH = Path(MAIN_PUBLIC_PATH / "fonts")  # Common.


launch_static = Blueprint("launch")

# Add static.
launch_static.static("/static/css", CSS_PATH, name="css")
launch_static.static("/static/js", JS_PATH, name="js")
launch_static.static("/static/fonts", FONTS_PATH, name="fonts")
launch_static.static("/assets", ASSETS_PATH, name="assets")
