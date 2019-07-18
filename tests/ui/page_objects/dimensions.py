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

