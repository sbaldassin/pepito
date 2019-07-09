from behave import step

from tests.ui.config.config import get_config


@step("I navigate to the home page")
def navigate_to_home(context):
    context.browser.get(get_config().get("webapp", "url"))