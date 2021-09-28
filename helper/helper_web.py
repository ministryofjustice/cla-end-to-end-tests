from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from helper.helper_base import HelperFunc
 
def get_browser(browser):
    if browser == "chrome":
        return HelperFunc(webdriver.Remote("http://seleniumchrome:4444/wd/hub", DesiredCapabilities.CHROME))