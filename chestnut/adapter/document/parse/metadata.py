import re
from pathlib import Path
from typing import Any, List

from ....application.document import exception as doc_exc
from ....application.document.domain.meta import DocumentMeta
from ....application.document.dto.load import DocumentLoader


MD_TITLE_PATTERN = re.compile(r"(^# (.*)\n)|(.*\n# (.*)\n)|((.*)\n^=.*\n)", re.MULTILINE)
# match-group-2: r"(^# (.*)\n)"    =>      ("# ABC\n..." -> "ABC")
# match-group-4: r"(.*\n# (.*)\n)" => ("...\n# ABC\n..." -> "ABC")
# match-group-6: r"((.*)\n^=.*\n)" =>        ("ABC\n=.." -> "ABC")


# from https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/meta.py
#META_PATTERN = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
#META_MORE_PATTERN = re.compile(r'^[ ]{4,}(?P<value>.*)')
META_BEGIN_PATTERN = re.compile(r"^-{3}(\s.*)?")
META_END_PATTERN = re.compile(r"^(-{3}|\.{3})(\s.*)?")


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

        return dict(
            name=file_path.name.split(".")[0],
            title=FilePathAdapter._gettitle(content),
            language=language,
            source=file_path,
            location=location,
            categories=[],
        )

    @staticmethod
    def _gettitle(content: str) -> str | None:
        """Return title."""

        if title := MD_TITLE_PATTERN.match(content):
            title = (
                title.group(2)
                # r"(^# (.*)\n)"    =>      ("# ABC\n..." -> "ABC")
                or title.group(4)
                # r"(.*\n# (.*)\n)" => ("...\n# ABC\n..." -> "ABC")
                or title.group(6)
                # r"((.*)\n^=.*\n)" =>        ("ABC\n=.." -> "ABC")
            )

        if isinstance(title, str):
            return title
        else:
            return None


class MetadataParserAdapter:
    """metadata segment -> metadata"""

    @classmethod
    def parse(cls, content: str) -> dict:
        ...

    def _fetchmetadata(self, raw_content: str) -> str:
        """"""

        # """---\n...\n---\n...""" => "---\n...\n---"
        ...

