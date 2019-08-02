import csv
from os.path import dirname, join, abspath

from time import sleep
from behave import step
from selenium import webdriver

from tests.config.config import get_config
from tests.factory.bonus_factory import create_bonus, create_bonus_fact
from tests.factory.freespin_factory import create_freespin, create_freespin_fact
from tests.factory.game_factory import create_random_game, create_casino_game_fact
from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue_fact
from tests.factory.wager_factory import create_casino_fact, create_sports_fact, create_lottery_fact
from tests.factory.withdrawal_factory import create_withdrawal_fact
from tests.ui.page_objects.dimensions import DimensionsDataPage, FactsDataPage
from tests.utils.api_utils import get_dim_game
from tests.utils.getters import get_until_not_empty

FREESPIN_SECTION = 'freespin'
CUSTOMER_SECTION = 'customer'
BONUSES_SECTION = 'bonuses'
GAMES_SECTION = 'games'


@step("I have a csv with {n} rows with {section} data with headers")
def create_freespin_with_headers_csv(context, n, section):
    n = int(n)
    dimensions_file = join(dirname(abspath(__file__)), "data", '{}_mapping.csv'.format(section))
    open(dimensions_file, 'w').close()
    if section == FREESPIN_SECTION:
        data = [create_freespin() for _ in range(n)]
        context.freespins = data

    if section == CUSTOMER_SECTION:
        data = [create_random_player() for _ in range(n)]
        context.users = data

    if section == BONUSES_SECTION:
        data = [create_bonus() for _ in range(n)]
        context.bonuses = data

    if section == GAMES_SECTION:
        data = [create_random_game() for _ in range(n)]
        context.games = data

    csv_data = [range(len(data[0].to_csv()))]
    for g in data:
        csv_data.append(g.to_csv())

    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)


@step("I click on data mapping section")
def navigate_to_data_mapping_section(context):
    context.browser.find_element(*DimensionsDataPage.data_mapping_section_locator).click()


@step("I am able to upload {section} data with mapping")
def upload_freespin_data_mapping(context, section):
    dimensions_file = join(dirname(abspath(__file__)), "data", '{}_mapping.csv'.format(section))
    if section == FREESPIN_SECTION:
        context.browser.find_element(*DimensionsDataPage.browse_freespin_map_btn_locator).send_keys(dimensions_file)

    if section == CUSTOMER_SECTION:
        context.browser.find_element(*DimensionsDataPage.browse_customer_map_btn_locator).send_keys(dimensions_file)

    if section == BONUSES_SECTION:
        context.browser.find_element(*DimensionsDataPage.browse_bonuses_map_btn_locator).send_keys(dimensions_file)

    if section == GAMES_SECTION:
        context.browser.find_element(*DimensionsDataPage.browse_games_map_btn_locator).send_keys(dimensions_file)


def find_element_and_click(context, el):
    webdriver.ActionChains(context.browser).move_to_element(el).click(el).perform()


@step("I am able to map {section} headers")
def map_freespin_headers(context, section):
    if section == FREESPIN_SECTION:
        context.browser.find_element(*DimensionsDataPage.freespin_description_btn_locator).click()
        context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[0].click()
        context.browser.find_element(*DimensionsDataPage.freespin_number_btn_locator).click()
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[1])
        context.browser.find_element(*DimensionsDataPage.freespin_map_save_btn_locator).click()

    if section == CUSTOMER_SECTION:
        context.browser.find_element(*DimensionsDataPage.customer_player_id_btn_locator).click()
        context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[0].click()
        find_element_and_click(context, context.browser.find_element(*DimensionsDataPage.customer_country_btn_locator))
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[6])

        find_element_and_click(context, context.browser.find_element(*DimensionsDataPage.customer_email_btn_locator))
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[7])
        find_element_and_click(context, context.browser.find_element(*DimensionsDataPage.customer_sign_up_btn_locator))
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[8])
        context.browser.find_element(*DimensionsDataPage.customer_map_save_btn_locator).click()

    if section == BONUSES_SECTION:
        context.browser.find_element(*DimensionsDataPage.bonuses_description_btn_locator).click()
        context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[0].click()
        context.browser.find_element(*DimensionsDataPage.bonuses_product_id_btn_locator).click()
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[1])
        context.browser.find_element(*DimensionsDataPage.bonuses_map_save_btn_locator).click()

    if section == GAMES_SECTION:
        context.browser.find_element(*DimensionsDataPage.game_name_btn_locator).click()
        context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[0].click()
        context.browser.find_element(*DimensionsDataPage.game_category_btn_locator).click()
        find_element_and_click(context, context.browser.find_elements(*DimensionsDataPage.freespin_map_headers)[1])
        context.browser.find_element(*DimensionsDataPage.game_map_save_btn_locator).click()

    assert 'Success! ' in context.browser.find_element(*DimensionsDataPage.alert_message_locator).text


@step("The dim bonuses are saved in the db")
def assert_bonuses_saved(context):
    for bonus in context.bonuses:
        url = "http://{}/bonuses?customer_id={}".format(
            get_config().get("test_framework", "db"), bonus.player_id)
        assert get_until_not_empty(url, timeout=100) != []
