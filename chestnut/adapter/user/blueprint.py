from sanic import Blueprint


user_bp = Blueprint("user_plain", "/user")
# Import libs.
from .register.blueprint import registerpresentation, register

user_bp.add_route(registerpresentation, uri="/register", methods=["GET"])
user_bp.add_route(register, uri="/register", methods=["POST"])

