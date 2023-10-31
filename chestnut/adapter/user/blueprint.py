from sanic import Blueprint


user_bp = Blueprint("user_plain", "/user")


# Register
from .register.blueprint import registerpresentation, register

user_bp.add_route(registerpresentation, uri="/register", methods=["GET"])
user_bp.add_route(register, uri="/register", methods=["POST"])


# Login
from .login.blueprint import login, loginpresentation, logout
user_bp.add_route(loginpresentation, uri="/login", methods=["GET"])
user_bp.add_route(login, uri="/login", methods=["POST"])
user_bp.add_route(logout, uri="/logout", methods=["GET", "POST"])


# User Profile.
...
