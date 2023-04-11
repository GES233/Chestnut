from enum import Enum
from typing import Dict, Any

from .base import FlowMeta


key_conf: Dict[str, str] = {"property": "value"}


class Role(str, Enum):
    i = "input"
    o = "output"


class PortMeta(FlowMeta):
    """PortMeta: Provide run-time type checking and automatic return of results.

    ```python
    class Port(metaclass=PortMeta):
        pass

    a = Port("name", t=typing.Union[int, str], input=True)
    ```
    """

    __instance: Dict[str, Any] = {}

    def __new__(cls, __name, __bases, __namespace, **kwds):
        # "name" must be in __namespace
        ...

        class_ = super().__new__(cls, __name, __bases, __namespace, **kwds)
        # - Bind specific method to class.
        #   - Type checking
        setattr(
            class_,
            key_conf["property"],
            property(
                fget=_fget_value(),
                fset=_fset_value(),
                fdel=_fdel_value(),
            ),
        )
        # setattr(class_, "__getattr__", ...)

        return class_

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        """Singleton with name."""

        # Add a `parse` process to extract the `name`.
        _args_dict = _func_parseportargs(args, kwds)

        if _args_dict["name"] not in cls.__instance:
            instance = super().__call__(*args, **kwds)
            # instance.__init__(*args, **kwds)
            cls.__instance[_args_dict["name"]] = instance
            return instance
        else:
            cls_type_ = cls.__instance[_args_dict["name"]].t
            new_type_ = _args_dict["t"]
            # TODO: Add classification.
            ...

            return cls.__instance[_args_dict["name"]]


def _fget_value():
    def value(self) -> Any:
        if "data" not in self.__dict__:
            return None
        if not self.data:
            return None
        if not isinstance(self.data, self.t):
            raise TypeError(f"Invalid type {type(self.data)} for {self.t}.")
        return self.data

    return value


def _fset_value():
    def value(self, value: Any):
        if not isinstance(value, self.t):
            raise TypeError(f"Invalid type {type(value)} for {self.t}.")
        self.data = value

    return value


def _fdel_value():
    def value(self):
        self.data = None

    return value


def _func_parseportargs(*args, **kwargs) -> Dict[str, Any]:
    """
    Parse arguments in Port.

    Port("name", type, role_related)
    """
    _args_dict: Dict[str, Any] = dict(
        name=None,
        t=None,
    )

    if "name" not in kwargs:
        name = args[0]
    else:
        name = kwargs["name"]
    _args_dict["name"] = name

    if "t" or "type_" not in kwargs:
        type_ = args[1]
    else:
        if kwargs.get("t") and kwargs.get("type_"):
            raise TypeError
        type_ = kwargs.get("t", kwargs.get("type_"))
    _args_dict["t"] = type_

    return _args_dict
