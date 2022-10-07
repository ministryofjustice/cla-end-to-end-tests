from selenium import webdriver
from helper.helper_base import HelperFunc
from features.constants import SELENIUM_WEB_DRIVER_URL, DOWNLOAD_DIRECTORY


def get_browser(browser):
    if browser == "chrome":
        actual_path = DOWNLOAD_DIRECTORY
        prefs = {"download.default_directory": actual_path}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", prefs)
        capabilities = chrome_options.to_capabilities()
        return HelperFunc(
            webdriver.Remote(SELENIUM_WEB_DRIVER_URL, desired_capabilities=capabilities)
        )
