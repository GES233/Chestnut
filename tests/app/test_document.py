import pytest

import re
import asyncio
from pathlib import Path
from sqlalchemy import Table
from sqlalchemy.sql import select, update
from sqlalchemy.orm import registry
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from typing import Any, Callable, Dict, Coroutine, List

# If this architecture is still used for the next project,
# I'll DEFINENITELY NOT use the full word.
from tinyui.application.document.domain.document import Document
from tinyui.application.document.domain.meta import DocumentMeta
from tinyui.application.document.domain.repo import DocRepo, DocMetaRepo
from tinyui.application.document.dto.load import DocumentLoader
from tinyui.application.document.dto.present import DocumentPresenter
from tinyui.application.document.usecase.display import DisplayIndex
from tinyui.application.document.usecase.shown import DisplayDocument
from tinyui.application.document import exception as doc_exc
from tinyui.infrastructure.helpers.config import DepsConfig
from tinyui.infrastructure.helpers.path import INSTANCE_PATH
from tinyui.infrastructure.dependencies.database.dao.base import tiny_sqlite_metadata
from tinyui.infrastructure.dependencies.database.dao.document import document_table
from tinyui.infrastructure.dependencies.database.service import enginefromconfig
from tinyui.infrastructure.dependencies.database.settings import database_test


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


def fetchfile(path: str | Path) -> str:
    if not isinstance(path, Path):
        path = Path(path)

    if not path.exists():
        raise doc_exc.DocumentNotFound

    return path.read_text(encoding="utf-8")


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
            location="/".join(["wild", "breeding", "chicken"]),
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
            location="/".join(["wild", "breeding", "chicken"]),
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
        fake_file_path = Path(
            "C:/root/docs/why/chicken/is/beautiful/chicken_is_nice.zh.md"
        )
        fake_root_path = Path("C:/root/docs")
        parsed_meta = DocumentLoader.parse(
            content=DOCUMENT_RAW_CONTENT,
            file_path=fake_file_path,
            root_path=fake_root_path,
        )

        assert parsed_meta.get("name") == "chicken_is_nice"
        assert parsed_meta.get("language") == "zh"

    def test_fetchfile_and_present(self) -> None:
        # 1. Fetch.
        file_path, root_path = self._store_file(
            "chicken_is_nice.zh.md", DOCUMENT_RAW_CONTENT
        )
        demo_loader = DocumentLoader.fromdict(
            input_dict=dict(file_path=file_path, root_path=root_path),
            read_service=fetchfile,
        )
        demo_obj = demo_loader.toentity()

        assert demo_obj.meta.title == "只因的美学"

        # 2. Present.
        presenter = DocumentPresenter.fromentity(demo_obj)
        assert presenter.dict()["title"] == "只因的美学"


def run_sync(func: Callable[..., Coroutine], **inputs) -> Any:
    return asyncio.get_event_loop().run_until_complete(func(**inputs))


class SimpleRepoImpl(DocRepo, DocMetaRepo):
    db: List[Document] = []

    def __init__(self) -> None:
        self.db = []

    async def display(self) -> List[DocumentMeta | None]:
        return [item.meta for item in (doc_item for doc_item in self.db)]

    async def loadbyname(self, name: str) -> List[Document | None]:
        return [item for item in self.db if item.meta.name == name]

    async def loadbycondition(self, **condition) -> List[Document | None]:
        raise NotImplementedError

    async def upgrade(self, add_object: Document) -> None:
        self.db.append(add_object)


mapper_registry = registry()


class DefaultRepo(DocRepo, DocMetaRepo):
    """Implementation with database"""

    engine: AsyncEngine
    table: Table

    def __init__(self, config: DepsConfig, table: Table) -> None:
        self.engine = enginefromconfig(config)
        self.table = table

        # TODO: create all.
        mapper_registry.map_imperatively(Document, document_table)

    async def display(self) -> List[DocumentMeta | None]:
        async with self.engine.begin() as conn:
            stmt = select(document_table)
            await conn.execute(stmt)
            ...
        # Table => DTO => DomainModel
        # Table =mapper=> DomainModel
        raise NotImplementedError

    async def loadbycondition(self, **condition) -> List[Document | None]:
        async with self.engine.begin() as conn:
            stmt = select(document_table).where()
            ...
        raise NotImplementedError

    async def loadbyname(self, name: str) -> List[Document | None]:
        return await self.loadbycondition(name=name)

    async def upgrade(self, add_object: Any) -> None:
        async with self.engine.begin() as conn:
            stmt = update(document_table).where().values()
            ...
        raise NotImplementedError


class TestUsecase:
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

    def _add_markdown(self, repo: DocRepo, add_object: Document) -> None:
        run_sync(repo.upgrade, add_object=add_object)

    def _pre(self, repo: DocRepo) -> None:
        """Append file when test."""

        file_path, root_path = self._store_file("1.md", DOCUMENT_RAW_CONTENT)
        self._add_markdown(
            repo=repo,
            add_object=DocumentLoader.fromdict(
                input_dict=dict(file_path=file_path, root_path=root_path),
                read_service=fetchfile,
            ).toentity(),
        )

        file_path, root_path = self._store_file("2.md", DOCUMENT_RAW_CONTENT)
        self._add_markdown(
            repo=repo,
            add_object=DocumentLoader.fromdict(
                input_dict=dict(file_path=file_path, root_path=root_path),
                read_service=fetchfile,
            ).toentity(),
        )

    def test_diaplay_index(self, repo=SimpleRepoImpl()) -> None:
        self._pre(repo=repo)
        usecase = DisplayIndex(repo=repo)

        index_list = run_sync(usecase)

        assert len(index_list) == 2

        item_1: DocumentPresenter = index_list[0]

        assert item_1.name == "1"
        assert item_1.language == "en"

    def test_display_file(self, repo=SimpleRepoImpl()) -> None:
        self._pre(repo=repo)
        usecase = DisplayDocument(repo=repo)

        item_1: DocumentPresenter = run_sync(usecase.show, name="2")

        assert item_1.name == "2"
        assert "\n" in item_1.content
