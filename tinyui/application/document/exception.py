from ..base.exception import AppExcBase


class DomainModelTypeInvalid(AppExcBase, TypeError):
    ...


class DocumentFormatInvalid(AppExcBase, TypeError):
    msg = "Invalid type {} not in {}."


class ContentNotFound(AppExcBase):
    ...


class DocumentNotFound(ContentNotFound):
    ...


class AssetsNotFound(ContentNotFound):
    ...
