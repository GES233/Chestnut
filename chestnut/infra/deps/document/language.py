import re

LINK_PATTERN = r"(?<!!)\[(.*?)\]\((.*?)(\.md)\)|\[(.*?)\]\((.*?)(.rst)\)"
"""To `[xxx](xxx.md)` and `[xxx](xxx.rst)`"""
link_pt = re.compile(LINK_PATTERN)


def nametoroute(content: str, name_lang_patter: str) -> str:
    """Let [name](Blabla.md) to [name](Blabla)."""

    # Parse process.
    file_link_all = re.findall(link_pt, content, re.MULTILINE)

    if len(file_link_all) == 0:
        return content
    else:
        for file_link in file_link_all:
            # Parse if the language exist.
            # lang, name = ...
            ...

            # If matched, replace it.
            ...
        return ""

    # return content.replace("q", name_lang_patter.format(...))
