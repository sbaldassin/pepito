import csv

from time import sleep
from behave import step
from os.path import dirname, join, abspath

from tests.config.config import get_config
from tests.factory.bonus_factory import create_bonus, create_bonus_fact
from tests.factory.freespin_factory import create_freespin, create_freespin_fact
from tests.factory.game_factory import create_random_game, create_casino_game_fact
from tests.factory.payout_factory import create_payout, create_payout_fact
from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue_fact
from tests.factory.wager_factory import create_casino_fact, create_sports_fact, create_lottery_fact
from tests.factory.withdrawal_factory import create_withdrawal_fact
from tests.models.facts import BonusFact, FreeSpinFact
from tests.models.wager import WagerCasinoFact, WagerSportFact, WagerLotteryFact
from tests.ui.page_objects.dimensions import DimensionsDataPage, FactsDataPage
from tests.utils.api_utils import get_dim_freespin, get_dim_game
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
        db_user = get_until_not_empty(url)
        assert len(db_user) == 1
        assert db_user[0]['ExternalCustomerID'] == user.PlayerID
        assert db_user[0]['Email'] == user.Email
        assert db_user[0]['Name'] == user.Name
        assert db_user[0]['Surname'] == user.Surname
        assert db_user[0]['ZipCode'] == user.ZipCode
        assert db_user[0]['State'] == user.State
        assert db_user[0]['City'] == user.City
        assert db_user[0]['CountryCode'] == user.CountryCode
        assert db_user[0]['DateOfBirth'] == user.DateOfBirth
        assert db_user[0]['PhoneNumber'] == user.MobilePhone
        assert db_user[0]['LastKnownLanguage'] == user.LanguageCode
        assert db_user[0]['LastKnownTimezone'] == user.TimeZone


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
        db_game = get_dim_game(game.GameType)
        assert len(db_game) == 1
        assert db_game[0]['GameID'] > 1
        assert db_game[0]['GameCategory'] == game.GameIdentifier
        assert db_game[0]['DateCreated']
        assert db_game[0]['MerchantID']
        assert db_game[0]['GameName'] == game.GameType


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
        db_freespin = get_dim_freespin(freespin.Identifier, freespin.Value)
        assert len(db_freespin) == 1
        assert db_freespin[0]['FreeSpinID'] > 1
        assert db_freespin[0]['Name'] == freespin.Identifier
        assert db_freespin[0]['Value'] == int(freespin.Value)
        assert db_freespin[0]['DateCreated']
        assert db_freespin[0]['MerchantID']


@step("I click on bonuses tab")
def navigate_to_bonuses_tab(context):
    context.browser.find_element(*DimensionsDataPage.bonuses_tab_locator).click()


@step("I select the {fact_type} tab")
def navigate_to_bonuses_tab(context, fact_type):
    navigation_bar = context.browser.find_element(*FactsDataPage.navigation_tabs_locator)
    options = navigation_bar.find_elements(*FactsDataPage.data_fact_type_locator)
    [option for option in options if option.text == fact_type][0].click()


@step("I have a csv with deposits facts data")
def create_deposits_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "deposits.csv")
    open(dimensions_file, 'w').close()
    deposits = [create_revenue_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in deposits]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.deposits = deposits


@step("I have a csv with withdrawals facts data")
def create_deposits_csv(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "withdrawals.csv")
    open(dimensions_file, 'w').close()
    withdrawals = [create_withdrawal_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in withdrawals]
    with open(dimensions_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.withdrawals = withdrawals


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


@step("I have a csv with bonus facts data and mappings")
def create_bonus_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "bonuses_facts_mapping.csv")
    open(facts_file, 'w').close()
    bonuses = [create_bonus_fact() for _ in range(2)]
    csvData = [BonusFact.get_headers()] + [g.to_csv_with_mappings() for g in bonuses]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.bonuses = bonuses


