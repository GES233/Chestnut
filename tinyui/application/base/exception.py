class AppExcBase(Exception):
    msg = ""

    def __str__(self) -> str:
        return self.msg
