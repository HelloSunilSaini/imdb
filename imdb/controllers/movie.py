
from imdb.utils.custom_error import CustomError
from imdb.controllers.user import get_session_user
from imdb.dao.movie import create_movie, update_movie, get_movie_by_id, \
    delete_movie_by_id, get_movie_obj_by_genre, get_movies_by_search

def add_movie(movie_data):
    create_movie(movie_data, get_session_user())
    
def update_movie_data(movie_data):
    update_movie(movie_data, get_session_user())
    
def remove_movie(movie_id):
    if not get_movie_by_id(movie_id):
        raise  CustomError(404, "Movie Not Found")
    delete_movie_by_id(movie_id)

def get_movie_json_by_id(movie_id):
    try:
        movie = get_movie_by_id(movie_id)
        if movie:
            return movie.as_json()
        else:
            raise CustomError(404, "Movie Not Found")
    except:
        raise CustomError(500, "Internal Server Error")

def get_movie_json_list_by_movies(movies):
    result = list()
    for movie in movies:
        result.append(movie.as_json())
    return result
    
def get_movies_by_genre(genre, limit=20, offset=0):
    movies = get_movie_obj_by_genre(genre,limit,offset)        
    return get_movie_json_list_by_movies(movies)

def get_movies_by_search_term(search_term, limit=20, offset=0):
    movies = get_movies_by_search(search_term, limit, offset)
    return get_movie_json_list_by_movies(movies)