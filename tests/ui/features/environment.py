import os
from pathlib import Path
from os.path import join
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from tests.ui.config.config import get_config


def before_all(context):
    p = Path(__file__).parents[1]
    context.screenshots_dir = join(str(p), "screenshots", os.getenv("BROWSER"))


def before_scenario(context, scenario):
    options = Options()
    browser = os.getenv("BROWSER")
    context.browser = WebDriver("http://{}:4444/wd/hub".format(get_config().get("browser", "host")),
                                desired_capabilities={"browserName": browser},
                                options=options)
    if browser == "firefox":
        options.set_preference("browser.tabs.remote.autostart", False)
        options.set_preference("security.insecure_password.ui.enabled", False)
        options.set_preference("security.insecure_field_warning.contextual.enabled", False)
    context.browser.set_page_load_timeout(60)
    context.browser.implicitly_wait(60)

    os.makedirs(join(context.screenshots_dir, scenario.name.replace(" ", "_")), exist_ok=True)
    context.screenshots_dir = join(context.screenshots_dir, scenario.name.replace(" ", "_"))


def after_step(context, step):
    try:
        context.browser.save_screenshot(join(context.screenshots_dir, "{}.png".format(step.name)))
    except Exception:
        print("Could not take screenshot")


def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.browser.save_screenshot(join(context.screenshots_dir, "{}_failed.png".format(scenario.name)))
    context.browser.quit()
