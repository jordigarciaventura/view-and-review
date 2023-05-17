from django.db.models import Q
from behave import *

from web.models import User

use_step_matcher("parse")

@when(u'I delete my user')
def step_impl(context):
    assert User.objects.count() == 1
    context.browser.visit(context.get_url('user-settings'))
    assert context.browser.url == context.get_url('user-settings')
    context.browser.find_by_id('delete-button').click()
    assert context.browser.url == context.get_url('user-delete')
    context.browser.find_by_value('Confirm').first.click()
    
    
@then(u'There are no users')
def step_impl(context):
    assert User.objects.count() == 0