from behave import step
from features.steps.common_steps import (
    assert_element_does_not_appear,
    assert_header_on_page,
    wait_until_page_is_loaded,
)
from helper.constants import CLA_SPECIALIST_CASE_TO_EDIT
from selenium.common.exceptions import NoSuchElementException


@step("the do you have valuables totalling £2500 or more question does not appear")
def step_impl_valuables_question_does_not_appear(context):
    assert_element_does_not_appear(context, "your_details-under_18_has_valuables")


@step("I can not answer the following 17 or under questions")
def step_impl_under_18_no_follow_up_questions_fail(context):
    assert_element_does_not_appear(context, "your_details-under_18_has_valuables")
    assert_element_does_not_appear(
        context, "your_details-under_18_receive_regular_payment"
    )


@step("I am taken to the cases Legal Help Form")
def step__on_legal_help_form(context):
    # Refresh the page as Legal Help Form holds old session data
    # and the page needs refreshing to bring in new changes (Selenium issue)
    context.helperfunc.refresh()
    legal_help_form_path = context.helperfunc.get_current_path()
    wait_until_page_is_loaded(legal_help_form_path, context)
    assert (
        legal_help_form_path
        == f"/provider/case/{CLA_SPECIALIST_CASE_TO_EDIT}/legal_help_form/"
    ), f"incorrect path, page path is {legal_help_form_path}"
    assert_header_on_page("Legal Help", context)


@step("<question> is visible with value <answer> in the form")
def step_impl_under_eighteen_table_and_values_checks(context):
    for row in context.table:
        question = row["question"]
        answer = row["answer"]

        # Find page wrapper to allow better xpath
        context.legal_help_form = context.helperfunc.find_by_xpath("//*[@id='wrapper']")

        # Yes or no is visible as a value in the input field on the Legal Help Form.
        # Find header to ensure finances is visible
        context.legal_help_form.find_element_by_xpath(
            "//h2[contains(text(), 'Your Finances')]"
        )

        # Find the question of the table row.
        table_title = f"//../table/tbody/tr/td[contains(text(), '{question}')]"
        context.legal_help_form.find_element_by_xpath(table_title)

        # Check input value of the question
        input_value = context.legal_help_form.find_element_by_xpath(
            table_title + "/../td/input"
        )
        assert (
            input_value.get_attribute("value") == answer
        ), f"{answer} was not found for {question}"


@step("<question> is not visible in the form")
def step_impl_under_eighteen_table_and_values_checks_not_visible(context):
    for row in context.table:
        question = row["question"]

        try:
            context.legal_help_form = context.helperfunc.find_by_xpath(
                "//h2[contains(text(), 'Your Finances')]"
            )
            context.legal_help_form.find_element_by_xpath(
                f"//../table/tbody/tr/td[contains(text(), '{question}')]"
            )
            return False
        except NoSuchElementException:
            # Return true as element could not be found
            return True
