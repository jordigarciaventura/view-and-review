from behave import *
from selenium.webdriver.common.by import By


use_step_matcher("parse")

@given('Exists a user "{username}" with password "{password}"')
def step_impl(context, username, password):
    from django.contrib.auth.models import User
    User.objects.create_user(username=username, email='user@example.com', password=password)
    assert User.objects.count() == 1, "There should be a user created"

@given('I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser.get(context.get_url('/accounts/login/?next=/'))
    context.browser.find_element(By.ID, 'username').send_keys(username)
    context.browser.find_element(By.ID, 'password').send_keys(password)
    context.browser.find_element(By.ID, 'login-button').click()
    assert context.get_url('index') in context.browser.current_url
    assert context.browser.find_element(By.ID, 'username').text == username