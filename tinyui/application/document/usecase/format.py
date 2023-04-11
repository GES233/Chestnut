from typing import Callable, Any

from ..domain.repo import DocRepo


class DocumentFormatpr:
    repo: DocRepo
    convert_service: Callable[[str], str]

    def __init__(self, repo: DocRepo, convert_service: Callable[..., str]) -> None:
        self.repo = repo
        self.convert_service = convert_service
