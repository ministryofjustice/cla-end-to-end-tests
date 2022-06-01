from behave import *
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from features.constants import CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK


def assert_header_on_page(title, context):
    heading = context.helperfunc.find_by_xpath('//h1')
    assert heading is not None
    assert heading.text == title


def wait_until_page_is_loaded(path, context):
    def do_test(*args):
        return context.helperfunc.get_current_path() == path
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(do_test)


def compare_client_details_with_backend(context, case_id, client_section):
    # look for the client details on the left hand side of screen
    assert client_section is not None
    # check it is the right client, use the table details to see which elements to check
    for row in context.table:
        element = CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK[row['details']]["form_element_type"]
        title_value = CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK[row['details']]["form_element_title"]
        backend_id = CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK[row['details']]["backend_id"]
        xpath_string = f'//{element}[@title="{title_value}"]'
        displayed_value = client_section.find_element_by_xpath(xpath_string).text
        backend_value = context.helperfunc.get_case_personal_details_from_backend(case_id)[backend_id]
        assert displayed_value == backend_value, \
            f"For {title_value}, value displayed is {displayed_value} but actual value is {backend_value}"


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


@step(u'I am taken to the "{type_of_user}" case details page')
def step_on_case_details_page(context, type_of_user):
    # get the case reference
    if hasattr(context, 'selected_case_ref'):
        case_id = context.selected_case_ref
    else:
        case_id = None
    # check the url of the page
    url_dir = None
    if type_of_user == "specialist provider":
        url_dir = "provider"
    elif type_of_user == "call centre":
        url_dir = "call_centre"
    else:
        assert url_dir is None, f"Incorrect path given to step function"
    # will look like /url_dir/CASEID/diagnosis/
    if case_id is not None:
        page = f"/{url_dir}/{context.selected_case_ref}/diagnosis/"
        wait_until_page_is_loaded(page, context)
        assert_header_on_page(case_id, context)
    else:
        # can use the function with the regex on test_steps
        # this will fail if this is for a specialist provider
        context.execute_steps(u'''
               Given I select to 'Create a case'
           ''')


@when(u'I select the diagnosis <category> and click next <number> times')
def step_impl(context):
    form = context.helperfunc.find_by_name('diagnosis-form')
    assert form.is_displayed()
    # work out which category to choose
    # note that there is one category where have to click 'next' twice
    for row in context.table:
        category_text = row['category']
        next_number = row["number"]
        # find the radio input next to the text of the category
        x_path = f".//p[contains(text(),'{category_text}')]//ancestor::label/input[@type='radio']"
        # for some reason these seem to return stale element errors
        try:
            context.helperfunc.find_by_xpath(x_path).click()
        except StaleElementReferenceException:
            context.helperfunc.find_by_xpath(x_path).click()
        # now click next the correct number of times (normally 1)
        for _ in range(int(next_number)):
            try:
                context.helperfunc.find_by_name("diagnosis-next").click()
            except StaleElementReferenceException:
                context.helperfunc.find_by_name("diagnosis-next").click()
    # Makes sure we at the end of the scope assessment
    assert context.helperfunc.find_by_partial_link_text('Create financial assessment').is_displayed()




