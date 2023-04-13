import re
from pathlib import Path
from typing import Any, Dict, List


def build_index(main_path: Path, readcontent: bool) -> List[Dict[str, Any]]:
    index_list = []

    for file in main_path.rglob("*.md"):
        """Content example:

        {
            'lang': 'cmn-Hans',
            'name': 'newbie',
            'path': '...\\Chestnut\\docs\\guide\\newbie.cmn-Hans.md',
            'relative': ['guide', 'newbie'],
            'title': '面向萌新的安装指南',
        }
        """
        # Relative path.
        _relative_path = (
            str(file)
            .removeprefix(str(main_path))  # Remove prefix
            .removesuffix(".md")  # Remove markdown
            .split(".")[0]  # If have language part, remove it.
            .replace("\\", "/")
            .split("/")
        )
        _file_name = (
            str(file)
            .removeprefix(str(main_path))  # Remove prefix
            .removesuffix(".md")  # Remove markdown
            .replace("\\", "/")
            .split("/")[-1]
        )
        # Remove blank element.
        _relative_path.pop(0)

        # Name and language.
        if "." in _file_name:
            file_name = _file_name.split(".")[0]
            lang = _file_name.split(".")[-1]
        else:
            file_name = _file_name
            lang = "en"

        _file_dict: Dict[str, str | List | None] = dict(
            path=str(file),
            relative=_relative_path,
            name=file_name,
            lang=lang,
            content=None,
            title=None,
        )
        if readcontent:
            content = file.read_text(encoding="utf-8")
            if title := re.match(r"^# (.*)\n", content, re.MULTILINE):
                title = title.group(1)
            _file_dict["content"] = content
            _file_dict["title"] = title

        index_list.append(_file_dict)

    return index_list
