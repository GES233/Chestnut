"""To replace Sanic's native MOTD."""
import os, sys


# sanic.compat
def is_atty() -> bool:
    return bool(sys.stdout and sys.stdout.isatty())
