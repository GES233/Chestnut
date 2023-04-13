from typing import Any, Dict


class PageConfig:
    """Config for a Page(usually for the requests to a HTML file)."""

    title: str | None
    role: str | None
    name_as_role: bool
    header_items: Dict[str, Any]
    __dict__: Dict[str, Any]

    __slots__ = ("name_as_role", "__dict__", "title", "role", "header_items")

    def __init__(self, **kwargs) -> None:
        self.title = None
        self.role = None
        self.name_as_role = False
        self.header_items = {}
        for item in kwargs:
            self.__setattr__(item, kwargs[item])

    def __getattr__(self, __name: str) -> Any:
        # Name related.
        if __name == "name":
            return self.title if self.name_as_role else self.role
        # Slots first.
        if __name in self.__slots__:
            return super().__getattribute__(__name)
        # Second dict.
        elif __name in self.__dict__:
            return (
                self.__dict__[__name]
                if __name.islower()
                else self.__dict__[__name.lower()]
            )
        else:
            raise AttributeError(f"Config has no attribute '{__name}'")

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "name":
            # If set attribute name => self.name_as_role
            if self.name_as_role:
                self.role = __value
                self.title = None
            else:
                self.title = __value
                self.role = None
        if __name in self.__slots__:
            # Set self.name_as_role.
            if __name == "title":
                self.name_as_role = False
            elif __name == "role":
                self.name_as_role = True
            super().__setattr__(__name, __value)
        else:
            self.__dict__[__name.lower()] = __value

    def __delattr__(self, __name: str) -> None:
        if __name in self.__slots__:
            super().__delattr__(__name)
        elif __name in self.__dict__:
            del self.__dict__[__name]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {self.title if not self.name_as_role else self.role}>"

    def load(self, config_dict: dict) -> None:
        for item in config_dict:
            self.__setattr__(item, config_dict[item])

    def load_items(self, **items) -> None:
        for item in items:
            self.__setattr__(item, items[item])

    @staticmethod
    def addtitle(**kwargs) -> dict:
        title = kwargs.get("title")
        role = kwargs.get("role")

        if title and role:
            raise AttributeError("Only title OR role allowed in PageConfig, not both.")
        elif not (title or role):
            raise AttributeError("title or role required.")

        if title:
            del kwargs["title"]
            return dict(
                title=title,
                name_as_role=False,
                **kwargs,
            )
        else:
            del kwargs["role"]
            return dict(
                role=role,
                name_as_role=True,
                **kwargs,
            )

    @classmethod
    def generate(cls, **kwargs) -> "PageConfig":
        return PageConfig(**PageConfig.addtitle(**kwargs))


class JSONConfig:
    """Reserved."""

    __slots__ = "__dict__"

    def __init__(self, **content) -> None:
        self.__dict__ = content or {}

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__slots__:
            return super().__getattribute__(__name)
        elif __name in self.__dict__ and __name.islower():
            return self.__dict__[__name]
        # elif __name.isupper() and (self.name.upper() + "_") in __name:
        # return self.__dict__[__name.lstrip(self.name.upper()).lstrip("_").lower()]
        else:
            raise AttributeError(f"Config has no attribute '{__name}'")

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.__slots__:
            super().__setattr__(__name, __value)
        elif __name.islower():
            self.__dict__[__name] = __value
        # elif __name.isupper() and (self.name.upper() + "_") in __name:
        # self.values[__name.lstrip(self.name.upper()).lstrip("_").lower()] = __value
        else:
            raise KeyError("Invalid key.")

    def __delattr__(self, __name: str) -> None:
        if __name in self.__dict__:
            del self.__dict__[__name]
        # elif __name.isupper() and (self.name.upper() + "_") in __name:
        # del self.values[__name.lstrip(self.name.upper()).lstrip("_").lower()]
