from pathlib import Path

from ...core.document import exception as doc_exc


def fetchdocumentfromfile(path: str | Path) -> str:
    if not isinstance(path, Path):
        path = Path(path)

    if not path.exists():
        raise doc_exc.DocumentNotFound

    return path.read_text(encoding="utf-8")
