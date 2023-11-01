from sanic import Blueprint


user_bp = Blueprint("user_plain", "/user")


# Register
from .register.view import registerpresentation, register

user_bp.add_route(registerpresentation, uri="/register", methods=["GET"])
user_bp.add_route(register, uri="/register", methods=["POST"])


# Login
from .login.view import login, loginpresentation, logout
user_bp.add_route(loginpresentation, uri="/login", methods=["GET"])
user_bp.add_route(login, uri="/login", methods=["POST"])
user_bp.add_route(logout, uri="/logout", methods=["GET", "POST"])


# User Profile.
user_info_bp = Blueprint("user_info")
from .me.view import returnuserprofile
user_info_bp.add_route(returnuserprofile, "/me", methods=["GET"])
