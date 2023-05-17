from django.db.models import Q
from behave import *

from web.models import User
from web.api import movie

use_step_matcher("parse")

@when(u'I view a movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    context.browser.visit(context.get_url('movie', tmdb_id))
    movie_info = movie(tmdb_id)
    assert context.browser.find_by_id('title').text == movie_info['title'] 


@then(u'I\'m viewing the movie page for movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    assert context.browser.url == context.get_url('movie', tmdb_id)
