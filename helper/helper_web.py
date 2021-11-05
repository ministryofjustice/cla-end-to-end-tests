from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from helper.helper_base import HelperFunc
from features.constants import SELENIUM_WEB_DRIVER_URL

 
def get_browser(browser):
    if browser == "chrome":
        return HelperFunc(webdriver.Remote(SELENIUM_WEB_DRIVER_URL, DesiredCapabilities.CHROME))