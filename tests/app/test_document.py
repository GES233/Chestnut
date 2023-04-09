import pytest

import re
from pathlib import Path

from tinyui.application.document.domain.document import Document
from tinyui.application.document.domain.meta import DocumentMeta
from tinyui.application.document.domain.repo import DocRepo, DocMetaRepo


DOCUMENT_RAW_CONTENT = """# 只因的美学

by 呕像恋蜥僧

> 迎面走来的你让我如此蠢蠢欲动
> 这种感觉我从未有 Cause I got a crush on you, who you
> 你是我的，我是你的谁
> 再多一眼看一眼就会爆炸
> 再近一点靠近点快被融化
> 想要把你占为己有baby bae
> 不管走到哪里都会想起的人是you you
> _——《只因你太美》_

"""


class TestDocumentDomain:
    def test_document(self) -> None:
        if title_ := re.match(r"^# (.*)\n", DOCUMENT_RAW_CONTENT, re.MULTILINE):
            title = title_.group(1)
        else:
            title = None
        demo_doc = Document(
            name="awesome_chicken",
            # from tinyui/infra/deps/document/dir/build_index
            title=title,
            source=Path(__file__),
            location=["wild", "breeding", "chicken"],
            categories=[],
            content=DOCUMENT_RAW_CONTENT
        )

        assert demo_doc.name == "awesome_chicken"
        assert demo_doc.title == "只因的美学"
    
    def test_document_meta(self) -> None:
        if title_ := re.match(r"^# (.*)\n", DOCUMENT_RAW_CONTENT, re.MULTILINE):
            title = title_.group(1)
        else:
            title = None
        demo_meta = DocumentMeta(
            name="awesome_chicken",
            # from tinyui/infra/deps/document/dir/build_index
            title=title,
            source=Path(__file__),
            location=["wild", "breeding", "chicken"],
            categories=[],
            # content=DOCUMENT_RAW_CONTENT
        )

        assert demo_meta.title is not None and "\n" not in demo_meta.title
