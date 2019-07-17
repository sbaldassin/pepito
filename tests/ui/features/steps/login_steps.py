from time import sleep

from behave import step

from tests.ui.config.config import get_config
from tests.config.config import get_config as _get_config
from tests.ui.page_objects.home_page import HomePage
from tests.ui.page_objects.reset_password_page import ResetPasswordPage
from tests.utils.getters import get_until_not_empty


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


@step("I reset the password")
def reset_password(context):
    username = get_config().get("user", "username")
    url = "http://{}/emails?recipient={}".format(_get_config().get("test_framework", "db"), username)
    context.emails_count = len(get_until_not_empty(url))
    context.browser.find_element(*ResetPasswordPage.username_field_locator).send_keys(username)
    context.browser.find_element(*ResetPasswordPage.reset_pass_btn_locator).click()


@step("I get an reset password email")
def assert_reset_password(context):
    sleep(3)
    username = get_config().get("user", "username")
    url = "http://{}/emails?recipient={}".format(_get_config().get("test_framework", "db"), username)
    emails_count = len(get_until_not_empty(url))

    assert  context.emails_count + 1 == emails_count