@step("I have a csv with casino wagers facts data and mappings")
def create_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    open(facts_file, 'w').close()
    facts = [create_casino_fact() for _ in range(2)]
    csvData = [WagerCasinoFact.get_headers()] + [g.to_csv_with_mappings() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with sports wagers facts data and mappings")
def create_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    open(facts_file, 'w').close()
    facts = [create_sports_fact() for _ in range(2)]
    csvData = [WagerSportFact.get_headers()] + [g.to_csv_with_mappings() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with lottery wagers facts data and mappings")
def create_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    open(facts_file, 'w').close()
    facts = [create_lottery_fact() for _ in range(2)]
    csvData = [WagerLotteryFact.get_headers()] + [g.to_csv_with_mappings() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with free spins facts data and mappings")
def create_bonus_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "freespin_mapping.csv")
    open(facts_file, 'w').close()
    facts = [create_freespin_fact() for _ in range(2)]
    csvData = [FreeSpinFact.get_headers()] + [g.to_csv_with_mappings() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with {payout_type} payouts facts data")
def create_bonus_csv(context, payout_type):
    facts_file = join(dirname(abspath(__file__)), "data", "payouts.csv")
    open(facts_file, 'w').close()
    payouts = [create_payout_fact(payout_type) for _ in range(2)]
    csvData = [g.to_csv() for g in payouts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.payouts = payouts


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


@step("I have a csv with casino wagers facts data")
def create_casino_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers.csv")
    open(facts_file, 'w').close()
    facts = [create_casino_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with sports wagers facts data")
def create_sports_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers.csv")
    open(facts_file, 'w').close()
    facts = [create_sports_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with lottery wagers facts data")
def create_sports_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers.csv")
    open(facts_file, 'w').close()
    facts = [create_lottery_fact() for _ in range(2)]
    csvData = [g.to_csv() for g in facts]
    with open(facts_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    context.facts = facts


@step("I have a csv with parimutuel wagers facts data")
def create_sports_wagers_facts_csv(context):
    facts_file = join(dirname(abspath(__file__)), "data", "wagers.csv")
    open(facts_file, 'w').close()
    facts = [create_lottery_fact() for _ in range(2)]
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


@step("I select the data mapping section")
def select_data_mapping(context):
    sleep(1)
    tabs = context.browser.find_elements(*FactsDataPage.data_mapping_locator)
    [t for t in tabs if t.is_displayed()][0].click()


@step("I select the upload bonuses data section")
def select_bonuses_data_mapping(context):
    context.browser.find_element(*FactsDataPage.upload_bonuses_data_section_locator).click()


@step("I select the upload wagers casino data section")
def select_bonuses_data_mapping(context):
    context.browser.find_element(*FactsDataPage.upload_casino_wagers_data_section_locator).click()


@step("I select the upload wagers lottery data section")
def select_bonuses_data_mapping(context):
    context.browser.find_element(*FactsDataPage.upload_lottery_wagers_data_section_locator).click()


@step("I select the upload wagers sports data section")
def select_wager_sports_data_mapping(context):
    context.browser.find_element(*FactsDataPage.upload_sport_wagers_data_section_locator).click()


@step("I select the upload freespin data section")
def select_free_spin_data_mapping(context):
    context.browser.find_element(*FactsDataPage.upload_freespin_data_section_locator).click()


@step("I upload the bonus fact mappings")
def select_data_mapping(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "bonuses_facts_mapping.csv")
    sleep(2)
    context.browser.find_element(*FactsDataPage.browse_bonuses_map_locator).send_keys(dimensions_file)


@step("I upload the freespin fact mappings")
def select_data_mapping(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "freespin_mapping.csv")
    sleep(2)
    context.browser.find_element(*FactsDataPage.browse_freespin_map_locator).send_keys(dimensions_file)


@step("I upload the casino wager fact mappings")
def select_data_mapping(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    sleep(2)
    context.browser.find_element(*FactsDataPage.browse_casino_wager_map_locator).send_keys(dimensions_file)


@step("I upload the sports wager fact mappings")
def select_data_mapping(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    sleep(2)
    context.browser.find_element(*FactsDataPage.browse_sports_wager_map_locator).send_keys(dimensions_file)


@step("I upload the lottery wager fact mappings")
def select_data_mapping(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")
    sleep(2)
    context.browser.find_element(*FactsDataPage.browse_lottery_wager_map_locator).send_keys(dimensions_file)


@step("I complete the mappings for casino wagers facts")
def complete_freespin_mappings(context):
    btns = context.browser.find_elements_by_tag_name("button")
    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerPlayerID"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[3]/div[2]/div/div/ul/li[8]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerCurrency"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[4]/div[2]/div/div/ul/li[1]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerAmount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[5]/div[2]/div/div/ul/li[2]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerName"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[6]/div[2]/div/div/ul/li[3]/a').click()

    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerCategory"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[7]/div[2]/div/div/ul/li[4]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerDate"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[8]/div[2]/div/div/ul/li[5]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerCount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[9]/div[2]/div/div/ul/li[6]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerChannel"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group92"]/div/div[10]/div[2]/div/div/ul/li[7]/a').click()

    context.browser.find_element_by_id("fileFactWagersCasinoMapSave").click()
    sleep(2)


@step("I complete the mappings for sport wagers facts")
def complete_freespin_mappings(context):
    btns = context.browser.find_elements_by_tag_name("button")
    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsPlayerID"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[3]/div[2]/div/div/ul/li[11]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsCurrency"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[4]/div[2]/div/div/ul/li[1]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsAmount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[5]/div[2]/div/div/ul/li[2]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsSport"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[6]/div[2]/div/div/ul/li[3]/a').click()

    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsLeague"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[7]/div[2]/div/div/ul/li[4]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsEvent"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[8]/div[2]/div/div/ul/li[5]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsLive"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[9]/div[2]/div/div/ul/li[6]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsEventDate"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[10]/div[2]/div/div/ul/li[7]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsDate"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[11]/div[2]/div/div/ul/li[8]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsCount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[12]/div[2]/div/div/ul/li[9]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerSportsChannel"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group102"]/div/div[13]/div[2]/div/div/ul/li[10]/a').click()

    context.browser.find_element_by_id("fileFactWagersSportsMapSave").click()
    sleep(2)


@step("I complete the mappings for lottery wagers facts")
def complete_lottery_mappings(context):
    btns = context.browser.find_elements_by_tag_name("button")
    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryPlayerID"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[3]/div[2]/div/div/ul/li[9]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryCurrency"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[4]/div[2]/div/div/ul/li[1]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryAmount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[5]/div[2]/div/div/ul/li[2]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryName"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[6]/div[2]/div/div/ul/li[3]/a').click()

    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryCategory"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[7]/div[2]/div/div/ul/li[4]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryDrawDate"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[8]/div[2]/div/div/ul/li[5]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryCount"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[10]/div[2]/div/div/ul/li[7]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlWagerLotteryChannel"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group142"]/div/div[11]/div[2]/div/div/ul/li[8]/a').click()

    context.browser.find_element_by_id("fileFactWagersLotteryMapSave").click()
    sleep(2)


@step("I complete the mappings for free spins facts")
def complete_freespin_mappings(context):
    btns = context.browser.find_elements_by_tag_name("button")
    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlFreespinPlayerID"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group62"]/div/div[3]/div[2]/div/div/ul/li[4]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlFreespinDescription"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group62"]/div/div[4]/div[2]/div/div/ul/li[1]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlFreespinNumber"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group62"]/div/div[5]/div[2]/div/div/ul/li[2]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlFreespinTime"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group62"]/div/div[6]/div[2]/div/div/ul/li[3]/a').click()

    context.browser.find_element_by_id("fileFactFreespinMapSave").click()
    sleep(2)

@step("I complete the mappings for bonuses facts")
def complete_mappings(context):
    btns = context.browser.find_elements_by_tag_name("button")
    bonus_description_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusDescription"][0]
    bonus_description_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[4]/div[2]/div/div/ul/li[1]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusPlayerID"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[3]/div[2]/div/div/ul/li[6]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusProductID"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[5]/div[2]/div/div/ul/li[2]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusCurrency"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[6]/div[2]/div/div/ul/li[3]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusValue"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[7]/div[2]/div/div/ul/li[4]/a').click()

    bonus_btn = [btn for btn in btns if btn.get_attribute("data-id") == "ddlBonusTime"][0]
    bonus_btn.click()
    sleep(1)
    context.browser.find_element_by_xpath('//*[@id="accordion-group52"]/div/div[8]/div[2]/div/div/ul/li[5]/a').click()

    context.browser.find_element_by_id("fileFactBonusesMapSave").click()
    sleep(2)


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


@step("I am able to upload bonus fact data with mapping")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "bonuses_facts_mapping.csv")
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


@step("I am able to upload free spins fact data with mappings")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "freespin_mapping.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_free_spin_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload casino wagers fact data with mappings")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_casino_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload sport wagers fact data with mappings")
def upload_bonus_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_sport_btn_locator).send_keys(dimensions_file)
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


@step("I am able to upload wagers casino fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_casino_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload lottery wagers fact data with mappings")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers_mappings.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_lottery_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    # assert context.browser.find_element(
    #     *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload payouts fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "payouts.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_payouts_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload wagers sports fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_sport_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload wagers lottery fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_lottery_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload wagers parimutuel fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "wagers.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_wager_parimutuel_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload deposits fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "deposits.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_deposits_btn_locator).send_keys(dimensions_file)
    upload_btns = context.browser.find_elements(*FactsDataPage.upload_btn_locator)

    [btn for btn in upload_btns if btn.is_displayed()][0].click()

    upload_confirmation_form = context.browser.find_element(*DimensionsDataPage.upload_confirmation_form_locator)
    sleep(2)
    upload_confirmation_form.find_element(*DimensionsDataPage.upload_confirmation_btn_locator).click()

    assert context.browser.find_element(
        *DimensionsDataPage.notification_title_locator).text.split()[0].upper() == "SUCCESS"


@step("I am able to upload withdrawals fact data")
def upload_wagers_casino_data(context):
    dimensions_file = join(dirname(abspath(__file__)), "data", "withdrawals.csv")

    sleep(2)

    context.browser.find_element(*FactsDataPage.browse_withdawals_btn_locator).send_keys(dimensions_file)
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


@step("The dimension bonuses are saved in the db")
def assert_dim_bonuses_saved(context):
    for bonus in context.bonuses:
        url = "http://{}/dim_bonuses?name={}&vertical_id={}".format(
            get_config().get("test_framework", "db"), bonus.Identifier, bonus.ProductID)
        db_bonus = get_until_not_empty(url, timeout=100)
        assert len(db_bonus) == 1
        assert db_bonus[0]['BonusID'] > 1
        assert db_bonus[0]['MerchantID'] > 1
        assert db_bonus[0]['Name'] == bonus.Identifier
        assert db_bonus[0]['VerticalID'] == int(bonus.ProductID)


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


@step("The wagers are saved in the db")
def assert_wager_casino_saved(context):
    for fact in context.facts:
        url = "http://{}/wagers?customer_id={}".format(
            get_config().get("test_framework", "db"), fact.player_id)
        assert get_until_not_empty(url, timeout=100) != []


@step("The deposits are saved in the db")
def assert_deposits_saved(context):
    for fact in context.deposits:
        url = "http://{}/deposits?customer_id={}".format(
            get_config().get("test_framework", "db"), fact.player_id)
        assert get_until_not_empty(url, timeout=100) != []


@step("The withdrawals are saved in the db")
def assert_deposits_saved(context):
    for withdrawal in context.withdrawals:
        url = "http://{}/withdrawals?customer_id={}".format(
            get_config().get("test_framework", "db"), withdrawal.player_id)
        assert get_until_not_empty(url, timeout=100) != []


@step("The payouts are saved in the db")
def assert_payouts_saved(context):
    for payout in context.payouts:
        url = "http://{}/payouts?customer_id={}".format(
            get_config().get("test_framework", "db"), payout.player_id)
        assert get_until_not_empty(url, timeout=100) != []
