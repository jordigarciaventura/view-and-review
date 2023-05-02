from django.db import models
from django.contrib.auth.models import User

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
    SCORE_CHOICES = ((0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0))
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, default="")
    score = models.DecimalField(decimal_places=1, max_digits=2, choices=SCORE_CHOICES, default=(0.0, 0.0))
    review = models.CharField(max_length=512, null=True)
    
    def __str__(self) -> str:
        return str(self.user) + " " + str(self.score) 