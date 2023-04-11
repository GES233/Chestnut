from typing import Any

from ..meta.port import PortMeta


class Port(metaclass=PortMeta):
    """Provide `Port`.

    A container with dynamic type-checking.
    """

    name: str
    t: type
    data: Any
    annotation: str
    value: property

    def __init__(
        self,
        name: str,
        *constraint,
        type_: type | object,
        role: str | None = None,
        default: Any | None = None
    ) -> None:
        self.name = name

        if not isinstance(type_, type):
            type_ = type(type_)

        self.t = type_

        if default:
            self.data = default
        else:
            self.data = None

        if constraint and role:
            raise AttributeError
        if not role:
            # Analyse role.
            ...


def toport(name: str, __obj: Any) -> Port:
    return Port(name, type_=type(__obj), default=__obj)
