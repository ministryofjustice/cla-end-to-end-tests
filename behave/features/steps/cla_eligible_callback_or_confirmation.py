from behave import *
from features.constants import (
    CLA_PUBLIC_URL,
    CLA_NUMBER,
    CLA_MEANS_TEST_PERSONAL_DETAILS_FORM,
    CLA_MEANS_TEST_CALL_BACK_NUMBER,
)
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def assert_form_input_element(callback_form, element_id, value):
    element = callback_form.find_element_by_id(element_id)
    assert element is not None
    element.send_keys(value)
    assert element.get_attribute("value") == value


@step("I enter my personal details")
def step_impl(context):
    personal_details_form = CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    context.form_values = {}
    for name, value in personal_details_form.items():
        context.form_values[name] = value["form_element_value"]
        assert_form_input_element(
            context.callback_form, value["form_element_id"], value["form_element_value"]
        )


@step("I select the contact option 'I’ll call CLA'")
def step_impl(context):
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    callback_element = context.callback_form.find_element_by_xpath(
        f'//input[@value="call"]'
    )
    assert callback_element is not None
    callback_element.click()
    assert callback_element.get_attribute("value") == "call"


@step("I should be shown the CLA number")
def step_impl(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(
        ".laa-confirmation-inset"
    )
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith(
        f"You can now call CLA on {CLA_NUMBER}."
    )


@step('I should see my reference number after the text "Your reference number is"')
def step_impl(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(
        ".govuk-panel__body"
    )
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith("Your reference number is")
    case_reference = confirmation_text_element.find_element_by_tag_name("strong").text
    assert case_reference is not None, "Could not find case reference number"
    context.case_reference = case_reference


@step("A matching case should be created on the CHS")
def step_impl(context):
    case = context.helperfunc.get_case_from_backend(context.case_reference)
    personal_details = context.helperfunc.get_case_personal_details_from_backend(
        context.case_reference
    )
    assert case["source"] == "WEB"
    for key, value in context.form_values.items():
        assert personal_details[key] == value


@step('I select "Call me back"')
def step_impl(context):
    call_me_back_element = context.callback_form.find_element_by_xpath(
        f'//input[@value="callback"]'
    )
    assert call_me_back_element is not None
    call_me_back_element.click()
    assert call_me_back_element.get_attribute("value") == "callback"


@step("I enter my phone number for the callback")
def step_impl(context):
    # context.form_values should already be created in previous step
    call_back_number = CLA_MEANS_TEST_CALL_BACK_NUMBER["mobile_phone"]
    context.form_values["mobile_phone"] = call_back_number["form_element_value"]
    assert_form_input_element(
        context.callback_form,
        call_back_number["form_element_id"],
        call_back_number["form_element_value"],
    )


@step('I select "Call on another day"')
def step_impl(context):
    call_another_day = context.callback_form.find_element_by_xpath(
        f'//input[@value="specific_day"]'
    )
    assert call_another_day is not None
    call_another_day.click()
    assert call_another_day.get_attribute("value") == "specific_day"


@step("I select an available day and time")
def step_impl(context):
    choose_day = Select(
        context.callback_form.find_element_by_xpath(
            f'//select[@id="callback-time-day"]'
        )
    )
    assert choose_day is not None
    choose_time_in_day = Select(
        context.callback_form.find_element_by_xpath(
            f'//select[@id="callback-time-time_in_day"]'
        )
    )
    assert choose_time_in_day is not None
    if len(choose_day.options) > 0:
        choose_day.select_by_index(0)
        # once you choose this it will re-populate times drop down now choose the first time
        if len(choose_time_in_day.options) > 0:
            choose_time_in_day.select_by_index(1)
        else:
            raise AssertionError("No option to call me back at a chosen time")
    else:
        raise AssertionError("No option to call me back another day")


@step('I should NOT see the text "You can now call CLA on 0345 345 4 345"')
def step_impl(context):
    # check to see if the incorrect text element is present, if it isn't then we can carry on
    try:
        confirmation_text_element = (
            context.helperfunc.driver().find_element_by_css_selector(
                ".laa-confirmation-inset"
            )
        )
        if confirmation_text_element is not None:
            assert confirmation_text_element.text.startswith(
                f"You can now call CLA on {CLA_NUMBER}."
            )
            raise AssertionError(f"Incorrect confirmation message showing")
    except NoSuchElementException as ex:
        # the element can't be found and we are ok
        pass


@step("The callback should have been created on the CHS")
def step_impl(context):
    case_callback = context.helperfunc.get_case_callback_details_from_backend(
        context.case_reference
    )

    if len(case_callback) > 0:
        # look at latest callback
        assert case_callback[0]["created_by"] == "web"
        # check the code in the call_back log
        # ok to assume this is the latest in the log?
        assert case_callback[0]["code"] == "CB1", "Callback not created"
    else:
        raise AssertionError("No callbacks for this case")
