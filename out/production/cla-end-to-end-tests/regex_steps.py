from behave import step, use_step_matcher

use_step_matcher("re")

# This file uses step matcher Regex. By using Regex we can create optional parameters and more.
# Regex pythons need to be separate in order to prevent parsing conflicts, which is Behaves default.


@step("I am (?P<optional>not )?on universal credit benefits")
def step_impluniversal_credit(context, optional):
    state = "true"
    if optional:
        state = "false"

    radio_input = context.helperfunc.find_by_css_selector(
        f"input[name='your_details-specific_benefits-universal_credit'][value='{state}']"
    )
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


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
    state = "true"
    if optional:
        state = "false"
    radio_input = context.helperfunc.find_by_css_selector(
        f"input[name='your_details-has_partner'][value='{state}']"
    )
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


@step("I am (?P<optional>not )?aged 60 or over")
def step_impl_over_sixty(context, optional):
    state = "true"
    if optional:
        state = "false"
    radio_input = context.helperfunc.find_by_xpath(
        f"//input[@name='your_details-older_than_sixty'][@value='{state}']"
    )
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


@step(
    "I am given a message 'The means test has been saved. The current result is (?P<optional>not )?eligible "
    "for Legal Aid'"
)
def step_impl_means_test_result(context, optional):
    element = context.helperfunc.find_by_css_selector(
        ".Notice.Notice--closeable.success"
    )
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
