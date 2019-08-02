from selenium.webdriver.common.by import By


class DimensionsDataPage:
    browse_btn_locator = (By.ID, "fileDimCustomers")
    upload_btn_locator = (By.CLASS_NAME, "icon-file-upload2")
    upload_confirmation_form_locator = (By.CLASS_NAME, "showSweetAlert")
    upload_confirmation_btn_locator = (By.CLASS_NAME, "confirm")
    notification_title_locator = (By.CLASS_NAME, "ui-pnotify-title")
    alert_message_locator = (By.XPATH, "//div[@class='alert label-theme-success alert-styled-left alert-arrow-left alert-bordered']")
    game_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[4]")
    upload_game_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[4]")
    browse_game_btn_locator = (By.ID, "fileDimGame")
    freespin_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[3]")
    data_mapping_section_locator = (By.XPATH, "//div[@class='tab-pane active']//div[@class='panel panel-white'][2]//a")
    upload_freespin_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[3]")
    browse_freespin_btn_locator = (By.ID, "fileDimFreespin")
    browse_freespin_map_btn_locator = (By.ID, "fileDimFreespinMap")
    browse_customer_map_btn_locator = (By.ID, "fileDimCustomersMap")
    freespin_description_btn_locator = (By.XPATH, "//button[@data-id='ddlFreespinDescription']")
    freespin_number_btn_locator = (By.XPATH, "//button[@data-id='ddlFreespinNumber']")
    freespin_map_save_btn_locator = (By.XPATH, "//div[contains(@id,'fileDimFreespinMapSave')]/button")
    freespin_map_headers = (By.XPATH, "//div[@class='btn-group bootstrap-select dropup open']//div[@class='dropdown-menu open']//ul//li")
    customer_player_id_btn_locator = (By.XPATH, "//button[@data-id='ddlCustomerPlayerID']")
    customer_country_btn_locator = (By.XPATH, "//button[@data-id='ddlCustomerCountry']")
    customer_email_btn_locator = (By.XPATH, "//button[@data-id='ddlCustomerEmail']")
    customer_sign_up_btn_locator = (By.XPATH, "//button[@data-id='ddlCustomerSignUp']")
    customer_map_save_btn_locator = (By.XPATH, "//div[contains(@id,'fileDimCustomersMapSave')]/button")
    bonuses_tab_locator = (By.XPATH, "//div[@class='tabbable']/ul/li[2]")
    browse_bonuses_map_btn_locator = (By.ID, "fileDimBonusesMap")
    upload_bonuses_btn_locator = (By.XPATH, "(//i[@class='icon-file-upload2'])[2]")
    browse_bonuses_btn_locator = (By.ID, "fileDimBonuses")
    bonuses_description_btn_locator = (By.XPATH, "//button[@data-id='ddlBonusDescription']")
    bonuses_product_id_btn_locator = (By.XPATH, "//button[@data-id='ddlBonusProductID']")
    bonuses_map_save_btn_locator = (By.XPATH, "//div[contains(@id,'fileDimBonusesMapSave')]/button")
    browse_games_map_btn_locator = (By.ID, "fileDimGameMap")
    game_name_btn_locator = (By.XPATH, "//button[@data-id='ddlGameName']")
    game_category_btn_locator = (By.XPATH, "//button[@data-id='ddlGameCategory']")
    game_map_save_btn_locator = (By.XPATH, "//div[contains(@id,'fileDimGameMapSave')]/button")


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
    browse_payouts_btn_locator = (By.ID, "fileFactPayout")
    upload_btn_locator = (By.CLASS_NAME, "fileinput-upload-button")
    data_mapping_locator = (By.XPATH, "//*[contains(text(), 'Data Mapping')]")
    upload_bonuses_data_section_locator = (By.XPATH, "//*[contains(text(), 'Upload Bonuses Data')]")
    upload_casino_wagers_data_section_locator = (By.XPATH, "//*[contains(text(), 'Upload Casino Wager Data')]")
    upload_freespin_data_section_locator = (By.XPATH, "//*[contains(text(), 'Upload Freespin Data')]")
    browse_bonuses_map_locator = (By.ID, "fileFactBonusesMap")
    browse_freespin_map_locator = (By.ID, "fileFactFreespinMap")
    browse_casino_wager_map_locator = (By.ID, "fileFactWagersCasinoMap")
    select_bonus_description_locator = (By.ID, "ddlBonusDescription")
    option_bonus_description_locator = (By.XPATH, "//*[contains(text(), 'description')]")