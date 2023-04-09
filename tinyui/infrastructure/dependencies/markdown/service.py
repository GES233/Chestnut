from mistune import Markdown

from .custome.inline import DocDiffLangParser
from .custome.renderer import TinyUIRenderer


class DocumentMarkdown(Markdown):
    """To represent content in `/docs`."""

    def __init__(self, block=None, inline=None, plugins=None):
        if not inline:
            inline = DocDiffLangParser()
        renderer = TinyUIRenderer(escape=False)

        super().__init__(renderer, block, inline, plugins)
