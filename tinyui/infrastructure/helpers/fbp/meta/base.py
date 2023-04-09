from typing import Any, Dict, Tuple


class FlowMeta(type):
    def __new__(
        cls, __name: str, __bases: Tuple[type], __namespace: Dict[str, Any], **kwds: Any
    ):
        # - Add __slots__.
        __solts__ = __namespace.keys()
        return super().__new__(cls, __name, __bases, __namespace, **kwds)
