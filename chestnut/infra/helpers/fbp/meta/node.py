import inspect as isp
import functools as fnt
from typing import Tuple, Dict, Callable, Any

from .base import FlowMeta
from .port import Role as PortRole, PortMeta, key_conf as port_key_conf
from .. import exception as exc


key_conf: Dict[str, str] = {
    "abstract": "__abstract__",
    "entry": "__entry__",  # IS NOT A METHOD.
    "mapper": "__mappings__",
}


def _func_entry(__bases: Tuple[type], __namespace: Dict[str, Any]) -> str:
    """Fetch entry attribute of class."""

    # if parent class have __entry__
    if __bases:
        for base in __bases:
            for parent in base.__mro__[:-1]:
                if parent.__dict__.get(key_conf["entry"]):
                    entry: str = parent.__dict__[key_conf["entry"]]
                    return entry

    # if has not __entry__
    entry: str = __namespace.get(
        key_conf["entry"], "function"  # `function` is not a keyword in Python
    )
    return entry


def _func_cover(__bases: Tuple[type], __namespace: Dict[str, Any]) -> Dict[str, Any]:
    """Let `Ports` into mapper."""

    _mappings = dict()

    # Heritage,
    if __bases:
        for base in __bases:
            for parent in base.__mro__[:-1]:
                if hasattr(parent, key_conf["mapper"]):
                    _mappings.update(parent.__dict__[key_conf["mapper"]])

    # Update and
    for k, v in __namespace.items():
        # if isinstance(v, Port):
        if isinstance(v.__class__, PortMeta):
            _mappings[k] = v

    # Delete
    for k in _mappings.keys():
        if k in __namespace:
            __namespace.pop(k)

    return _mappings


# `__mappings__` => `__mappings_bla__`
role_convert: Callable[[str], str] = (
    lambda k: "__" + key_conf["mapper"].strip("_") + "_" + k + "__"
)


def _func_seperate(_mappings_dict: Dict[str, Any], role: Tuple[str]) -> Dict[str, Dict]:
    """Add mappers with role."""

    _mappings_with_role = {role_convert(k): dict() for k in role}

    for port_name in _mappings_dict:
        port = _mappings_dict[port_name]

        # Check role.
        ...

        # _mappings_with_role[role_convert(_port_role)][port_name] = port

    return _mappings_with_role


# TODO: Learning args of Python language.
def _func_analysefunc(func: Callable[..., Any]) -> Dict[str, Dict]:
    """Only for 'input' and 'output' of function."""

    _args_dict = {"input": dict(), "output": dict()}

    _args = isp.getfullargspec(func)

    if _args.annotations:
        _annotations = _args.annotations.copy()
        _args_dict["output"] = {"return": _annotations.pop("return")}
        _args_dict["input"] = _annotations
    else:
        # Any -> Any
        # Replace type in port.
        # If not defined port => raise error.
        _args_dict["input"] = {arg: Any for arg in _args.args}
        _args_dict["output"] = {"return": Any}

    if _args.defaults:
        # If input is not default value.
        ...

    if _args.varargs:
        _args_dict["args"] = dict()
        # TODO: bind param.
    if _args.varkw:
        _args_dict["kwargs"] = dict()

    return _args_dict


def _method_setattr():
    """Implement the `__setattr__` of class."""

    # If role is not output:
    # - put.
    # else:
    # - raise Exception.
    def __setattr__(self: object, __name: str, __value: Any) -> None:
        if __name in self.__slots__ or key_conf.values():  # type: ignore
            return self.__setattr__(__name, __value)
        elif __name in self.__getattribute__(key_conf["mapper"]):
            target_port = self.__getattribute__(key_conf["mapper"])[__name]
            if not isinstance(target_port.__class__, PortMeta):
                raise TypeError(
                    f"The object in mapper {__name.__class__} is not a Port object."
                )
            else:
                # TODO: Check role.
                raise NotImplementedError
        raise NotImplementedError

    return __setattr__


def _method_getattr():
    """Implement the `__getattr__` of class."""

    # Return value via mappers.
    def __getattr__(self: object, __name: str) -> Any:
        if __name in key_conf.values():
            return self.__getattribute__(__name)
        elif __name in self.__getattribute__(key_conf["mapper"]):
            target_port = self.__getattribute__(key_conf["mapper"])[__name]
            if not isinstance(target_port.__class__, PortMeta):
                raise TypeError(
                    f"The object in mapper {__name.__class__} is not a Port object."
                )
            else:
                return getattr(target_port, port_key_conf["property"])
        raise NotImplementedError

    return __getattr__


def _method_run():
    """Implement the run method of class."""

    # TODO: Add coroutine.
    def run(self, *args, **kwds):
        func: Callable[..., Any] = getattr(self, key_conf["entry"])
        result = func(*args, **kwds)
        return result

    return run


def _method_init():
    """Implement the `__init__` of class."""

    def __init__(self):
        ...

    raise NotImplementedError


def _method_call():
    """Implement the `__call__` of class."""

    def __call__(self, *args, **kwds):
        # TODO: Padding.
        return self

    return __call__


def _method_rrshift():
    """Implement the `__rrshift__` of class."""

    def __rrshift__(self): ...

    return __rrshift__


class NodeMeta(FlowMeta):
    def __new__(
        cls, __name: str, __bases: Tuple[type, ...], __namespace: Dict[str, Any], **kwds
    ):
        # - Add name to attr: `camel_to_snake(name)`.
        __namespace["name"] = __name

        # - Check configuration.
        #   If you want to definate freely, explicitly configurate it.
        #
        #   => __abstract__
        #   => __entry__
        #   => ...
        __namespace["abstract"] = __namespace.get(
            key_conf["abstract"], False
        )  # Default: False
        abstract: bool = __namespace["abstract"]
        entry: str = _func_entry(
            __bases, __namespace
        )  # __namespace.get(key_conf["entry"], "function")

        # - Create mapper(port -> data).
        _mappings_dict = _func_cover(__bases, __namespace)
        __namespace[key_conf["mapper"]] = _mappings_dict

        if not abstract and __bases:  # avoid class Bla(metaclass=NodeMeta): ...
            # If not have entrypoint.
            if entry not in __namespace:
                raise exc.LackRuntimeFunctionError
            else:
                # Extract function.
                entry_function: Callable[..., Any] = __namespace.pop(entry)

            # Analyse function.
            ...

            # - Check ports.
            #   - sperate by role,
            _mappings_with_role = _func_seperate(
                _mappings_dict, tuple(r.value for r in PortRole)
            )
            #   - and upgrade.
            # __namespace.pop(key_conf["mapper"])
            __namespace.update(_mappings_with_role)

            #   - Is it valid?
            ...

            # - Bind core function to `Node`.
            __namespace[key_conf["entry"]] = staticmethod(entry_function)
            ...

            # - Update `__doc__`.
            if entry_function.__doc__:
                __namespace["__doc__"] = entry_function.__doc__

        class_ = super().__new__(cls, __name, __bases, __namespace, **kwds)

        if not abstract and __bases:
            # - Bind specific method to class.
            setattr(class_, "run", _method_run())
            #   - `__init__()`
            #   - `__call__()`
            #   - `__rrshift__()`
            # setattr(class_, "__init__", ...)
            setattr(class_, "__call__", _method_call)
            # setattr(class_, "__repr__", ...)

        return class_
