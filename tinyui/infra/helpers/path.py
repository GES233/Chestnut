""" `tinyui.infra.helpers.path`
    ~~~~

    Present Paths.
"""
from pathlib import Path
from typing import Callable


PROJECT_PATH = Path(__file__).cwd()
BACKEND_PATH = Path(PROJECT_PATH / "tinyui")
INSTANCE_PATH = Path(PROJECT_PATH / "instance")
INSTANCE_CONFIG_PATH: Callable[[str | int | None], Path] = lambda app_id: Path(
    INSTANCE_PATH / "config.toml"
    if not app_id
    else INSTANCE_PATH / ("config_" + str(app_id) + ".toml")
)
DOCS_PATH = Path(PROJECT_PATH / "docs")
DOCS_ASSETS_PATH = Path(DOCS_PATH / "assets")
MAIN_PUBLIC_PATH = Path(PROJECT_PATH / "public")
ASSETS_PATH = Path(MAIN_PUBLIC_PATH / "assets")
TEMPLATE_PATH = Path(MAIN_PUBLIC_PATH / "template")
STATIC_PATH = Path(MAIN_PUBLIC_PATH / "static")
FONTS_PATH = Path(MAIN_PUBLIC_PATH / "fonts")  # Common.
