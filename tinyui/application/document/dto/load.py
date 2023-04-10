import re
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Tuple

from .. import exception as doc_exc
from ..domain.meta import DocumentMeta
from ..domain.document import Document
from ...base.dto.io import InputSchemaMixin


class DocumentLoader(InputSchemaMixin, BaseModel):
    content: str | None
    meta: DocumentMeta

    @classmethod
    def fromdict(cls, input_dict: dict) -> "DocumentLoader":
        # input_dict: ["file_path"], ["root_path"]
        content = cls.fetchfile(input_dict["file_path"])

        return DocumentLoader(
            content=content,
            meta=DocumentLoader.parse(
                content=content,
                file_path=input_dict["file_path"],
                root_path=input_dict["root_path"]
            )
        )

    def toentity(self) -> Document:
        return DocumentLoader.sqeeze(self.content, self.meta)

    @staticmethod
    def fetchfile(path: str | Path) -> str:
        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise doc_exc.DocumentNotFound
        
        return path.read_text(encoding="utf-8")

    @staticmethod
    def parse(
        content: str,
        file_path: Path | str,
        root_path: Path | str | None,
    ) -> DocumentMeta:
        # Let the limitation of spec into domain knowledge.

        # Check suffix.
        if file_path.suffix not in [".md", ".rst", ".html"]:
            raise doc_exc.DocumentFormatInvalid
        else:
            doc_format = file_path.suffix

        # Parse paths.
        if isinstance(file_path, str):
            file_path = Path(file_path)
            if not file_path.is_absolute():
                file_path = file_path.absolute()
        if root_path is not None:
            if isinstance(root_path, str):
                root_path = Path(root_path)
        else:
            # Let's guess root_path.
            path_segments = file_path.parts
            root_path = []
            for dir_ in path_segments:
                if dir_ in ["doc", "docs", "document",]:
                    break
                else:
                    root_path.append(dir_)
            root = root_path.pop(0)
            root_path = Path(root).joinpath(*root_path)
        if not root_path.is_absolute():
            root_path = root_path.absolute()

        location = (
            str(file_path)
            .removeprefix(str(file_path.anchor))
            # Avoid "C:\" & "c:\"
            .removeprefix(str(root_path).removeprefix(str(root_path.anchor)))
            .replace("\\", "/")
        )

        language = (file_path.suffixes.remove[doc_format] or ["en"])[0]

        if title := re.match(r"^# (.*)\n", content, re.MULTILINE):
                title = title.group(1)

        return DocumentMeta(
            name=file_path.name.split["."][0],
            title=title,
            language=language,
            source=root,
            location=location,
            categories=[],
        )
    
    @staticmethod
    def sqeeze(content: str, meta: DocumentMeta) -> Document:
        return Document(
            id=meta.name,
            meta=meta,
            content=content
        )
