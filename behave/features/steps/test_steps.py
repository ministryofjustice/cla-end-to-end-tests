import re
from features.constants import CLA_FRONTEND_PERSONAL_DETAILS_FORM
from selenium.webdriver.support.ui import Select, WebDriverWait
from behave import step, then
from selenium.webdriver.common.by import By


@step("I am on the 'call centre dashboard' page")
def step_impl_call_center_dashboard(context):
    def wait_for_dashboard(*args):
        return context.helperfunc.find_by_css_selector("body.v-Dashboard") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_dashboard, "Could not find dashboard")

    current_path = context.helperfunc.get_current_path()
    assert (
        current_path == "/call_centre/"
    ), f"Current path is {current_path}. Expected /call_centre/"


@step("I select to 'Create a case'")
def step_impl_create_case(context):
    # wrap click() to avoid StaleElementException
    context.helperfunc.click_button(By.ID, "create_case")
    context.case_reference = context.helperfunc.find_by_css_selector(
        "h1.CaseBar-caseNum a"
    ).text


@step("I am taken to the 'case details' page")
def step_impl_case_details(context):
    assert context.helperfunc.find_by_xpath("//header/h1").text == "Case details"
    current_path = context.helperfunc.get_current_path()
    assert re.match(r"^/call_centre/\w{2}-\d{4}-\d{4}/diagnosis/$", current_path)


@step("I select 'Create new user'")
def step_impl_create_user(context):
    btn = context.helperfunc.find_by_name("create-newuser")
    assert btn is not None
    btn.click()
    form = context.helperfunc.find_by_name("personaldetails_frm")
    assert form.is_displayed()


@step("enter the client's personal details")
def step_impl_enter_details(context):
    if not hasattr(context, "personal_details_form"):
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    for name, value in context.personal_details_form.items():
        element = context.helperfunc.find_by_name(name)
        assert element is not None
        if element.tag_name == "select":
            select_element = Select(element)
            select_element.select_by_visible_text(value)
        else:
            element.send_keys(value)


@step("I click the save button on the screen")
def step_impl_click_save_button(context):
    form = context.helperfunc.find_by_name("personaldetails_frm")
    btn = context.helperfunc.find_by_name("save-personal-details")
    assert btn is not None
    btn.click()

    def wait_until_personal_details_are_saved(*args):
        return not form.is_displayed()

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_personal_details_are_saved)


@then("I will see the users details")
def step_impl_user_details(context):
    personal_details = context.helperfunc.find_by_id("personal_details").text
    for name, value in context.personal_details_form.items():
        assert value in personal_details
