from ..core.exception import AppExcBase


class CommonUser(AppExcBase):
    message = "Have a user with common email in the database."
    how_to = "If that's your email, you can find the account with it, or use a new email to sign up."
    extra_context = dict(conflict_email="")


class TokenInvalid(AppExcBase):
    ...


class TokenExpire(TokenInvalid):
    ...
