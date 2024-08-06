from django.db import models
import uuid
from django.conf import settings


class Movie(models.Model):

    # Defining genre choices as a list of tuples
    # Each tuple contains:
    # - The first element: the actual value to be stored in the database
    # - The second element: the human-readable name shown in forms and admin interface
    GENRE_CHOICES = [
        ('action', 'Action'),               # ('value', 'display name')
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy')
    ]

    # Fields for the Movie model
    uu_id = models.UUIDField(default=uuid.uuid4)  # Generates a unique identifier for each movie using UUID.
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)  # The genre field can only take one of the values defined in GENRE_CHOICES
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movie_images/')
    image_cover = models.ImageField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')
    movie_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    
