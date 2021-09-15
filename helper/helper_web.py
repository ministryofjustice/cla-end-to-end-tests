from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from helper.helper_base import HelperFunc
 
def get_browser(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        return HelperFunc(webdriver.Remote("http://127.0.0.1:4444", DesiredCapabilities.CHROME))