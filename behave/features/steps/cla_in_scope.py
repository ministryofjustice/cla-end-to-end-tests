from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from features.constants import CLA_PUBLIC_URL


@given(u'I have selected the start now button on the start page')
def step_in_scope_education(context):
    start_page_url = f"{CLA_PUBLIC_URL}"
    context.helperfunc.open(start_page_url)
    heading = context.helperfunc.find_by_xpath('//h1')
    assert heading is not None
    assert heading.text == "Check if you can get legal aid"

    start_button = context.helperfunc.find_by_id('start')
    assert start_button is not None
    assert start_button.text == "Start now"

    start_button.click()

    def wait_until_page_is_loaded_after_start_button_is_clicked(*args):
        return context.helperfunc.get_current_path() == "/scope/diagnosis/"
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_page_is_loaded_after_start_button_is_clicked)


