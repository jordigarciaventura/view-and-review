from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.utils.text import slugify

# Create your models here.

class Rating(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    review = models.CharField(max_length=512, blank=True)
    review_title = models.CharField(max_length=64, blank=True)
    film = models.PositiveIntegerField(null=False, blank=False) #tmdb film id
    score = models.PositiveIntegerField(default=0, choices=RATING_CHOICES)

    def __str__(self) -> str:
        return str(self.film) + "-" + str(self.user) + " " + str(self.score)


"""Stores the user rating upvotes and downvotes"""
class Reputation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    value = models.BooleanField() # False == downvote, True == upvote

    def __str__(self) -> str:
        return str(self.user) + " " + str(self.rating) + ("+" if self.value else "-")
    
    
class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, primary_key=True, editable=False)
    watchlist = models.TextField(validators=[int_list_validator], max_length=40000, default="")
    favlist = models.TextField(validators=[int_list_validator], max_length=40000, default="")
    slug = models.SlugField(default="")
    
    def __str__(self) -> str:
        return str(self.user) + " - " + str(self.slug)
    
    @classmethod
    def create(cls, user) -> 'MyProfile': 
        profile = cls(user=user, slug=slugify(user))
        return profile