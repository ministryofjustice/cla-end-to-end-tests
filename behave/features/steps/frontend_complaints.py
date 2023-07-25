from behave import step
from common_steps import click_on_hyperlink_and_get_href


@step("I am on the '{tab}' tab on the dashboard")
def step_impl_complaints_tab(context, tab):
    click_on_hyperlink_and_get_href(context, tab)


@step("There are cases available")
def step_impl_complaints_cases(context):
    assert (
        context.helperfunc.find_by_xpath(
            "//table[contains(@class,'ListTable ng-scope')]/tbody/tr"
        )
        is not None
    ), "No Complaint Cases Available"


@step("When I search for '{complaint_num}'")
def step_impl_complaints_search(context, complaint_num):
    context.helperfunc.find_by_id("case-search").sendKeys(complaint_num)
    context.helperfunc.find_by_xpath(
        "//input[contains(@class,CaseSearch-submit)]"
    ).click()


@step("The complaint i search for is available")
def step_impl_complaint_check(context):
    assert (
        context.helperfunc.find_by_xpath(
            "//tr[contains(@ng-class,statusClass(complaint))"
        )
        is not None
    ), "Complaint not found"


@step("I select the complaint '{complaint_num}'")
def step_impl_complaint_select(context, complaint_num):
    context.helperfunc.find_by_link_text(complaint_num).click()


@step("I am on the complaint '{complaint_num}'")
def step_impl_complaint_open(context, complaint_num):
    assert (
        context.helperfunc.find_by_link_text(complaint_num) is not None
    ), "Not on the complaints page"


@step("The complaint i search for is not available")
def step_impl_complaint_fail(context):
    assert (
        context.helperfunc.find_by_xpath(
            "//div[contains(@class,Notice ng-scope)]"
        ).getText()
        == "There are no complaints"
    ), "There are complaints found"
