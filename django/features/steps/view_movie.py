from behave import *

from web.models import Movie
from web.api import movie

use_step_matcher("parse")

@given(u'A movie "{tmdb_id}" exists')
def step_impl(context, tmdb_id):
    Movie.objects.create(tmdb_id=tmdb_id)


@when(u'I view a movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    context.browser.get(context.get_url('movie', tmdb_id))


@then(u'I\'m viewing the movie page for movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    assert context.browser.current_url == context.get_url('movie', tmdb_id)
