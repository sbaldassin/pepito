from selenium.webdriver.common.by import By


class HomePage:
    username_field_locator = (By.ID, "txtLoginName")
    password_field_locator = (By.ID, "txtPassword")
    login_form_locator = (By.CLASS_NAME, "login-form")
    login_btn_locator = (By.TAG_NAME, "button")
    logged_in_name_locator = (By.ID, "spanUser")
