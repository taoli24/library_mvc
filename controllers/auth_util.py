from flask_jwt_extended import get_jwt_identity
from flask import abort


def librarian_only(func):
    def wrapper(*args, **kwargs):
        if "lib" in get_jwt_identity():
            return func(*args, **kwargs)
        else:
            return abort(403, description="You must be a librarian to perform this operation.")
    wrapper.__name__ = func.__name__
    return wrapper
