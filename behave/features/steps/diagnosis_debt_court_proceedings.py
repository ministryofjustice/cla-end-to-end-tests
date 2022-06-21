import time
from features.constants import CLA_USER_TO_ASSIGN_CASES_TO, MINIMUM_SLEEP_SECONDS
from common_steps import select_value_from_list
from selenium.webdriver.support.ui import WebDriverWait


@given(u'a client with an existing case is added to it')
def step_impl(context):
    select_value_from_list(context, label="Search for existing user", op="startswith", value=CLA_USER_TO_ASSIGN_CASES_TO)
    # there will be an alert asking if you wish to continue
    assert context.helperfunc.driver().switch_to.alert is not None, "No alert confirming you want to add the user"
    context.helperfunc.driver().switch_to.alert.accept()


@then(u'I select the "{category}" knowledge base category')
def step_impl(context, category):
    select_value_from_list(context, label="Law category", value=category)
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)


@then(u'I select the alternative help organisations "{organisation}"')
def step_impl(context, organisation):
    name, _ = organisation.split(' - ')
    search_input = context.helperfunc.find_by_xpath(f"//input[@placeholder='Search providers and other help organisations']")
    search_input.clear()
    search_input.send_keys(name)
    submit = search_input.find_element_by_xpath('following-sibling::*')
    submit.click()
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)
    search_results_form = context.helperfunc.find_by_xpath('//form[@name="alternative_help"]')
    # This will only find the first search result which is fine because we are searching for a specific organisation
    parent_wrapper = search_results_form.find_element_by_xpath('.//input[@name="selected_providers"]/ancestor::div[1]')
    assert parent_wrapper.find_element_by_css_selector('.FormRow-label strong').text == organisation
    parent_wrapper.find_element_by_css_selector('label.FormRow-label').click()


@then(u'I enter "{comment}" in the Assignment comments box')
def step_impl(context, comment):
    text_area = context.helperfunc.find_by_xpath('//textarea[@name="assign-notes"][@placeholder="Assignment comments"]')
    text_area.send_keys(comment)
    assert text_area.get_attribute("value") == comment


@then(u'I select Assign alternative help')
def step_impl(context):
    submit_btn = context.helperfunc.find_by_xpath('//button[@name="assign-alternative-help"]')
    submit_btn.click()


@then(u'I am shown the survey reminder')
def step_impl(context):
    def wait_for_survey_reminder_dialog(*args):
        return context.helperfunc.find_by_css_selector('.modal-dialog') is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_survey_reminder_dialog, "Could not find survey reminder modal dialog")
    heading = context.helperfunc.find_by_css_selector('.modal-dialog .modal-content header h2')
    assert heading.text == 'Survey reminder'


@then(u'select continue on the the survey reminder')
def step_impl(context):
    continue_btn = context.helperfunc.find_by_css_selector('.modal-dialog .modal-content .FormActions button')
    assert continue_btn.text == "Continue"
    continue_btn.click()
