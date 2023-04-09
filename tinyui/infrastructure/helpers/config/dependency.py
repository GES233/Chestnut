from typing import Any, Dict


class DepsConfig:
    __slots__ = "name", "enable", "values"

    name: str
    enable: bool
    values: Dict[str, Any]

    def __init__(self, name: str, enable: bool = False, values: dict = {}) -> None:
        self.name = name.lower()
        self.enable = enable
        self.values = values

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__slots__:
            return super().__getattribute__(__name)
        elif __name in self.values and __name.islower():
            return self.values[__name]
        elif __name.isupper() and (self.name.upper() + "_") in __name:
            return self.values[__name.lstrip(self.name.upper()).lstrip("_").lower()]
        else:
            raise AttributeError(f"Config has no attribute '{__name}'")

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.__slots__:
            super().__setattr__(__name, __value)
        elif __name.islower():
            self.values[__name] = __value
        elif __name.isupper() and (self.name.upper() + "_") in __name:
            self.values[__name.lstrip(self.name.upper()).lstrip("_").lower()] = __value
        else:
            raise KeyError("Invalid key.")

    def __delattr__(self, __name: str) -> None:
        if __name in self.values:
            del self.values[__name]
        elif __name.isupper() and (self.name.upper() + "_") in __name:
            del self.values[__name.lstrip(self.name.upper()).lstrip("_").lower()]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {self.name}>"

    def _push_values(self) -> dict:
        """Push to application side."""

        if not self.enable:
            return {}

        cfg = {}
        for item in self.values:
            cfg[(self.name + "_" + item).upper()] = self.values[item]

        return cfg

    def _push(self) -> dict:
        """Push the content into configuration document."""

        return {
            "name": self.name,
            "enable": self.enable,
            "values": self.values if self.enable else {},
        }

    def push(self, only_values: bool) -> dict:
        if only_values:
            # with App.
            return self._push_values()
        else:
            # with Toml.
            return self._push()

    def load(self, enable: bool, config_dict: dict) -> None:
        self.enable = enable
        if not enable:
            self.values = {}
        else:
            for item in config_dict:
                self.__setattr__(item, config_dict[item])

    @staticmethod
    def _remove_enable(whole: dict) -> dict:
        # delattr(whole, "enable")
        del whole["enable"]
        return whole

    def load_from_toml(self, deps_config: dict) -> None:
        self.load(
            deps_config["enable"],
            self._remove_enable(deps_config),
        )

    def update_items(self, **items) -> None:
        if not self.enable:
            return None
        for item in items:
            if "_" not in item or item.islower() or self.name.upper() in item:
                self.__setattr__(item, items[item])
            else:
                continue

    @classmethod
    def create(cls, name: str, enable: bool, values: dict = {}) -> "DepsConfig":
        return DepsConfig(
            name=name,
            enable=enable,
            values=values,
        )
