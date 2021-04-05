from imdb.controllers.user import validate_user
from imdb.validators.login import validate_login_request
from imdb.utils.error_handler import ErrorHandler
from imdb.utils.resource import Resource, ok_response, error_response
from imdb.utils.logger import get_root_logger
from flask.globals import request

logger = get_root_logger()


class Login(Resource):
    @ErrorHandler("Login Post")
    def post(self):
        request_data = request.get_json(force=True)
        logger.info("Received login request")
        if validate_login_request(request_data):
            return error_response(400, "Bad Request")
        response = validate_user(request_data)
        if response:
            return ok_response(response)
        else:
            return error_response(403, "The username or password you entered is incorrect")

    post.authenticated = False

