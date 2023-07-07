import re
from typing import Callable, Dict


# Only `#`: ^(#+ .*)\n
# Only `-` or `=`: ^(.*\n+(=|-)\n)
MARKDOWN_HEADER_PATTERN = re.compile(
    r"^(#+ .*)\n|^(.*\n+(=|-)\n)",  # Only one group.
    re.MULTILINE,
)


def getmarkdownheaderbody(header: str) -> str:
    header.split(" ").remove(header.split(" ")[0])
    return " ".join(header)


header_dict: Dict[str, int] = {"=": 1, "-": 2}


getmarkdownheaderlength: Callable[[str], int] = (
    lambda header: len(header.split(" ")[0])
    if "\n" not in header
    else header_dict[header.split("\n")[1][0]]
)
"""Return the level in header."""


class HeaderParser:
    ...
