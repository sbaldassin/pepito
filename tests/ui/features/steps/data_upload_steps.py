from time import sleep

from behave import step
from os.path import dirname, join, abspath

from tests.ui.page_objects.dimensions import DimensionsDataPage


@step("I am able to upload dimensions data")
def upload_dimensions_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "dimensions.csv")
    context.browser.find_element(*DimensionsDataPage.browse_btn_locator).send_keys(dimensions_file)
    context.browser.find_element(*DimensionsDataPage.upload_btn_locator).click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"
