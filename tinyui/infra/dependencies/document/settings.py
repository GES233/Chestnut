from pathlib import Path

from ...helpers.config.dependency import DepsConfig
from ...helpers.path import DOCS_PATH, DOCS_ASSETS_PATH


document = DepsConfig(
    "document",
    True,
    dict(
        path=DOCS_PATH,
        assets=DOCS_ASSETS_PATH,
        language="en",
    ),
)
