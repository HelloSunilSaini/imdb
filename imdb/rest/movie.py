from imdb.utils.resource import Resource, error_response, ok_response
from imdb.utils.error_handler import ErrorHandler
from imdb.utils.logger import get_root_logger
from imdb.validators.movie import validate_movie_post_request, validate_movie_put_request
from imdb.controllers.movie import add_movie, update_movie_data, remove_movie, \
    get_movie_json_by_id, get_movies_by_genre, get_movies_by_search_term

from flask import session, request

logger = get_root_logger()


class Movie(Resource):
    @ErrorHandler("Movie GET")
    def get(self, movie_id=None):
        logger.info("Received Movie Get request from : " + session.name)
        if movie_id:
            response = get_movie_json_by_id(movie_id)
            return ok_response(response)
        try:
            params = request.args.to_dict()
            limit = int(params.get('limit', 20))
            offset = int(params.get('offset', 0))
            if params.get('genre'):
                response = get_movies_by_genre(params['genre'], limit, offset)
                return ok_response(response)
            elif params.get('search_term'):
                response = get_movies_by_search_term(params['search_term'], limit, offset)
                return ok_response(response)
            else:
                return error_response(400, "Bad Request")
        except:
            return error_response(500, "Internal Server Error")
        
    get.authenticated = False
        
    @ErrorHandler("Movie POST")
    def post(self):
        logger.info("Received Movie Post request from : " + session.name)

        request_body = request.get_json(force=True)
        
        if not validate_movie_post_request(request_body):
            return error_response(400, "Bad Request")
        
        if not add_movie(request_body):
            return error_response(500, message="Internal Server Error")
        return ok_response({}, message="Movie added Successfully")

            
    @ErrorHandler("Movie PUT")
    def put(self):
        logger.info("Received Movie Put request from : " + session.name)

        request_body = request.get_json(force=True)
        
        if not validate_movie_put_request(request_body):
            return error_response(400, "Bad Request")
        
        if not update_movie_data(request_body):
            return error_response(500, message="Internal Server Error")
        return ok_response({}, message="Movie Updated Successfully")
    
    @ErrorHandler("Movie DELETE")
    def delete(self,movie_id=None):
        logger.info("Received Movie Delete request from : " + session.name)
        if not movie_id:
            return error_response(400, "Bad Request")
        remove_movie(movie_id)
        return ok_response({}, message="Movie Deleted Successfully")