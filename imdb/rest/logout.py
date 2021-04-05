from imdb.controllers.user import logout_user, get_session_user
from imdb.utils.error_handler import ErrorHandler
from imdb.utils.resource import Resource, ok_response, error_response
from imdb.utils.logger import get_root_logger

logger = get_root_logger()


class Logout(Resource):
    @ErrorHandler("Logout Post")
    def post(self):
        try:
            get_session_user()
        except:
            return error_response(400, "logout called for an invalid session")
        logout_user()
        return ok_response({},message="logout successfully")
