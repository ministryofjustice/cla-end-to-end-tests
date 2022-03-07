from behave import *
from features.constants import CLA_PUBLIC_URL, CLA_NUMBER
from features.steps.cla_in_scope import assert_header_on_page, wait_until_page_is_loaded


def assert_form_input_element(callback_form, element_id, value):
    element = callback_form.find_element_by_id(element_id)
    assert element is not None
    element.send_keys(value)
    assert element.get_attribute('value') == value


@given(u'I am have passed the means test')
def step_means_test_page(context):
    # Todo: This is a filler step so that I can write the rest of the feature steps instead of waiting for
    #   Child 2: Means test pass ticket to be completed
    #   This step should be removed when the Child 2: Means test pass ticket has been completed
    url = f"{CLA_PUBLIC_URL}/contact"
    context.helperfunc.open(url)
    assert_header_on_page("Contact Civil Legal Advice", context)


@given(u'I enter "{full_name}" as my full name')
def step_enter_full_name(context, full_name):
    context.form_values = {"full_name": full_name}
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    assert_form_input_element(context.callback_form, "full_name", full_name)


@given(u'I enter "{email}" as my email address')
def step_enter_email_address(context, email):
    context.form_values["email"] = email
    assert_form_input_element(context.callback_form, "email", email)


@given(u'I enter "{postcode}" as my postcode')
def step_enter_postcode(context, postcode):
    context.form_values["postcode"] = postcode
    assert_form_input_element(context.callback_form, "address-post_code", postcode)


@given(u'I enter "{street_address}" street address')
def step_enter_street_address(context, street_address):
    context.form_values["street"] = street_address
    assert_form_input_element(context.callback_form, "address-street_address", street_address)


@given(u'I select the the callback option to callback CLA')
def step_select_callback_cla(context):
    callback_element = context.callback_form.find_element_by_xpath(f'//input[@value="call"]')
    assert callback_element is not None
    callback_element.click()
    assert callback_element.get_attribute("value") == "call"


@given(u'click "Submit details"')
def step_submit_form(context):
    element = context.callback_form.find_element_by_id("submit-button")
    assert element is not None
    element.click()


@then(u'I should be taken to the "{title}" page')
def step_confirmation_page(context, title):
    wait_until_page_is_loaded("/result/confirmation", context)
    assert_header_on_page(title, context)


@then(u'I should shown the CLA number')
def step_check_cla_number(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(".laa-confirmation-inset")
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith(f"You can now call CLA on {CLA_NUMBER}.")


@then(u'I should see my reference number after the text "Your reference number is"')
def step_impl(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(".govuk-panel__body")
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith("Your reference number is")
    case_reference = confirmation_text_element.find_element_by_tag_name("strong").text
    assert case_reference is not None, "Could not find case reference number"
    context.case_reference = case_reference


@then(u'A matching case should be created on the CHS')
def step_matching_case_on_chs(context):
    case = context.helperfunc.get_case_from_backend(context.case_reference)
    personal_details = context.helperfunc.get_case_personal_details_from_backend(context.case_reference)
    assert case["source"] == "WEB"
    for key, value in context.form_values.items():
        assert personal_details[key] == value
