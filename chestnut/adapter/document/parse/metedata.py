import re
from pathlib import Path
from typing import Any, List

from ....application.document import exception as doc_exc
from ....application.document.domain.meta import DocumentMeta
from ....application.document.dto.load import DocumentLoader


class FilePathAdapter:
    """file path -> metadata."""
    
    @staticmethod
    def parse(
        content: str,
        file_path: Path | str,
        root_path: Path | str | None,
    ) -> dict:
        """Fetch metedata from file dir"""

        if not isinstance(file_path, Path):
            file_path = Path(file_path).absolute()

        # Check suffix.
        if file_path.suffix not in [".md", ".txt", ".rst", ".html"]:
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
                    "documents",
                ]:
                    break
                else:
                    root_path_list.append(dir_)
            root = root_path_list.pop(0)
            root_path = Path(root).joinpath(*root_path_list)
        if not root_path.is_absolute():
            root_path = root_path.absolute()

        location = [
            str(file_path)
            .removeprefix(str(file_path.anchor))
            # Avoid "C:\" & "c:\"
            .removeprefix(str(root_path).removeprefix(str(root_path.anchor)))
            .replace("\\", "/")
            .split("/")
        ]

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



class MetadataParserAdapter:
    """metadata segment -> metadata"""
    
    @staticmethod
    def parse(content: str) -> dict:
        ...
