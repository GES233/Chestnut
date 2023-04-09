from mistune.renderers.html import HTMLRenderer
from mistune.renderers.markdown import MarkdownRenderer
from mistune.util import escape
from typing import Any

# from ..helpers.config import DepsConfig as Config

from ...highlight import rendercode


class TinyUIRenderer(HTMLRenderer):
    """Customize version."""

    def __init__(
        self,
        escape: bool = True,
        allow_harmful_protocols: Any = None,
        # config: dict | None = None,
    ) -> None:
        super().__init__(escape, allow_harmful_protocols)

    def block_code(self, code: str, info: str | None = None) -> str:
        """Code with highlight."""

        return rendercode(code, info)
