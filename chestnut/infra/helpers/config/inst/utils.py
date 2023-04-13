from pathlib import Path
from typing import Dict, Callable, Any


_convert_boolean = lambda boolean: str(boolean).lower()
_convert_string = (
    lambda content: '"' + content + '"'
    if "\n" not in content
    else '"""\n' + content + '"""'.replace("\r\n", "\n")
)
_convert_char = lambda content: "'" + str(content) + "'"


def convert(value: Any) -> str:
    if isinstance(value, bool):
        return _convert_boolean(value)
    elif isinstance(value, str):
        if "\\" in value or "/" in value:
            return _convert_char(value)
        else:
            return _convert_string(value)
    elif isinstance(value, Path):
        return _convert_char(value)
    elif not value:
        return '""'
    else:
        return value


def multivaluecontent(
    root: str,
    content: str | Dict[str, str],
    convert: Callable[[str], str],
) -> str:
    if isinstance(content, dict):
        return "\n".join(
            [root + "." + key + " = " + convert(content[key]) for key in content]
        )
    else:
        return root + " = " + convert(content)
