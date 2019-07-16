from selenium.webdriver.common.by import By


class CampaignNotificationsPage:
    def __init__(self):
        pass

    page_title_locator = (By.CLASS_NAME, "text-semibold")
    delete_all_btn_locator = (By.CSS_SELECTOR, ".btn.btn-link.btn-float.has-text")
    no_errors_label_locator = (By.CSS_SELECTOR, ".text-semibold.text-white.text-center.dashboard-background")
    confirm_btn_locator = (By.CLASS_NAME, "confirm")
    cancel_btn_locator = (By.CLASS_NAME, "cancel")
