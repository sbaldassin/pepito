from time import sleep

from behave import step

from tests.ui.config.config import get_config
from tests.ui.page_objects.home_page import HomePage


@step("I complete the sign in form")
def complete_login_form(context):
    username = get_config().get("user", "username")
    password = get_config().get("user", "password")

    context.browser.find_element(*HomePage.username_field_locator).send_keys(username)
    context.browser.find_element(*HomePage.password_field_locator).send_keys(password)


@step("I am able to login")
def assert_login(context):
    login_form = context.browser.find_element(*HomePage.login_form_locator)
    login_form.find_element(*HomePage.login_btn_locator).click()

    loged_in_name = context.browser.find_element(*HomePage.logged_in_name_locator).text
    assert loged_in_name == get_config().get("user", "username")