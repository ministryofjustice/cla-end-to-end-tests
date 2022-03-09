from behave import *
from features.constants import CLA_PUBLIC_URL, CLA_NUMBER, CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
from features.steps.cla_in_scope import assert_header_on_page, wait_until_page_is_loaded


def assert_form_input_element(callback_form, element_id, value):
    # import pdb
    # pdb.set_trace()
    element = callback_form.find_element_by_id(element_id)
    assert element is not None
    element.send_keys(value)
    assert element.get_attribute('value') == value


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

@given(u'I enter my personal details')
def step_enter_personal_details(context):
    personal_details_form = CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    context.form_values = {}
    for name, value,  in personal_details_form.items():
        context.form_values[name] = value['form_element_value']
        assert_form_input_element(context.callback_form, value['form_element_id'], value['form_element_value'])

@given(u'I select the the callback option to callback CLA')
def step_select_callback_cla(context):
    callback_element = context.callback_form.find_element_by_xpath(f'//input[@value="call"]')
    assert callback_element is not None
    callback_element.click()
    assert callback_element.get_attribute("value") == "call"

@then(u'I should be shown the CLA number')
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
