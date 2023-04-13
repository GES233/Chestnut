from sanic.request import Request
from sanic.errorpages import exception_response
from sanic.handlers import ErrorHandler

from .plain import CustomeHTMLRenderer
from ...blueprints.api import API_PREFIX


class CustomeErrorHandler(ErrorHandler):
    def default(self, request: Request, exception: Exception):
        self.log(request, exception)

        # Parse requiest link.
        url = request.path

        if not url.startswith(API_PREFIX):
            return exception_response(
                request,
                exception,
                debug=self.debug,
                base=self.base,
                fallback="html",
                renderer=CustomeHTMLRenderer,
            )
        else:
            fallback = request.app.config.FALLBACK_ERROR_FORMAT
            return exception_response(
                request,
                exception,
                debug=self.debug,
                base=self.base,
                fallback=fallback,
                renderer=None,  # type:ignore
            )
