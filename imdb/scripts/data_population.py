import json
import django
django.setup()
from imdb.dao.movie import create_movie

if __name__=="__main__":
    with open('imdb_test_data.json') as f:
        data = json.load(f)
    for movie in data:
        create_movie(movie, None)
