from behave import step

from tests.ui.config.config import get_config
from tests.ui.page_objects.home_page import HomePage
from tests.ui.page_objects.campaign_notifications_page import CampaignNotificationsPage


@step("I verify the total campaign notifications")
def verify_campaign_notifications_errors(context):
    total_errors = int(context.browser.find_element(*HomePage.campaign_notifications_badge_locator).text)
    assert total_errors >= 0


@step("I verify the notification page title")
def verify_page_title(context):
    title = context.browser.find_element(*CampaignNotificationsPage.page_title_locator).text
    assert title == 'Notifications'


@step("I click on delete all notifications button")
def click_delete_all(context):
    context.browser.find_element(*CampaignNotificationsPage.delete_all_btn_locator).click()


@step("I click on cancel button")
def click_delete_all(context):
    previous_notifications = int(context.browser.find_element(*HomePage.campaign_notifications_badge_locator).text)
    context.browser.find_element(*CampaignNotificationsPage.cancel_btn_locator).click()
    current_notifications = int(context.browser.find_element(*HomePage.campaign_notifications_badge_locator).text)
    assert previous_notifications == current_notifications
