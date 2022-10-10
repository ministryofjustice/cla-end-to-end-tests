from behave import step
from features.constants import CLA_PUBLIC_URL
from features.steps.common_steps import (
    assert_header_on_page,
    wait_until_page_is_loaded,
    remove_prefix,
)


@step("I have passed the means test")
def step_impl(context):
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
def step_impl(context):
    start_page_url = f"{CLA_PUBLIC_URL}"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Check if you can get legal aid", context)
    start_button = context.helperfunc.find_by_id("start")
    assert start_button is not None
    assert start_button.text == "Start now"
    start_button.click()


@step("I select the category <category>")
def step_impl(context):
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
def step_impl(context):
    check_if_you_qualify_link = context.helperfunc.find_by_xpath('//a[@href="/about"]')
    assert check_if_you_qualify_link is not None
    check_if_you_qualify_link.click()


@step("I <answer> the <question>")
def step_impl(context):
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
def step_impl(context):
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
def step_impl(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )
