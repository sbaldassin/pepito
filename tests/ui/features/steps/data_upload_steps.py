import csv

from time import sleep
from behave import step
from os.path import dirname, join, abspath

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.config.config import get_config
from tests.factory.bonus_factory import create_bonus, create_bonus_fact
from tests.factory.freespin_factory import create_freespin, create_freespin_fact
from tests.factory.game_factory import create_random_game, create_casino_game_fact
from tests.factory.player_factory import create_random_player
from tests.ui.page_objects.dimensions import DimensionsDataPage, FactsDataPage
from tests.utils.api_utils import get_dim_game
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


@step("I have a csv with 2 games")
def create_game_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "games.csv")
    open(dimensions_file, 'w').close()
    games = [create_random_game() for _ in range(2)]
    csvData = [g.to_csv() for g in games]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.games = games


@step("I am able to upload games data")
def upload_games_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "games.csv")
    context.browser.find_element(*DimensionsDataPage.browse_game_btn_locator).send_keys(dimensions_file)
    context.browser.find_element(*DimensionsDataPage.upload_game_btn_locator).click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I click on game tab")
def navigate_to_game_tab(context):
    context.browser.find_element(*DimensionsDataPage.game_tab_locator).click()


@step("the games are saved in the db")
def assert_games_saved(context):
    for game in context.games:
        response = get_dim_game(game.GameType)
        assert len(response) == 1


@step("I click on freespin tab")
def navigate_to_freespin_tab(context):
    context.browser.find_element(*DimensionsDataPage.freespin_tab_locator).click()


@step("I have a csv with freespin data")
def create_freespin_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "freespin.csv")
    open(dimensions_file, 'w').close()
    freespins = [create_freespin() for _ in range(2)]
    csvData = [g.to_csv() for g in freespins]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.freespins = freespins


@step("I am able to upload freespin data")
def upload_games_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "freespin.csv")
    context.browser.find_element(*DimensionsDataPage.browse_freespin_btn_locator).send_keys(dimensions_file)
    context.browser.find_element(*DimensionsDataPage.upload_freespin_btn_locator).click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("the freespins are saved in the db")
def assert_games_saved(context):
    for freespin in context.freespins:
        #response = get_dim_game(freespin.GameType)
        assert freespin


@step("I click on bonuses tab")
def navigate_to_bonuses_tab(context):
    context.browser.find_element(*DimensionsDataPage.bonuses_tab_locator).click()


@step("I select the {fact_type} tab")
def navigate_to_bonuses_tab(context, fact_type):
    navigation_bar = context.browser.find_element(*FactsDataPage.navigation_tabs_locator)
    options = navigation_bar.find_elements(*FactsDataPage.data_fact_type_locator)
    [option for option in options if option.text == fact_type][0].click()


@step("I have a csv with bonus data")
def create_bonus_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "bonus.csv")
    open(dimensions_file, 'w').close()
    bonuses = [create_bonus() for _ in range(2)]
    csvData = [g.to_csv() for g in bonuses]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.bonuses = bonuses


@step("I have a csv with bonus facts data")
def create_bonus_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "bonus.csv")
    open(facts_file, 'w').close()
    bonuses = [create_bonus_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in bonuses]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.bonuses = bonuses


@step("I have a csv with casino games facts data")
def create_casino_games_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "games.csv")
    open(facts_file, 'w').close()
    facts = [create_casino_game_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with free spins facts data")
def create_bonus_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "freespin.csv")
    open(facts_file, 'w').close()
    facts = [create_freespin_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with payouts facts data")
def create_bonus_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "payouts.csv")
    open(facts_file, 'w').close()
    bonuses = [create_bonus_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in bonuses]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.bonuses = bonuses


@step("I am able to upload bonus data")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "bonus.csv")
    context.browser.find_element(*DimensionsDataPage.browse_bonuses_btn_locator).send_keys(dimensions_file)
    context.browser.find_element(*DimensionsDataPage.upload_bonuses_btn_locator).click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload bonus fact data")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "bonus.csv")
    context.browser.find_element(*FactsDataPage.browse_btn_locator).send_keys(dimensions_file)
    context.browser.find_element(*FactsDataPage.upload_btn_locator).click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload free spins fact data")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "freespin.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_free_spin_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload game sessions fact data")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "games.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_game_session_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("The bonuses are saved in the db")
def assert_bonuses_saved(context):
    for bonus in context.bonuses:
        url = "http://{}/bonuses?customer_id={}".format(
            get_config().get("test_framework", "db"), bonus.player_id)
        assert get_until_not_empty(url, timeout=100) != []


@step("The free spins are saved in the db")
def assert_freespins_saved(context):
    for fact in context.facts:
        url = "http://{}/freespin_by_customer?customer_id={}".format(
            get_config().get("test_framework", "db"), fact.player_id)
        assert get_until_not_empty(url, timeout=100) != []


@step("The game session facts are saved in the db")
def assert_game_sessions_saved(context):
    for fact in context.facts:
        url = "http://{}/game?customer_id={}".format(
            get_config().get("test_framework", "db"), fact.player_id)
        assert get_until_not_empty(url, timeout=100) != []
