from typing import Any, Dict, Callable


class AppExcBase(Exception):
    """Base exception type in Chestnut."""

    message: str = ""
    how_to: str = ""
    extra_context: Dict[str, Any] = {}

    def __init__(
        self,
        message: str | bytes | None = None,
        *,
        how_to: str | None = None,
        hook: Callable[[str, dict], str] = lambda x, _: x,
        **context,
    ) -> None:
        self.how_to = hook(
            how_to or getattr(self.__class__, "how_to", self.how_to), context
        )
        super().__init__(hook(str(message) or self.message, context))
        self.extra_context = context or {}

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return super().__repr__()
