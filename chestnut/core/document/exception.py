from ..base.exception import AppExcBase


class DomainModelTypeInvalid(AppExcBase, TypeError):
    ...


class DocumentFormatInvalid(AppExcBase, TypeError):
    ...


class ContentNotFound(AppExcBase):
    ...


class DocumentNotFound(ContentNotFound):
    ...


class AssetsNotFound(ContentNotFound):
    ...
