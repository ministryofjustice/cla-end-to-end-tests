from behave import *
from features.constants import CLA_PUBLIC_URL, CLA_NUMBER, CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
from features.steps.cla_in_scope import assert_header_on_page, wait_until_page_is_loaded
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# TODO this is the same as on eligible_contact so can remove once that has been merged
def assert_form_input_element(callback_form, element_id, value):
    element = callback_form.find_element_by_id(element_id)
    assert element is not None
    element.send_keys(value)
    assert element.get_attribute('value') == value

# TODO this is the same as on eligible_contact so can remove once that has been merged
@given(u'I have passed the means test')
def step_means_test_page(context):
    # The next steps are the steps that pass the means test
   context.execute_steps(u'''
        Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
        When I select the category Education
        And the category Special Educational needs
        Then I am taken to the "Legal aid is available for this type of problem" page located on "/legal-aid-available"
        And I click on the 'Check if you qualify financially' button 
        And I am taken to the "About you" page located on "/about"
        And I <answer> the <question> 
            | question                                                   | answer |
            | Do you have a partner?                                     | No     |
            | Do you receive any benefits (including Child Benefit)?     | Yes    |
            | Do you have any children aged 15 or under?                 | No     |
            | Do you have any dependants aged 16 or over?                | No     |
            | Do you own any property?                                   | No     |
            | Are you employed?                                          | No     |
            | Are you self-employed?                                     | No     |
            | Are you or your partner (if you have one) aged 60 or over? | No     |
            | Do you have any savings or investments?                    | No     |
            | Do you have any valuable items worth over £500 each?       | No     |
        # All steps that are clicking continue written in identical format so can reuse code
        And I click continue
        And I am taken to the "Which benefits do you receive?" page located on "/benefits"
        And I select 'Universal Credit' from the list of benefits
        And I click continue 
        And I am taken to the "Review your answers" page located on "/review"
        # this is actually click confirm
        And I click continue
        Then I am taken to the "Contact Civil Legal Advice" page located on "/result/eligible"
        ''')

# TODO this is the same as on eligible_contact so can remove once that has been merged
@given(u'I enter my personal details')
def step_enter_personal_details(context):
    personal_details_form = CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    context.form_values = {}
    for name, value,  in personal_details_form.items():
        context.form_values[name] = value['form_element_value']
        assert_form_input_element(context.callback_form, value['form_element_id'], value['form_element_value'])

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
    #TODO do we check the date and time? they are stored in case under 'requires_action_at' and 'callback_time_string'
    case = context.helperfunc.get_case_from_backend(context.case_reference)
    personal_details = context.helperfunc.get_case_personal_details_from_backend(context.case_reference)
    assert case["source"] == "WEB"
    for key, value in context.form_values.items():
        assert personal_details[key] == value
        