from selenium.webdriver.common.by import By


class ResetPasswordPage:
    username_field_locator = (By.ID, "txtLoginName")
    reset_pass_btn_locator = (By.TAG_NAME, "button")
