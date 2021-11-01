from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HelperFunc(object):
    __TIMEOUT = 10
 
    def __init__(self, driver):
        super(HelperFunc, self).__init__()
        self._driver_wait = WebDriverWait(driver, HelperFunc.__TIMEOUT)
        self._driver = driver

    def driver(self):
        return self._driver
 
    def open(self, url):
        self._driver.get(url)
 
    def maximize(self):
        self._driver.maximize_window()        
        
    def close(self):
        self._driver.quit()
        
    # Helper functions to find web elements, possibly will be in a different place 
 
    def find_by_xpath(self, xpath):
        return self._driver_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_by_css_selector(self, css):
        return self._driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
 
    def find_by_name(self, name):
        return self._driver_wait.until(EC.visibility_of_element_located((By.NAME, name)))
 
    def find_by_id(self, id):
        return self._driver_wait.until(EC.visibility_of_element_located((By.ID, id)))

    def find_by_class(self, class_name):
        return self._driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))

    def find_by_partial_link_text(self, text):
        return self._driver_wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, text)))

    def get_current_path(self):
        return urlparse(self._driver.current_url).path
