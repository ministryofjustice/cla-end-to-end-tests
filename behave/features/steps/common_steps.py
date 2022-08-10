import re
from behave import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from features.constants import CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK, CLA_FRONTEND_URL, USERS, USER_HTML_TAGS
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def remove_prefix(text, prefix):
    return text[len(prefix):] if text.startswith(prefix) else text


def assert_header_on_page(title, context):
    # occasionally there could be more than one h1 on the page. In most cases we want the first one
    # Go through the list to check all h1 elements
    headings = context.helperfunc.find_many_by_xpath('//h1')
    assert headings is not None
    found_heading = False
    # check each of the headings to see if we have a match
    for heading in headings:
        if heading.text == title:
            found_heading = True
    error_message = f"{title} not found on {context.helperfunc.get_current_path()}"
    assert found_heading, error_message


def wait_until_page_is_loaded(path, context):
    def do_test(*args):
        return context.helperfunc.get_current_path() == path
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(do_test)


def click_on_hyperlink_and_get_href(context, hyperlink_text):
    # this is a generic step to click on a hyperlink
    assert context.helperfunc.find_by_link_text(hyperlink_text) is not None, f"Could not find link: {hyperlink_text}"
    hyperlink_href = context.helperfunc.find_by_link_text(hyperlink_text).get_attribute("href")
    context.helperfunc.click_button(By.LINK_TEXT, hyperlink_text)
    # return the href
    return hyperlink_href


@step(u'I select the link "{hyperlink_text}"')
def step_impl(context, hyperlink_text):
    # this is a generic step to click on a hyperlink
    context.helperfunc.click_button(By.LINK_TEXT, hyperlink_text)


@step(u'I select the \'Sign out\' link')
def step_impl(context):
    # We need to be on a page that we can control, otherwise the current page could have a modal dialog visible which
    # could impact how we can interact with menu elements
    context.helperfunc.open(f"{CLA_FRONTEND_URL}")
    page = context.helperfunc
    context.header = page.find_by_xpath("//header[@id='global-header']")
    # wait for the menu link to be visible then click
    user_menu = "//div[@class='UserMenu']/a"
    page.click_button(By.XPATH, user_menu)
    # Find the SignOut link now it's visible
    signout_link_xpath = "//ul[@id='UserMenu-links']/li[2]/a"
    page.click_button(By.XPATH, signout_link_xpath)


def switch_to_new_tab(context, new_tab_handle, hyperlink_selected):
    context.helperfunc.driver().switch_to.window(new_tab_handle)
    # check the url
    error_string = f"Chosen link : {hyperlink_selected} is not the same as the tab url: {context.helperfunc.driver().current_url}"
    assert hyperlink_selected == context.helperfunc.driver().current_url, error_string


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


def step_click_submit(context):
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


@step(u'that I am logged in as "{user}"')
def step_impl(context, user):
    login_url = USERS[user]["login_url"]
    context.helperfunc.open(login_url)
    if USERS[user]["application"] == "FRONTEND":
        form = context.helperfunc.find_by_name(USER_HTML_TAGS[USERS[user]["application"]]["form_identifier"])
        submit_xpath = f"//button[@type='submit']"
        # on CHS, there is a tag which indicates whether you are logged in as an operator or a provider
        # does not exist on fox_admin
        if USERS[user]["user_type"] == "OPERATOR":
            html_tag = "//html[@ng-app='cla.operatorApp']"
        else:
            html_tag = "//html[@ng-app='cla.providerApp']"
    else:
        form = context.helperfunc.find_by_id(USER_HTML_TAGS[USERS[user]["application"]]["form_identifier"])
        submit_xpath = f"//input[@type='submit']"
        html_tag = None
    assert form is not None
    form.find_element_by_name("username").send_keys(USERS[user]["username"])
    form.find_element_by_name("password").send_keys(USERS[user]["password"])
    form.find_element_by_xpath(submit_xpath).click()
    if html_tag is not None:
        element = context.helperfunc.find_by_xpath(html_tag)
        assert element is not None


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


@step(u'I am taken to the "{header}" page for the case located at "{sub_page}"')
def step_impl(context, sub_page, header):
    # can't use the above step because there is a case reference in the url
    # find the first part of the url
    # sub_page will already have / at start and possibly at end as required
    current_path = context.helperfunc.get_current_path()
    reg_ex = re.compile(r"(\w{2}-\d{4}-\d{4})")
    case_reference_id = reg_ex.search(current_path).group(1)
    required_page = f"/call_centre/{case_reference_id}{sub_page}"
    wait_until_page_is_loaded(required_page, context)
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
              Given I am taken to the 'case details' page
           ''')


def select_value_from_list(context, label, value, op='equals'):
    label_link = context.helperfunc.find_by_xpath(f"//span[text()='{label}']/..")
    # Clicking this link will automatically focus the input for us to type into
    label_link.click()
    input_element = context.helperfunc.driver().switch_to.active_element
    input_element.send_keys(value)

    list_id = input_element.get_attribute("aria-owns")
    # Get the list of possible items that match our value
    list_element = context.helperfunc.find_by_id(list_id)

    def wait_for_list_of_values(*args):
        try:
            list_element.find_element_by_css_selector('.select2-highlighted')
            return True
        except NoSuchElementException:
            return False

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_list_of_values, message=f"Could not find any matches for {value} in {label} list")

    list_item = list_element.find_element_by_css_selector('.select2-highlighted')
    if op.lower() == 'startswith':
        assert list_item.text.startswith(value), f"Could not find value {value} in {label} list"
    else:
        assert value == list_item.text, f"Could not find value {value} in {label} list"
    list_item.click()


def search_and_select_case(context, case_reference):
    # This method searches for and clicks on the case in the case list
    # prevents not finding it if the list goes onto two pages.
    context.selected_case_ref = case_reference
    search_bar = context.helperfunc.find_by_id("case-search")
    search_bar.send_keys(case_reference)
    search_submit = context.helperfunc.find_by_class("CaseSearch-submit")
    search_submit.click()
    context.helperfunc.click_button(By.LINK_TEXT, case_reference)


@step(u'the message \'{message}\' appears on the case details page')
def step_impl(context, message):
    element = context.helperfunc.find_by_css_selector(".Notice.Notice--closeable.success")
    assert element.text == message
