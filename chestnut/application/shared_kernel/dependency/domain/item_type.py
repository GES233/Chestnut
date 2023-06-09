from enum import Enum

from ....core.domain.value_object import ValueObject as VOMixin


class ItemType(VOMixin, int, Enum):
    PythonObject = 1
    PythonModule = 2
    Command = 3
    Program = 4
    File = 5
    Device = 6
    "Such as GPU, etc."

    @classmethod
    def fromvalue(cls, value: int | str) -> "ItemType":
        if isinstance(value, int):
            return cls(value)
        # elif isinstance(value, str):
        #     raise NotImplementedError
        else:
            raise NotImplementedError

    def hasnativever(self) -> bool:
        """Has native version."""

        return self.value == ItemType.PythonModule or self.value == ItemType.Program

    def caninvoke(self) -> bool:
        return (
            self.value == ItemType.PythonModule
            or self.value == ItemType.PythonObject
            # or self.value == ItemType.Command
        )

    def servicerequired(self) -> bool:
        raise NotImplementedError


class ItemIdentity(VOMixin, tuple, Enum):
    """Check the item is valid or not."""

    @classmethod
    def fromvalue(cls, value) -> "ItemIdentity":
        raise NotImplementedError
