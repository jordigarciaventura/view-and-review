from django.db.models import Q
from behave import *

from web.models import Movie, Rating, User

use_step_matcher("parse")

@given(u'Exists a rating for movie "{tmdb_id}" from user "{username}" with score "{score}"')
def step_impl(context, tmdb_id, username, score):
    movie = Movie.objects.get(pk=tmdb_id)
    user = User.objects.get(username=username)
    assert user.username == username
    Rating(user=user, movie=movie, score=int(score)).save()
    assert Rating.objects.count() == 1, Rating.objects.count()
    
@when(u'I make a rating of score "{score}" of the movie "{tmdb_id}"')
def step_impl(context, score, tmdb_id):
    raise Exception("TODO")
    context.browser.get(context.get_url('movie', tmdb_id))