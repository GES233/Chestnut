from sanic import Sanic, Blueprint


api = Blueprint("api")


API_PREFIX = "/api"
api_bp = Blueprint.group(api, url_prefix=API_PREFIX)
