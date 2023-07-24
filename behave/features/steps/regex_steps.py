from behave import step, use_step_matcher
from features.steps.common_steps import (
    green_checkmark_appears_on_tab,
    assert_select_radio_button,
    assert_element_does_not_appear,
)

use_step_matcher("re")

# This file uses step matcher Regex. By using Regex we can create optional parameters and more.
# Regex pythons need to be separate in order to prevent parsing conflicts, which is Behaves default.


@step("I am (?P<optional>not )?on universal credit benefits")
def step_impl_universal_credit(context, optional):
    assert_select_radio_button(
        context, optional, "your_details-specific_benefits-universal_credit"
    )


@step("I am (?P<optional>not )?self employed")
def step_impl_self_employed(context, optional):
    state = "1"
    if optional:
        state = "0"
    radio_input = context.helperfunc.find_by_css_selector(
        f"input[name='id_your_income-self_employed'][value='{state}']"
    )
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


@step("I do (?P<optional>not )?have a partner")
def step_impl_has_partner(context, optional):
    assert_select_radio_button(context, optional, "your_details-has_partner")


@step("I am (?P<optional>not )?aged 60 or over")
def step_impl_over_sixty(context, optional):
    assert_select_radio_button(context, optional, "your_details-older_than_sixty")


@step("I am (?P<optional>not )?aged 17 or under")
def step_impl_under_eighteen(context, optional):
    assert_select_radio_button(context, optional, "your_details-is_you_under_18")


@step("I do (?P<optional>not )?receive money on a regular basis")
def step_impl_receive_money_regularly(context, optional):
    assert_select_radio_button(
        context, optional, "your_details-under_18_receive_regular_payment"
    )


@step(
    "I do (?P<optional>not )?have savings, items of value or investments totalling £2500 or more?"
)
def step_impl_have_savings_items_over_two_thousand_five_hundred(context, optional):
    assert_select_radio_button(context, optional, "your_details-under_18_has_valuables")


@step("I can not answer the following 17 or under questions")
def step_impl_under_18_no_follow_up_questions_fail(context):
    assert_element_does_not_appear(context, "your_details-under_18_has_valuables")
    assert_element_does_not_appear(
        context, "your_details-under_18_receive_regular_payment"
    )


@step("the do you have valuables totalling £2500 or more question does not appear")
def step_impl_valuables_question_does_not_appear(context):
    assert_element_does_not_appear(context, "your_details-under_18_has_valuables")


@step(
    "I am given a message 'The means test has been saved. The current result is (?P<optional>not )?eligible "
    "for Legal Aid'"
)
def step_impl_means_test_result(context, optional):
    element = context.helperfunc.find_by_css_selector(
        ".Notice.Notice--closeable.success"
    )
    context.helperfunc.scroll_to_top()
    if optional:
        assert (
            element.text
            == "The means test has been saved. The current result is not eligible for Legal Aid"
        )
    else:
        assert (
            element.text
            == "The means test has been saved. The current result is eligible for Legal Aid"
        )


@step("I select the '(?P<optional>.*?)' button in the pop-up")
def step_impl_popup_button(context, optional):
    modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    modal.find_element_by_xpath("//button[@type='submit']").click()


@step("the green tick is (?P<optional>not )?present in the Finance tab")
def step_impl_green_tick_present(context, optional):
    classes = (
        context.helperfunc.find_by_css_selector("ul.Tabs")
        .find_element_by_link_text("Finances")
        .get_attribute("class")
    )
    if optional:
        # Checking that the green tick in the Finance Tab is not present.
        # make this function and refactor elsewhere
        assert green_checkmark_appears_on_tab(classes) is False
    else:
        # Checking that the green tick in the Finance Tab is present.
        assert green_checkmark_appears_on_tab(classes) is True
