from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add a ForeignKey to the User model
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='movies',on_delete=models.CASCADE)
    trailer_link = models.URLField()

    def __str__(self):
        return self.title



class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'