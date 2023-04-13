import sys


def snake_toCamel(snake: str) -> str:
    return "".join(x.capitalize() or "_" for x in snake.split("_"))


def CamelTo_snake(Camel: str) -> str:
    res = [Camel[0].lower()]
    for c in Camel[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)

    return "".join(res)


# sanic.compat
def is_atty() -> bool:
    return bool(sys.stdout and sys.stdout.isatty())
