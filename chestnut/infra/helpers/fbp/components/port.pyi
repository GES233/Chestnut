from typing import overload, Any, Callable

class Port:
    name: str
    t: type
    data: Any
    annotation: str
    value: property
    """
    @overload
    def __init__(self, name: str, type_: type | object) -> None: ...
    @overload
    def __init__(
        self, name: str, type_: type | object, role: str | None = None
    ) -> None: ...
    """
    def __init__(
        self,
        name: str,
        *constraints,
        type_: type | object,
        role: str | None,
        default: Any | None = None
    ) -> None: ...
    """
    @overload
    def __call__(self) -> Any: ...
    @overload
    def __call__(self, *value) -> Any: ...
    """
    def __call__(self, *args: Any, **kwds: Any) -> Any: ...
