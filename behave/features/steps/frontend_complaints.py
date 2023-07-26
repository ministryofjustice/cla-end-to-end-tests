from behave import step
from common_steps import click_on_hyperlink_and_get_href, assert_header_on_page


@step("I am on the '{tab}' tab on the dashboard")
def step_impl_complaints_tab(context, tab):
    click_on_hyperlink_and_get_href(context, tab)


@step("There are complaints available")
def step_impl_complaints_cases(context):
    assert (
        context.helperfunc.find_by_xpath(
            "//table[contains(@class,'ListTable ng-scope')]/tbody/tr"
        )
        is not None
    ), "No Complaint Cases Available"


@step("I search for '{complaint_text}'")
def step_impl_complaints_search(context, complaint_text):
    context.helperfunc.find_by_id("case-search").send_keys(complaint_text)
    context.helperfunc.find_by_xpath(
        "//input[contains(@class,CaseSearch-submit)]"
    ).click()


@step("I can select the complaint '{complaint_num}'")
def step_impl_complaint_select(context, complaint_num):
    assert (
        context.helperfunc.find_by_link_text(complaint_num) is not None
    ), "Complaint not found"
    context.helperfunc.find_by_link_text(complaint_num).click()


@step("I am on the complaint '{complaint_num}' detail page")
def step_impl_complaint_open(context, complaint_num):
    # <h1 class="ng-binding">Complaint details</h1>
    assert_header_on_page("Complaint details", context)
    assert (
        context.helperfunc.find_by_link_text(complaint_num) is not None
    ), "Not on the complaints page"


@step("there are no complaints returned")
def step_impl_complaint_fail(context):
    assert (
        context.helperfunc.find_by_xpath(
            "//div[contains(@class,'Notice ng-scope')]"
        ).getText()
        == "There are no complaints"
    ), "Complaints are available"
