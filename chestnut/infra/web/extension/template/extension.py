# A RE-implementation of sanic_ext.template.
from sanic_ext.extensions.templating.extension import TemplatingExtension
from sanic_ext.extensions.templating.engine import Templating
from sanic_ext.bootstrap import Extend

# from ..extend import CustomeExtend
from ....helpers.path import TEMPLATE_PATH
from ....deps.html.service import returnloaderandenv


class CustomeTemplatingExtension(TemplatingExtension):
    name = "customtemplating"

    def startup(self, bootstrap: Extend) -> None:
        self._add_template_paths_to_reloader([TEMPLATE_PATH])

        loader, launch_environment = returnloaderandenv(TEMPLATE_PATH, True)

        if not hasattr(bootstrap, "environment"):
            bootstrap.environment = launch_environment
        if not hasattr(bootstrap, "templating"):
            bootstrap.templating = Templating(
                environment=bootstrap.environment, config=self.config
            )
