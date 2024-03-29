from behave import step
from helper.constants import (
    CLA_NUMBER,
    CLA_MEANS_TEST_PERSONAL_DETAILS_FORM,
    CLA_MEANS_TEST_CALL_BACK_NUMBER,
    CLA_PUBLIC_URL,
)
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from features.steps.common_steps import (
    assert_header_on_page,
    wait_until_page_is_loaded,
    remove_prefix,
)


def assert_form_input_element(callback_form, element_id, value):
    element = callback_form.find_element_by_id(element_id)
    assert element is not None
    element.send_keys(value)
    assert element.get_attribute("value") == value


@step("I enter my personal details")
def step_impl_enter_details(context):
    personal_details_form = CLA_MEANS_TEST_PERSONAL_DETAILS_FORM
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    context.form_values = {}
    for name, value in personal_details_form.items():
        context.form_values[name] = value["form_element_value"]
        assert_form_input_element(
            context.callback_form, value["form_element_id"], value["form_element_value"]
        )


@step("I should be shown the CLA number")
def step_impl_cla_number_shown(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(
        ".laa-confirmation-inset"
    )
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith(
        f"You can now call CLA on {CLA_NUMBER}."
    )


@step('I should see my reference number after the text "Your reference number is"')
def step_impl_reference_number(context):
    confirmation_text_element = context.helperfunc.find_by_css_selector(
        ".govuk-panel__body"
    )
    assert confirmation_text_element is not None
    assert confirmation_text_element.text.startswith("Your reference number is")
    case_reference = confirmation_text_element.find_element_by_tag_name("strong").text
    assert case_reference is not None, "Could not find case reference number"
    context.case_reference = case_reference


@step("A matching case should be created on the CHS")
def step_impl_case_created_on_chs(context):
    case = context.helperfunc.get_case_from_backend(context.case_reference)
    personal_details = context.helperfunc.get_case_personal_details_from_backend(
        context.case_reference
    )
    assert case["source"] == "WEB"
    for key, value in context.form_values.items():
        assert personal_details[key] == value


@step('I select "Call me back"')
def step_impl_select_call_me_back(context):
    call_me_back_element = context.callback_form.find_element_by_xpath(
        '//input[@value="callback"]'
    )
    assert call_me_back_element is not None
    call_me_back_element.click()
    assert call_me_back_element.get_attribute("value") == "callback"


@step("I enter my phone number for the callback")
def step_impl_enter_phone_number(context):
    # context.form_values should already be created in previous step
    call_back_number = CLA_MEANS_TEST_CALL_BACK_NUMBER["mobile_phone"]
    context.form_values["mobile_phone"] = call_back_number["form_element_value"]
    assert_form_input_element(
        context.callback_form,
        call_back_number["form_element_id"],
        call_back_number["form_element_value"],
    )


@step('I select "Call on another day"')
def step_impl_call_another_day(context):
    call_another_day = context.callback_form.find_element_by_xpath(
        '//input[@value="specific_day"]'
    )
    assert call_another_day is not None
    call_another_day.click()
    assert call_another_day.get_attribute("value") == "specific_day"


@step("I select an available day and time")
def step_impl_select_available_day(context):
    choose_day = Select(
        context.callback_form.find_element_by_xpath('//select[@id="callback-time-day"]')
    )
    assert choose_day is not None
    choose_time_in_day = Select(
        context.callback_form.find_element_by_xpath(
            '//select[@id="callback-time-time_in_day"]'
        )
    )
    assert choose_time_in_day is not None
    if len(choose_day.options) > 0:
        choose_day.select_by_index(1)
        # once you choose this it will re-populate times drop-down.
        # Now choose the first time
        if len(choose_time_in_day.options) > 0:
            choose_time_in_day.select_by_index(1)
        else:
            raise AssertionError("No option to call me back at a chosen time")
    else:
        raise AssertionError("No option to call me back another day")


@step('I select an available "{option}" call time')
def step_impl_select_available_callback_time(context, option):
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    choose_callback_time = Select(
        context.callback_form.find_element_by_xpath(
            f'//select[@id="{option}-time-time_today"]'
        )
    )

    assert choose_callback_time is not None
    if len(choose_callback_time.options) > 0:
        choose_callback_time.select_by_index(1)
    else:
        raise AssertionError("No option to callback time")


@step('I should NOT see the text "You can now call CLA on 0345 345 4 345"')
def step_impl_cla_number_not_shown(context):
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
            raise AssertionError("Incorrect confirmation message showing")
    except NoSuchElementException:
        # the element can't be found and we are ok
        pass


@step("The callback should have been created on the CHS")
def step_impl_callback_created(context):
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


@step("I have passed the means test")
def step_impl_passed_means_test(context):
    # The next steps are the steps that pass the means test
    context.execute_steps(
        """
        Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
        When I select the category <category>
            | category                  |
            | Education                 |
            | Special educational needs |
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
        """
    )


@step("I have selected the start now button on the start page")
def step_impl_select_start_button(context):
    start_page_url = f"{CLA_PUBLIC_URL}"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Check if you can get legal aid", context)
    start_button = context.helperfunc.find_by_id("start")
    assert start_button is not None
    assert start_button.text == "Start now"
    start_button.click()


@step("I select the category <category>")
def step_impl_select_category(context):
    next_page_path = None
    for row in context.table:
        if next_page_path is not None:
            wait_until_page_is_loaded(next_page_path, context)
        category_link = context.helperfunc.find_by_xpath(
            f'//a[@title="{row["category"]}"]'
        )
        next_page_path = category_link.get_attribute("pathname")
        assert category_link is not None
        category_link.click()


@step("I click on the 'Check if you qualify financially' button")
def step_impl_select_financial_check(context):
    check_if_you_qualify_link = context.helperfunc.find_by_xpath('//a[@href="/about"]')
    assert check_if_you_qualify_link is not None
    check_if_you_qualify_link.click()


@step("I <answer> the <question>")
def step_impl_answer_question(context):
    # answer tells me if I say yes or no
    # question helps me find the radio buttons
    for row in context.table:
        value = row["question"]
        question_fieldset = context.helperfunc.find_by_xpath(
            f"//*[contains(text(),'{row['question']}')]"
        )
        question_field_id = question_fieldset.get_attribute("id")
        question_input_id_start = remove_prefix(question_field_id, "field-label-")
        if row["answer"] == "No" or row["answer"] == "Yes":
            if row["answer"] == "No":
                question_id = question_input_id_start + "-1"
            else:
                question_id = question_input_id_start + "-0"
            question_radio = context.helperfunc.driver().find_element_by_xpath(
                f"//input[@id='{question_id}']"
            )
            assert question_radio is not None, f"Could not find: {value}"
            question_radio.click()
            # check that the input is selected
            assert question_radio.get_attribute("checked") == "true"
        else:
            # textbox answer rather than radio buttons
            question_id = question_input_id_start
            question_box = context.helperfunc.driver().find_element_by_xpath(
                f"//input[@id='{question_id}']"
            )
            assert question_box is not None, f"Could not find: {value}"
            # type in the text
            question_box.send_keys(row["answer"])


@step("I select 'Universal Credit' from the list of benefits")
def step_impl_select_universal_credit(context):
    # check value of universal_credit checkbox
    check_box_universal_credit = context.helperfunc.driver().find_element_by_id(
        "benefits-4"
    )
    assert check_box_universal_credit is not None
    # click on universal credit
    check_box_universal_credit.click()
    # now check universal credit is checked
    assert check_box_universal_credit.get_attribute("checked") == "true"


@step("I click Confirm")
def step_impl_click_confirm(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )
