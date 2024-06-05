from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from helper.backend import Backend

from helper.constants import CALL_CENTRE_ZONE
from datetime import datetime, timedelta


class HelperFunc(object):
    __TIMEOUT = 10

    def __init__(self, driver):
        super(HelperFunc, self).__init__()
        self._driver_wait = WebDriverWait(driver, HelperFunc.__TIMEOUT)
        self._driver = driver
        self.call_centre_backend = Backend("/call_centre/api/v1/")
        self.call_centre_backend.authenticate(**CALL_CENTRE_ZONE)
        today = datetime.now().date()
        self.date_start_this_month = (today - timedelta(days=today.day)).replace(day=1)

    def driver(self):
        return self._driver

    def delete_cookies(self):
        return self._driver.delete_all_cookies()

    def open(self, url):
        self._driver.get(url)

    def maximize(self):
        self._driver.maximize_window()

    def close(self):
        self._driver.quit()

    def get_cookie(self, cookie):
        return self._driver.get_cookie(cookie)

    def get_cookies(self):
        return self._driver.get_cookies()

    # Get the date set in the init method
    # if needed, create a set method to override the date set in init
    def get_date_now(self):
        return self.date_start_this_month

    # Takes screenshot, specifically it grabs the entire body of the page.
    def take_screenshot(self, scenario_file_path):
        element = self._driver.find_element_by_tag_name("body")
        element.screenshot(scenario_file_path)

    # Helper functions to find web elements, possibly will be in a different place

    def find_by_xpath(self, xpath):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

    # added in so can check if there is more then one element on the page
    def find_many_by_xpath(self, xpath):
        return self._driver_wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )

    def javascript_wait_for_ready_state(self):
        WebDriverWait(self._driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete",
            "Page ready state is not complete",
        )

    def find_by_css_selector(self, css):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )

    def find_by_css_selector_without_wait(self, css):
        return self._driver.find_element(By.CSS_SELECTOR, css)

    def find_by_name(self, name):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.NAME, name))
        )

    def find_by_id(self, id):
        return self._driver_wait.until(EC.visibility_of_element_located((By.ID, id)))

    def find_by_class(self, class_name):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        )

    # added in so can check if there is more then one element on the page
    def find_many_by_class(self, class_name):
        return self._driver_wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, class_name))
        )

    def find_by_link_text(self, text):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, text))
        )

    def refresh(self):
        # Refresh the page you're on.
        return self._driver.refresh()

    def find_by_partial_link_text(self, text):
        return self._driver_wait.until(
            EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, text))
        )

    def get_current_path(self):
        return urlparse(self._driver.current_url).path

    def get_url(self):
        return self._driver.current_url

    def scroll_to_top(self):
        self._driver.execute_script("window.scrollTo(0, 0);")

    def get_case_from_backend(self, case_reference):
        return self.call_centre_backend.get_case(case_reference)

    def get_case_personal_details_from_backend(self, case_reference):
        return self.call_centre_backend.get_case_personal_details(case_reference)

    def get_case_callback_details_from_backend(self, case_reference):
        return self.call_centre_backend.get_case_callback_details(case_reference)

    def update_case_callback_details(self, case_reference, case_json):
        return self.call_centre_backend.update_case_callback_details(
            case_reference, case_json
        )

    def get_future_callbacks(self):
        return self.call_centre_backend.get_future_callbacks()

    def click_button(self, selector_type, selector):
        wait = WebDriverWait(
            self._driver, 10, ignored_exceptions=StaleElementReferenceException
        )
        wait.until(EC.element_to_be_clickable((selector_type, selector))).click()
