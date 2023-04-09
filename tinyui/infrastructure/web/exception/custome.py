from sanic.exceptions import SanicException


class TeapotError(SanicException):
    status_code = 418
    message = "This is a teapot but a server."


class ModuleLackException(SanicException):
    quiet = True
    extra: dict
    # TODO: extra & content => DTO object.

    @property
    def message(self):
        return ""
