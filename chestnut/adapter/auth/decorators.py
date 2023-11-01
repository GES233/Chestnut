from functools import wraps

from .service.session import checksession


def requiredauth():
    def decorator(f):
        wraps(checksession)
