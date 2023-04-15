from typing import Callable, Any

from .. import exception as doc_exc
from .repo import DocRepo


class DocumentFormater:
    raw_content: str
    convert_service: Callable[[str], str]

    def __init__(self, raw: str, convert_service: Callable[..., str]) -> None:
        self.raw_content = raw
        self.convert_service = convert_service

    def __str__(self) -> str:
        try:
            content = self.convert_service(self.raw_content)
        except Exception:
            raise doc_exc.DocumentFormatInvalid
        else:
            if content == "":
                raise doc_exc.DocumentFormatInvalid
            return content
