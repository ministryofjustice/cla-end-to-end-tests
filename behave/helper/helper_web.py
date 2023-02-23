from selenium import webdriver
from helper.helper_base import HelperFunc
from helper.constants import SELENIUM_WEB_DRIVER_URL


def get_browser(browser, download_directory):
    if browser == "chrome":

        prefs = {"download.default_directory": download_directory}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", prefs)
        capabilities = chrome_options.to_capabilities()
        return HelperFunc(
            webdriver.Remote(SELENIUM_WEB_DRIVER_URL, desired_capabilities=capabilities)
        )
