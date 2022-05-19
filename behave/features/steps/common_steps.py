from behave import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait


def assert_header_on_page(title, context):
    heading = context.helperfunc.find_by_xpath('//h1')
    assert heading is not None
    assert heading.text == title


def wait_until_page_is_loaded(path, context):
    def do_test(*args):
        return context.helperfunc.get_current_path() == path
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(do_test)


@step(u'I click continue')
def step_click_continue(context):
    # click on the continue button
    continue_button = context.helperfunc.find_by_id("submit-button")
    assert continue_button is not None
    continue_button.click()
    # did the form get submitted correctly?
    # check for 'there is a problem'
    try:
        confirmation_text_element = context.helperfunc.driver().find_element_by_css_selector(".govuk-error-summary")
        if confirmation_text_element is not None:
            assert confirmation_text_element.text.startswith("There is a problem")
            raise AssertionError(f"There is a problem with submitting the form")
    except NoSuchElementException as ex:
        # this will error because we actually moved off the page which is actually what we want
        pass


@step(u'I am taken to the "{header}" page located on "{page}"')
def step_check_page(context, page, header):
    wait_until_page_is_loaded(page, context)
    assert_header_on_page(header, context)
