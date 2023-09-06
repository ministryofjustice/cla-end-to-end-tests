from behave import step
from features.steps.common_steps import (
    assert_element_does_not_appear,
    assert_header_on_page,
)
from helper.constants import CLA_SPECIALIST_CASE_TO_EDIT


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
    assert (
        context.helperfunc.get_current_path()
        == f"/provider/case/{CLA_SPECIALIST_CASE_TO_EDIT}/legal_help_form/"
    )
    assert_header_on_page("Legal Help", context)


@step("<question> is visible with value <answer> in the form")
def step_impl_under_eighteen_table_and_values_checks(context):
    for row in context.table:
        question = row["question"]
        answer = row["answer"]
        # Yes or no is visible as a value in the input field on the Legal Help Form.
        # Find header to ensure finances is visible
        context.legal_help_form = context.helperfunc.find_by_xpath(
            "//h2[contains(text(), 'Your Finances')]"
        )

        # Find the question of the table row.
        table_title = f"//../table/tbody/tr/td[contains(text(), '{question}')]"
        context.legal_help_form.find_element_by_xpath(table_title)
        assert table_title is not None

        # Check input value of the question
        input_value = context.legal_help_form.find_element_by_xpath(
            table_title + "/../td/input"
        )
        assert input_value.get_attribute("value") == answer
