from pathlib import Path
from sanic import Blueprint

from .page import add_router
from .....deps.document.dir import build_index


def create_blueprint(
    docs_path: str | Path, assets_path: str | Path | None = None
) -> Blueprint:
    if isinstance(docs_path, str):
        docs_path = Path(docs_path)
    if assets_path:
        if isinstance(assets_path, str):
            assets_path = Path(assets_path)

    docs_bp = Blueprint("plain_docs_bp", url_prefix="/docs")
    docs_bp.static("/docs/assets", assets_path if assets_path else docs_path / "assets")

    # TODO: Update it from database.
    # Why closure?
    def build_index_to_route(bp: Blueprint, main_path: Path) -> None:
        docs_list = build_index(main_path, True)

        for docs_item in docs_list:
            uri = "/" + docs_item["lang"] + "/".join(docs_item["relative"])
            name = docs_item["name"]
            content = docs_item["content"]
            bp.add_route(
                add_router(content, name),
                uri,
                name="_".join(docs_item["relative"]),
            )

    build_index_to_route(docs_bp, docs_path)

    return docs_bp
