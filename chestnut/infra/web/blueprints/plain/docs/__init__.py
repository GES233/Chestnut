""" `chestnut.adapter.plain.docs`
    ~~~~

    Render documents in `/docs`.

    In main application, the documents may presented with front-end renderer.
"""
from .bp import create_blueprint
from .....helpers.path import DOCS_PATH, DOCS_ASSETS_PATH


docs_bp = create_blueprint(DOCS_PATH, DOCS_ASSETS_PATH)
