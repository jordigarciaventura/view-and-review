from behave import *
from selenium.webdriver.common.by import By

from web.models import User

use_step_matcher("parse")

@when(u'I delete my user')
def step_impl(context):
    assert User.objects.count() == 1
    context.browser.get(context.get_url('user-settings'))
    assert context.browser.current_url == context.get_url('user-settings')
    context.browser.find_element(By.ID, 'delete-button').click()
    assert context.browser.current_url == context.get_url('user-delete')
    context.browser.find_element(By.ID, 'confirm-button').click()
    
    
@then(u'There are no users')
def step_impl(context):
    assert User.objects.count() == 0