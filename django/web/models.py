from django.db import models

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
    
class Rating(models.Model):     
    ...
    
class Review(models.Model):
    ...
    
class Film(models.Model):
    title = models.CharField(max_length=64)
    release_date = models.DateField()
    duration = models.IntegerField()
    plot = models.CharField(max_length=512)
    
    directors = models.ManyToManyField(Director)
    languages = models.ManyToManyField(Language)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    
    def __str__(self):
        return self.title