from selenium.webdriver.common.by import By


class DimensionsDataPage:
    browse_btn_locator = (By.ID, "fileDimCustomers")
    upload_btn_locator = (By.CLASS_NAME, "icon-file-upload2")
    upload_confirmation_form_locator = (By.CLASS_NAME, "showSweetAlert")
    upload_confirmation_btn_locator = (By.CLASS_NAME, "confirm")
    notification_title_locator = (By.CLASS_NAME, "ui-pnotify-title")
    game_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[4]")
    upload_game_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[4]")
    browse_game_btn_locator = (By.ID, "fileDimGame")
    freespin_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[3]")
    upload_freespin_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[3]")
    browse_freespin_btn_locator = (By.ID, "fileDimFreespin")
    bonuses_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[2]")
    upload_bonuses_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[2]")
    browse_bonuses_btn_locator = (By.ID, "fileDimBonuses")


class FactsDataPage:
    navigation_tabs_locator = (By.CLASS_NAME, "nav-tabs-bottom")
    data_fact_type_locator = (By.TAG_NAME, "a")
    browse_btn_locator = (By.ID, "fileFactBonuses")
    browse_free_spin_btn_locator = (By.ID, "fileFactFreespin")
    browse_game_session_btn_locator = (By.ID, "fileFactGame")
    browse_wager_casino_btn_locator = (By.ID, "fileFactWagersCasino")
    browse_wager_sport_btn_locator = (By.ID, "fileFactWagersSports")
    browse_wager_lottery_btn_locator = (By.ID, "fileFactWagersLottery")
    browse_wager_parimutuel_btn_locator = (By.ID, "fileFactWagersParimutuel")
    browse_deposits_btn_locator = (By.ID, "fileFactRevenue")
    browse_withdawals_btn_locator = (By.ID, "fileFactWithdrawal")
    upload_btn_locator = (By.CLASS_NAME, "fileinput-upload-button")
