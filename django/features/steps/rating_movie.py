from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
    context.browser.get(context.get_url('movie', tmdb_id))
    star = context.browser.find_element(By.ID, 'label-' + score)
    ActionChains(context.browser).move_to_element(star).click(star).pause(1).perform()
    stored_score = Rating.objects.first().score 
    assert str(stored_score) == score, "Saved score [" + str(stored_score) + "] instead of " + score
    
@when(u'I can delete a rating of the movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    context.browser.get(context.get_url('movie', tmdb_id))
    delete_button = context.browser.find_element(By.ID, 'delete-rating')
    ActionChains(context.browser).move_to_element(delete_button).click(delete_button).pause(1).perform()
    
@when(u'I can edit a rating with new score "{score}" of the movie "{tmdb_id}"')
def step_impl(context, score, tmdb_id):
    context.browser.get(context.get_url('movie', tmdb_id))
    star = context.browser.find_element(By.ID, 'label-' + score)
    ActionChains(context.browser).move_to_element(star).click(star).pause(1).perform()
    stored_score = Rating.objects.first().score 
    assert str(stored_score) == score, "Saved score [" + str(stored_score) + "] instead of " + score
    
@then(u'There is "{number:d}" ratings')
def step_impl(context, number):
    assert Rating.objects.count() == number, "There are [" + Rating.objects.count() + "] ratings instead of " + number