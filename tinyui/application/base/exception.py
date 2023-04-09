# Will replace with i18n wrapper.
_ = lambda x: x


class AppExcBase(Exception):
    msg = ""

    def __str__(self) -> str:
        return _(self.msg)
