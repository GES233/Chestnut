import re
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Any, Tuple, Callable

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...base.dto.io import InputSchemaMixin
from ...base.dto.db import DataAccessObjectMixin


# TODO: Replace as `DAOMixin`
class DocumentLoader(InputSchemaMixin, BaseModel):
    content: str
    # Same as DocumentMeta.
    name: str
    title: str | None
    language: str
    source: Path
    location: str
    categories: List[str | None]

    @classmethod
    def fromdict(
        cls, input_dict: dict, read_service: Callable[[str | Path], str]
    ) -> "DocumentLoader":
        """`file_path` and `root_path` required."""

        # input_dict: ["file_path"], ["root_path"]
        content = read_service(input_dict["file_path"])

        return DocumentLoader(
            content=content,
            **DocumentLoader.parse(
                content=content,
                file_path=input_dict["file_path"],
                root_path=input_dict["root_path"],
            ),
        )

    def toentity(self) -> Document:
        return DocumentLoader.sqeeze(
            content=self.content,
            meta_dict=dict(
                name=self.name,
                title=self.title,
                language=self.language,
                source=self.source,
                location=self.location,
                categories=self.categories,
            ),
        )

    @staticmethod
    def parse(
        content: str,
        file_path: Path | str,
        root_path: Path | str | None,
    ) -> dict:
        # Let the limitation of spec into domain knowledge.

        if not isinstance(file_path, Path):
            file_path = Path(file_path).absolute()

        # Check suffix.
        if file_path.suffix not in [".md", ".rst", ".html"]:
            raise doc_exc.DocumentFormatInvalid
        else:
            doc_format = file_path.suffix

        # Parse paths.
        if root_path is not None:
            if isinstance(root_path, str):
                root_path = Path(root_path)
        else:
            # Let's guess root_path.
            path_segments = file_path.parts
            root_path_list: List[Any] = []
            for dir_ in path_segments:
                if dir_ in [
                    "doc",
                    "docs",
                    "document",
                ]:
                    break
                else:
                    root_path_list.append(dir_)
            root = root_path_list.pop(0)
            root_path = Path(root).joinpath(*root_path_list)
        if not root_path.is_absolute():
            root_path = root_path.absolute()

        location = (
            str(file_path)
            .removeprefix(str(file_path.anchor))
            # Avoid "C:\" & "c:\"
            .removeprefix(str(root_path).removeprefix(str(root_path.anchor)))
            .replace("\\", "/")
        )

        # assert len(file_path.suffixes.remove(file_path.suffix)) == 1
        suffixes = file_path.suffixes.copy()
        suffixes.remove(doc_format)
        language = (suffixes or [".en"])[0].strip(".")

        if title := re.match(r"^# (.*)\n", content, re.MULTILINE):
            title = title.group(1)

        return dict(
            name=file_path.name.split(".")[0],
            title=title,
            language=language,
            source=file_path,
            location=location,
            categories=[],
        )

    @staticmethod
    def sqeezetometa(meta_dict: dict) -> DocumentMeta:
        return DocumentMeta(
            name=meta_dict["name"],
            title=meta_dict.get("title", None),
            language=meta_dict["language"],
            source=meta_dict["source"],
            location=meta_dict["location"],
            categories=meta_dict["categories"],
        )

    @staticmethod
    def sqeeze(content: str, meta_dict: dict) -> Document:
        meta = DocumentLoader.sqeezetometa(meta_dict=meta_dict)
        return Document(id=meta.name, meta=meta, content=content)
