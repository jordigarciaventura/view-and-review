from django.db.models import Q
from behave import *

from web.models import User

use_step_matcher("parse")

@when('I register a new user')
def step_impl(context):
    for row in context.table:
        context.browser.visit(context.get_url('register'))
        assert context.browser.url == context.get_url('register')
        form = context.browser.find_by_id('register-form')
        for heading in row.headings:
            context.browser.fill(heading, row[heading])
        form.find_by_value('register').click()
    assert User.objects.count() == 1
        
@then(u'I\'m viewing the main page')
def step_impl(context):
    assert context.get_url('index') in context.browser.url # Check if it is substring due to deep-linking
