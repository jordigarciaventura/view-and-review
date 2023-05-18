from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from behave import *

from web.models import Review

use_step_matcher("parse")

@when(u'I can make a review of movie "{tmdb_id}"')
def step_impl(context, tmdb_id):
    context.browser.get(context.get_url('movie', tmdb_id))
    assert context.browser.find_element(By.ID, 'review-form'), "review form does not exist in current page"
    for row in context.table:
        for heading in row.headings:
            input = context.browser.find_element(By.ID, heading)
            input.send_keys(row[heading])
            assert input.get_attribute('value') == row[heading], heading + ": " + input.get_attribute('value')
        submit_button = context.browser.find_element(By.ID, 'submit-button')
        ActionChains(context.browser).move_to_element(submit_button).click(submit_button).perform()
    assert Review.objects.count() == 1, "There should be a review"
        