from time import sleep

from behave import step

from tests.ui.config.config import get_config
from tests.ui.page_objects.home_page import HomePage


@step("I navigate to the home page")
def navigate_to_home(context):
    context.browser.get(get_config().get("webapp", "url"))


@step("I navigate to the dimensions data page")
def navigate_to_dimensions_data(context):
    context.browser.get(get_config().get("webapp", "dimensions"))


@step("I navigate to the facts data page")
def navigate_to_dimensions_data(context):
    context.browser.get(get_config().get("webapp", "facts"))


@step("I navigate to reset password page")
def navigate_to_dimensions_data(context):
    context.browser.get(get_config().get("webapp", "reset_password"))


@step("I click in integration errors button")
def navigate_to_integration_errors(context):
    context.browser.find_element(*HomePage.integration_errors_btn_locator).click()


@step("I click on campaign notifications button")
def navigate_to_integration_errors(context):
    context.browser.find_element(*HomePage.campaign_notifications_btn_locator).click()
