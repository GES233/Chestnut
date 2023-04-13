from enum import Enum


class ItemType(int, Enum):
    PythonObject = 1
    PythonModule = 2
    Command = 3
    Program = 4
    File = 5

    def hasnativever(self) -> bool:
        return (
            self.value == ItemType.PythonModule
            or self.value == ItemType.Program
        )
    
    def caninvoke(self) -> bool:
        return (
            self.value == ItemType.PythonModule
            or self.value == ItemType.PythonObject
            # or self.value == ItemType.Command
        )
    
    def servicerequired(self) -> bool:
        raise NotImplementedError
