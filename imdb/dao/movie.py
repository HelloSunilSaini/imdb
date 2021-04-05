
from imdb.db.imdb.models import Movie, Genre

def get_movie_by_id(movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        return movie
    except:
        return None
    
def get_movies_by_search(search_term, limit=20, offset=0):
    try: 
        movies = Movie.object.filter(
            name__icontains=search_term, 
            director__icontains=search_term)[offset : offset+limit]
        return movies
    except:
        return []

def get_movie_obj_by_genre(genre, limit=20, offset=0):
    try:
        genre_obj = Genre.objects.get(name=genre)
        movies = genre_obj.movie_set.all()[offset : offset+limit]
        return movies
    except:
        return []


def create_movie(movie_data, user):
    try:
        movie = Movie.objects.create(
            name=movie_data['name'],
            imdb_score=movie_data['imdb_score'],
            popularity=movie_data['99popularity'],
            director=movie_data['director'],
            added_by=user
        )
        for genre in movie_data['genre']:
            genre_obj,_ = Genre.objects.get_or_create(name=genre)
            movie.genre.add(genre_obj)
        return movie
    except:
        return None

def update_movie(movie_data, user):
    try:
        movie = Movie.objects.get(id=movie_data['movie_id'])
        if movie_data.get('name'):
            movie.name = movie_data['name']
        if movie_data.get('imdb_score'):
            movie.imdb_score = movie_data['imdb_score']
        if movie_data.get('99popularity'):
            movie.popularity = movie_data['99popularity']
        if movie_data.get('director'):
            movie.director = movie_data['director']
        
        movie.modified_by = user
        movie.save()
        if movie_data.get('genre'):
            movie.genre.clear()
            for genre in movie_data['genre']:
                genre_obj,_ = Genre.objects.get_or_create(name=genre)
                movie.genre.add(genre_obj)
        return movie
    except:
        return None

def delete_movie_by_id(movie_id):
    try:
        movie = Movie.object.get(id=movie_id)
        movie.delete()
    except:
        pass