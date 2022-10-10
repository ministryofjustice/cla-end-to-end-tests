from common_steps import select_value_from_list
from features.constants import CLA_EXISTING_USER, MINIMUM_SLEEP_SECONDS
from behave import step, given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


@given("a client with an existing case is added to it")
def step_impl_client_with_existing_case(context):
    select_value_from_list(
        context,
        label="Search for existing user",
        op="startswith",
        value=CLA_EXISTING_USER,
    )
    # there will be an alert asking if you wish to continue
    assert (
        context.helperfunc.driver().switch_to.alert is not None
    ), "No alert confirming you want to add the user"
    context.helperfunc.driver().switch_to.alert.accept()


@step("I select ‘Create Scope Diagnosis'")
def step_impl_select_create_scope(context):
    context.helperfunc.find_by_name("diagnosis-new").click()


@step("I select the diagnosis <category> and click next <number> times")
def step_impl_select_diagnosis_category(context):
    def wait_for_diagnosis_form(*args):
        form = context.helperfunc.find_by_name("diagnosis-form")
        return form is not None and form.is_displayed()

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_diagnosis_form)

    # work out which category to choose
    # note that there is one category where have to click 'next' twice
    for row in context.table:
        category_text = row["category"]
        next_number = row["number"]
        # find the radio input next to the text of the category
        x_path = f".//p[contains(text(),'{category_text}')]//ancestor::label/input[@type='radio']"
        # for some reason these seem to return stale element errors
        context.helperfunc.click_button(By.XPATH, x_path)
        # now click next the correct number of times (normally 1)
        for _ in range(int(next_number)):
            context.helperfunc.click_button(By.NAME, "diagnosis-next")
            # This is required because the diagnosis-next button on the current page and next page have the same name
            # Without this sleep it will just find the same button and click it again instead of waiting for new button
            # to load
            time.sleep(MINIMUM_SLEEP_SECONDS)

    # Makes sure we at the end of the scope assessment
    # We can't rely on Finance tab being active as the scope could be out of scope

    def wait_for_diagnosis_delete_btn(*args):
        diagnosis_btn = context.helperfunc.find_by_name("diagnosis-delete")
        return diagnosis_btn is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_diagnosis_delete_btn)


@step('I get an "{scope}" decision')
def step_impl_scope_decision(context, scope):
    text = context.helperfunc.find_by_name("diagnosis-form").text
    assert scope in text


@step("select 'Create financial assessment'")
def step_impl_create_financial_assessment(context):
    context.helperfunc.find_by_partial_link_text("Create financial assessment").click()


@step("I am taken to the Finances tab with the ‘Details’ sub-tab preselected")
def step_impl_finances_tab(context):
    selected_tab = context.helperfunc.find_by_css_selector(
        "li[class='Tabs-tab is-active']"
    )
    assert "Finances" in selected_tab.text


@then('I select the "{category}" knowledge base category')
def step_impl_select_category(context, category):
    select_value_from_list(context, label="Law category", value=category)
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)


@then('I select the alternative help organisations "{organisation}"')
def step_impl_select_alt_help_org(context, organisation):
    name, _ = organisation.split(" - ")
    search_input = context.helperfunc.find_by_xpath(
        "//input[@placeholder='Search providers and other help organisations']"
    )
    search_input.clear()
    search_input.send_keys(name)
    submit = search_input.find_element_by_xpath("following-sibling::*")
    submit.click()
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)
    search_results_form = context.helperfunc.find_by_xpath(
        '//form[@name="alternative_help"]'
    )
    # This will only find the first search result which is fine because we are searching for a specific organisation
    parent_wrapper = search_results_form.find_element_by_xpath(
        './/input[@name="selected_providers"]/ancestor::div[1]'
    )
    assert (
        parent_wrapper.find_element_by_css_selector(".FormRow-label strong").text
        == organisation
    )
    parent_wrapper.find_element_by_css_selector("label.FormRow-label").click()


@step('I enter "{comment}" in the Assignment comments box')
def step_impl_enter_assignment_comment(context, comment):
    text_area = context.helperfunc.find_by_xpath(
        '//textarea[@name="assign-notes"][@placeholder="Assignment comments"]'
    )
    text_area.send_keys(comment)
    assert text_area.get_attribute("value") == comment


@then("I click the Assign Alternative Help button")
def step_impl_click_assign_alt_help(context):
    submit_btn = context.helperfunc.find_by_xpath(
        '//button[@name="assign-alternative-help"]'
    )
    submit_btn.click()


@step("I am shown the survey reminder")
def step_impl_survey_reminder_shown(context):
    def wait_for_survey_reminder_dialog(*args):
        return context.helperfunc.find_by_css_selector(".modal-dialog") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(
        wait_for_survey_reminder_dialog, "Could not find survey reminder modal dialog"
    )
    heading = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content header h2"
    )
    assert heading.text == "Survey reminder"


@then("select continue on the survey reminder")
def step_impl_select_continue_on_survey(context):
    continue_btn = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content .FormActions button"
    )
    assert continue_btn.text == "Continue"
    continue_btn.click()
