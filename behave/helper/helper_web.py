from selenium import webdriver
from helper.helper_base import HelperFunc
from helper.constants import (
    SELENIUM_WEB_DRIVER_URL,
    USING_CHROME_DRIVER,
    CHROME_DRIVER_LOCATION,
)


def get_browser(browser, download_directory):
    if browser == "chrome":

        prefs = {"download.default_directory": download_directory}
        chrome_options = webdriver.ChromeOptions()
        if USING_CHROME_DRIVER:
            # we need to let chromedriver know where to look
            chrome_options.binary_location = CHROME_DRIVER_LOCATION
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", prefs)
        capabilities = chrome_options.to_capabilities()
        return HelperFunc(
            webdriver.Remote(command_executor=SELENIUM_WEB_DRIVER_URL, options=chrome_options)
        )
