from imdb.utils.resource import Resource,ok_response
from imdb.utils.logger import get_root_logger

logger = get_root_logger()


class Ping(Resource):
    def get(self):
        logger.info("Received Ping request")
        return ok_response({})
    
    get.authenticated = False
