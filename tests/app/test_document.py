import pytest

import re
from pathlib import Path, PurePath

from tinyui.application.document.domain.document import Document
from tinyui.application.document.domain.meta import DocumentMeta
from tinyui.application.document.domain.repo import DocRepo, DocMetaRepo
from tinyui.application.document.dto.load import DocumentLoader
from tinyui.application.document.dto.present import DocumentPresenter
from tinyui.infrastructure.helpers.path import INSTANCE_PATH


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
    def test_document_meta(self) -> None:
        if title_ := re.match(r"^# (.*)\n", DOCUMENT_RAW_CONTENT, re.MULTILINE):
            title = title_.group(1)
        else:
            title = None
        demo_meta = DocumentMeta(
            name="awesome_chicken",
            # from tinyui/infra/deps/document/dir/build_index
            title=title,
            language="cmn-Hans",
            source=Path(__file__),
            location=["wild", "breeding", "chicken"],
            categories=[],
            # content=DOCUMENT_RAW_CONTENT
        )

        assert demo_meta.title is not None and "\n" not in demo_meta.title

    def test_document(self) -> None:
        if title_ := re.match(r"^# (.*)\n", DOCUMENT_RAW_CONTENT, re.MULTILINE):
            title = title_.group(1)
        else:
            title = None

        demo_meta = DocumentMeta(
            name="awesome_chicken",
            # from tinyui/infra/deps/document/dir/build_index
            title=title,
            language="cmn-Hans",
            source=Path(__file__),
            location=["wild", "breeding", "chicken"],
            categories=[],
            # content=DOCUMENT_RAW_CONTENT
        )

        demo = Document(
            id=demo_meta.name,
            meta=demo_meta,
            content=DOCUMENT_RAW_CONTENT,
        )

        assert demo.meta.name == demo.id


class TestDTO:
    def _store_file(self, file_name: str, content: str) -> tuple:
        if not INSTANCE_PATH.exists():
            INSTANCE_PATH.mkdir()
        if not (INSTANCE_PATH / "test").exists():
            (INSTANCE_PATH / "test").mkdir()
        if not (INSTANCE_PATH / "test/docs/").exists():
            (INSTANCE_PATH / "test/docs/").mkdir()

        TEST_FILE_PATH = INSTANCE_PATH / "test/docs/"

        if not (TEST_FILE_PATH / file_name).exists():
            (TEST_FILE_PATH / file_name).touch()
            (TEST_FILE_PATH / file_name).write_text(data=content, encoding="utf-8")
        
        return (TEST_FILE_PATH / file_name), TEST_FILE_PATH

    def test_parse(self) -> None:
        fake_file_path = Path("C:/root/docs/why/chicken/is/beautiful/chicken_is_nice.zh.md")
        fake_root_path = Path("C:/root/docs")
        parsed_meta = DocumentLoader.parse(
            content=DOCUMENT_RAW_CONTENT,
            file_path=fake_file_path,
            root_path=fake_root_path,
        )

        assert parsed_meta.name == "chicken_is_nice"
        assert parsed_meta.language == "zh"

    def test_fetchfile(self) -> None:
        file_path, root_path = self._store_file("chicken_is_nice.zh.md", DOCUMENT_RAW_CONTENT)
        demo_loader = DocumentLoader.fromdict(dict(file_path=file_path, root_path=root_path))
        demo_obj = demo_loader.toentity()

        assert demo_obj.meta.title == "只因的美学"
