from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Actor(models.Model):
    full_name = models.CharField(max_length=64)

    def __str__(self):
        return self.full_name


class Director(models.Model):
    full_name = models.CharField(max_length=64)

    def __str__(self):
        return self.full_name


class Language(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=64)
    release_date = models.DateField()
    duration = models.IntegerField()
    plot = models.CharField(max_length=512)
    photo_url = models.URLField(default="")

    directors = models.ManyToManyField(Director)
    languages = models.ManyToManyField(Language)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


class Rating(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    review = models.CharField(max_length=512, blank=True)
    review_title = models.CharField(max_length=64, blank=True)
    score = models.PositiveIntegerField(default=0, choices=RATING_CHOICES)

    def __str__(self) -> str:
        return str(self.user) + " " + str(self.score)
