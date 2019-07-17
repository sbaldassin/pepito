from behave import step

from tests.ui.config.config import get_config
from tests.ui.page_objects.home_page import HomePage
from tests.ui.page_objects.integration_errors_page import IntegrationErrorsPage


@step("I verify the total integration errors")
def verify_integration_errors(context):
    total_errors = int(context.browser.find_element(*HomePage.integration_errors_badge_locator).text)
    assert total_errors >= 0


@step("I verify the page title")
def verify_page_title(context):
    title = context.browser.find_element(*IntegrationErrorsPage.page_title_locator).text
    assert title == 'Integration errors'


@step("I click on delete all button")
def click_delete_all(context):
    context.browser.find_element(*IntegrationErrorsPage.delete_all_btn_locator).click()


@step("I click on confirm button")
def click_delete_all(context):
    context.browser.find_element(*IntegrationErrorsPage.confirm_btn_locator).click()


@step("I verify that there are no messages left")
def click_delete_all(context):
    msg = context.browser.find_element(*IntegrationErrorsPage.no_errors_label_locator).text
    assert msg == 'NO ERRORS DETECTED'
