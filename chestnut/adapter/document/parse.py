import re
from typing import Callable


MARKDOWN_HEADER_PATTERN = re.compile(
    r"^(#+ .*)\n",  # Only one group.
    re.MULTILINE,
)


def getmarkdownheaderbody(header: str) -> str:
    header.split(" ").remove(header.split(" ")[0])
    return " ".join(header)


getmarkdownheaderlength: Callable[[str], int] = lambda header: len(header.split(" ")[0])
"""Return the number of `'#'` in header."""
