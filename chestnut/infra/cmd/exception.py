""" `chestnut.infra.cmd.exception`

    Wrapper of exceptions in terminal.
"""
from typing import Any, Dict


class TerminalExecption(Exception):
    """Generic error in tty."""

    # quite: bool
    message: str
    detail: Dict[str, Any] | None
    detail_secret: Dict[str, Any] | None

    def __init__(
        self,
        message: str | None,
        *,
        # quite: bool = False,
        detail: Dict | None = None,
        detail_secret: Dict | None = None,
    ) -> None:
        super().__init__(message)

        # self.quite = quite or False
        self.detail = detail
        self.detail_secret = detail_secret


class ModuleLackError(TerminalExecption):
    ...
