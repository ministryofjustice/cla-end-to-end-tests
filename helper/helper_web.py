from selenium import webdriver
from helper.helper_base import HelperFunc
 
def get_browser(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        return HelperFunc(webdriver.Chrome(chrome_options = options))