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
