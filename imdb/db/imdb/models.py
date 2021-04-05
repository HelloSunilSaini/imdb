from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    """
    Genre model : model for movie Genres
    """
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    """
    Movie model : model for Movies
    """
    name = models.CharField(db_index=True, max_length=500)
    imdb_score = models.FloatField()
    popularity = models.FloatField()
    director = models.CharField(db_index=True, max_length=500)
    genre = models.ManyToManyField(Genre)
    # meta-data for creation and changes ..
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="movie_added_by")
    added_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="movie_modified_by")
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name
    
    def as_json(self):
        return dict({
            "name" : self.name,
            "99popularity" : self.popularity,
            "director" : self.director,
            "imdb_score" : self.imdb_score,
            "genre" : self.genre.all().values_list('name', flat=True)
        })