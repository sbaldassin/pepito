import csv
from time import sleep

import requests
from behave import step
from os.path import dirname, join, abspath

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.ui.page_objects.dimensions import DimensionsDataPage
from tests.utils.getters import get_until_not_empty


@step("I have a csv with 5 users")
def create_users_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "dimensions.csv")
    open(dimensions_file, 'w').close()
    users = [create_random_player() for _ in range(5)]
    csvData = [user.to_csv() for user in users]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.users = users


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


@step("the users are saved in the db")
def assert_users_saved(context):
    for user in context.users:
        url = "http://{}/customer_by_id?customer_id={}".format(get_config().get("test_framework", "db"), user.PlayerID)
        users = get_until_not_empty(url)
        assert  len(users) == 1
