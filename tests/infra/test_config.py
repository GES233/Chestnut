import pytest

from pathlib import Path

from tinyui.infrastructure.helpers.config import AppConfig, DepsConfig, PageConfig
from tinyui.infrastructure.helpers.config.inst import (
    setinstance,
    loadappconfig,
    loaddepsconfig,
    createdepsconfig,
    createappconfig,
)
from tinyui.infrastructure.helpers.path import INSTANCE_PATH

TEST_PATH = Path(INSTANCE_PATH / "test")


class TestConfig:
    def test_app_config(self) -> None:
        # Initialize firstly.
        app_config = AppConfig("Config", "Bla bla", True)
        assert app_config.name == "Config"

        # Update.
        app_config.use_https = True
        assert app_config.use_https == True

        # Push.
        push_dict = app_config.push(True, "")
        assert push_dict["NAME"] == "Config"

        # Load.
        load_dict = {"name": "Config1", "introduction": "只因你太没", "installed": True}
        app_config.load(load_dict)
        assert app_config.installed == True

    def test_deps_config(self) -> None:
        deps_config = DepsConfig.create("Test", False)
        assert deps_config.values == {}

        # Enable firstly.
        deps_config.enable = True
        deps_config.values = {"a": 1, "b": 2}
        assert deps_config.a == 1

        # If `only_values` is False: return a fake `__dict__`.
        lower_dict = deps_config.push(False)
        assert lower_dict["values"]["a"] == 1
        upper_dict = deps_config.push(True)
        assert upper_dict["TEST_B"] == 2

        # If you not want enable it mannually, you can use `DepsConfig.load()` instead.
        deps_config.load(False, {})  # Clear the values.
        assert deps_config.values == {}
        deps_config.load(True, {"dingzhen": True})  # MUST lower or upper with prefix.

        deps_config.update_items(cxk="Chicken")
        assert deps_config.cxk == "Chicken"

        deps_config.update_items(TEST_GEENE="只因")
        assert deps_config.geene == "只因"

        deps_config.update_items(sqlalchemy_uri="sqlite:...")
        assert deps_config.push(True)["TEST_SQLALCHEMY_URI"] == "sqlite:..."

    def test_page_config(self) -> None:
        title_config = PageConfig.generate(title="Geene")
        role_config = PageConfig.generate(role="Video")

        assert title_config.name_as_role == False
        assert role_config.name_as_role == True

        # The function of PageConfig still simple.
        assert title_config.title == "Geene"
        assert role_config.role == "Video"


multi_line_content = """迎面走来的你让我如此蠢蠢欲动
这种感觉我从未有 Cause I got a crush on you, who you
你是我的，我是你的谁
再多一眼看一眼就会爆炸
再近一点靠近点快被融化
想要把你占为己有baby bae
不管走到哪里都会想起的人是you you"""

path = Path(__file__)


class TestConfigInstance:
    def test_toml_instance(self) -> None:
        # Initialize first
        if not INSTANCE_PATH.exists():
            INSTANCE_PATH.mkdir()
        if not TEST_PATH.exists():
            TEST_PATH.mkdir()

        # Store.
        config_1 = DepsConfig(
            "one", True, {"item1": 1, "item2": multi_line_content, "item3": path}
        )
        config_2 = DepsConfig("two", True, {"item1": "q", "item2": "r", "item3": "s"})
        app_config = AppConfig("Name", "Bla bla...", True)
        app_config.description = multi_line_content
        app_config.lang = "en"

        # renderer = createdepsconfig([config_1])
        # assert r"\\" in renderer

        setinstance(
            Path(TEST_PATH / "test_1.toml"),
            "\n\n".join(
                [createappconfig(app_config), createdepsconfig([config_1, config_2])]
            ),
        )

        # Load.
        loaded_app_config = loadappconfig(Path(TEST_PATH / "test_1.toml"))
        loaded_deps_config = loaddepsconfig(Path(TEST_PATH / "test_1.toml"))

        app_config_new = AppConfig("", "", False)
        app_config_new.load(loaded_app_config)
        deps_config_new = DepsConfig("one")
        deps_config_new.load_from_toml(loaded_deps_config["one"])

        assert app_config_new.name == "Name"
        assert ("只因" not in deps_config_new.item2) and ("you" in deps_config_new.item2)
        assert deps_config_new.ONE_ITEM1 == 1


class TestPrerequisiteConfig:
    def test_config(self) -> None:
        pass
