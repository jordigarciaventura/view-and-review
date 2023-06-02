from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

use_step_matcher("parse")

@given('Exists a user "{username}" with password "{password}"')
def step_impl(context, username, password):
    from django.contrib.auth.models import User
    User.objects.create_user(username=username, email='user@example.com', password=password)
    assert User.objects.count() == 1, "There should be a user created"

@given('I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    wait = WebDriverWait(context.browser, 30)
    context.browser.get(context.get_url('/accounts/login/?next=/'))
    
    wait.until(EC.presence_of_element_located((By.ID, 'username-input'))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    wait.until(EC.presence_of_element_located((By.ID, 'login-button'))).click()
    assert context.get_url('index') in context.browser.current_url
    logged_user = wait.until(EC.presence_of_element_located((By.ID, 'username'))).text
    assert logged_user == username