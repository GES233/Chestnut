from ...helpers.config import DepsConfig


database_dev = DepsConfig(
    "database",
    True,
    {
        "uri": "sqlite+aiosqlite:///chestnut_dev.db",
        "encoding": "utf-8",
        "echo": True,
    },
)


database_test = DepsConfig(
    "database",
    True,
    {
        "uri": "sqlite+aiosqlite://",  # Using memory when unit test.
        "encoding": "utf-8",
        "echo": True,
    },
)


database_prod = DepsConfig(
    "database",
    True,
    {
        "uri": "sqlite+aiosqlite:///chestnut_local.db",
        "encoding": "utf-8",
        "echo": False,
    },
)
