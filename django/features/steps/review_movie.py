from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from behave import *

from web.models import Rating, Review, Movie, User

use_step_matcher("parse")

@given(u'A review of movie "{tmdb_id}" from user "{username}" exists')
def step_impl(context, tmdb_id, username):
    movie = Movie.objects.get(pk=tmdb_id)
    user = User.objects.get(username=username)
    related_rating = Rating.objects.get(user=user, movie=movie)
    for row in context.table:
        review = Review()
        for heading in row:
            setattr(review, heading, row[heading])
        review.save()
    related_rating.review = review
    related_rating.save()
    related_rating.refresh_from_db(fields=['review'])
    assert Review.objects.count() > 0
    assert related_rating.review is not None

@then(u'I can make a review')
def step_impl(context):
    form = context.browser.find_element(By.ID, 'review-form')
    for row in context.table:
        for heading in row.headings:
            input = form.find_element(By.ID, heading)
            input.send_keys(row[heading])
            assert input.get_attribute('value') == row[heading], heading + ": " + input.get_attribute('value')
        submit_button = form.find_element(By.ID, 'submit-button')
        ActionChains(context.browser).move_to_element(submit_button).click(submit_button).perform()
    
    assert Review.objects.count() > 0, "There should be a review"
        
        
@then(u'I can edit my review')
def step_impl(context):
    form = context.browser.find_element(By.ID, 'review-form')
    
    submit_button = form.find_element(By.ID, 'submit-button')
    ActionChains(context.browser).move_to_element(submit_button).perform()
    
    # Check that form is prefilled
    assert form.find_element(By.ID, 'id_title').text is not None
    assert form.find_element(By.ID, 'id_content').text is not None