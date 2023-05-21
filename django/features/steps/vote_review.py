from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from behave import *

from web.models import ReviewVote

@when(u'I "{vote_type}" the first review')
def step_impl(context, vote_type):
    button = context.browser.find_element(By.CLASS_NAME, vote_type) # Will return only the first element matching !
    context.browser.execute_script("window.scrollTo({ top: arguments[0].offsetTop, behavior: 'instant' })", button)
    ActionChains(context.browser).move_to_element(button).click(button).pause(1).perform() # Pause is needed bc of slow scroll
    

@then(u'There are "{amount:d}" review votes and their value is "{value}"')
def step_impl(context, amount, value):
    vote_count = ReviewVote.objects.count() 
    assert vote_count == amount, "There were [{}] votes instead of {}".format(vote_count, amount)
    
    value = value == "True"
    assert ReviewVote.objects.filter(value=value).count() == ReviewVote.objects.count(), "There were votes not matching the given value {}".format(value)
