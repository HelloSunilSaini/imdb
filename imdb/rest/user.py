from imdb.utils.resource import Resource, error_response, ok_response
from imdb.utils.error_handler import ErrorHandler
from imdb.utils.logger import get_root_logger
from imdb.validators.user import validate_user_post_request
from imdb.controllers.user import create_user, user_exist_with_username, user_exist_with_email

from flask import session, request

logger = get_root_logger()


class User(Resource):
    @ErrorHandler("User POST")
    def post(self):
        logger.info("Received User Post request from : {}".format(session.get("user_id")))

        request_body = request.get_json(force=True)
        
        if not validate_user_post_request(request_body):
            return error_response(400, "Bad Request")
        
        if user_exist_with_username(request_body['username']):
            return error_response(409, message="User Alreay Exist with username")
        if user_exist_with_email(request_body['email']):
            return error_response(409, message="User Alreay Exist with email")
        
        if not create_user(request_body):
            return error_response(500, message="Internal Server Error")
        return ok_response({}, message="User Created Successfully")

            
