from behave import *
from features.constants import CLA_PUBLIC_URL, CLA_NUMBER, CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
from features.steps.cla_in_scope import assert_header_on_page, wait_until_page_is_loaded
from features.steps.cla_eligible_confirmation import assert_form_input_element
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

@given(u'I select "Call me back"')
def step_receive_callback_from_cla(context):
    call_me_back_element = context.callback_form.find_element_by_xpath(f'//input[@value="callback"]')
    assert call_me_back_element is not None
    call_me_back_element.click()
    assert call_me_back_element.get_attribute("value") == "callback"

@given(u'I enter my phone number for the callback')
def step_enter_phone_number(context):
    # personal_details_form = CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
    # TODO will just put phone number in for now and then put in constants later
    # context.form_values and context.callback_form should already be created in previous step
    context.form_values["mobile_phone"] = "020 1234 67890"
    assert_form_input_element(context.callback_form, "callback-contact_number", "020 1234 67890")

@given(u'I select "Call on another day"')
def step_choose_call_another_day(context):
    call_another_day = context.callback_form.find_element_by_xpath(f'//input[@value="specific_day"]')
    assert call_another_day is not None
    call_another_day.click()
    assert call_another_day.get_attribute("value") == "specific_day"

@given(u'I select an available day and time')
def step_choose_available_day_and_time(context):
    choose_day = Select(context.callback_form.find_element_by_xpath(f'//select[@id="callback-time-day"]'))
    assert choose_day is not None
    choose_time_in_day = Select(context.callback_form.find_element_by_xpath(f'//select[@id="callback-time-time_in_day"]'))
    assert choose_time_in_day is not None   
    # 'data-day-time-choices' nested dictionary {'day'{'start_time':{'time range'}}
    # TODO decide if want to check these in DB
    if len(choose_day.options) > 0:
        choose_day.select_by_index(0)
        # remember the day you chose so can check in cla_backend case
        # context.form_values["day"] = choose_day.first_selected_option.text
        # once you choose this it will re-populate times drop down now choose the first time
        if len(choose_time_in_day.options) > 0:
            choose_time_in_day.select_by_index(1)
            # context.form_values["time"] = choose_time_in_day.first_selected_option.text
        else:
            raise AssertionError("No option to call me back at a chosen time")
    else:
        raise AssertionError ("No option to call me back another day")
        
@then(u'I should NOT see the text "You can now call CLA on 0345 345 4 345"')
def step_call_now_text_not_visible(context):
    # check to see if the incorrect text element is present, if it isn't then we can carry on
    try:
        confirmation_text_element = context.helperfunc.driver().find_element_by_css_selector(".laa-confirmation-inset")
        if confirmation_text_element is not None:
            assert confirmation_text_element.text.startswith(f"You can now call CLA on {CLA_NUMBER}.")
            raise AssertionError(f"Incorrect confirmation message showing")   
    except NoSuchElementException as ex:
        # the element can't be found and we are ok
        pass
