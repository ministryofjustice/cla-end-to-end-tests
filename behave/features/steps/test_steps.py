import re
from features.constants import CLA_FRONTEND_PERSONAL_DETAILS_FORM, CLA_FRONTEND_URL
from selenium.webdriver.support.ui import Select, WebDriverWait
from behave import *
from selenium.webdriver.common.by import By


@given(u'that I am logged in')
def step_impl(context):
    config = context.config.userdata
    login_url = f"{CLA_FRONTEND_URL}/auth/login/"
    context.helperfunc.open(login_url)
    form = context.helperfunc.find_by_name('login_frm')
    assert form is not None
    form.find_element_by_name("username").send_keys(config["cla_frontend_operator_username"])
    form.find_element_by_name("password").send_keys(config["cla_frontend_operator_password"])
    form.find_element_by_name("login-submit").click()

    element = context.helperfunc.find_by_xpath("//html[@ng-app='cla.operatorApp']")
    assert element is not None


@step(u'that I am on the \'call centre dashboard\' page')
def step_impl(context):
    current_path = context.helperfunc.get_current_path()
    assert current_path == "/call_centre/"


@step(u'I select to \'Create a case\'')
def step_impl(context):
    # wrap click() to avoid StaleElementException
    context.helperfunc.click_button(By.ID, "create_case")
    context.case_reference = context.helperfunc.find_by_css_selector('h1.CaseBar-caseNum a').text


@step(u'I am taken to the \'case details\' page')
def step_impl(context):
    assert context.helperfunc.find_by_xpath("//header/h1").text == "Case details"
    current_path = context.helperfunc.get_current_path()
    assert re.match(r"^/call_centre/\w{2}-\d{4}-\d{4}/diagnosis/$", current_path)


@step(u'I select \'Create new user\'')
def step_impl(context):
    btn = context.helperfunc.find_by_name("create-newuser")
    assert btn is not None
    btn.click()
    form = context.helperfunc.find_by_name("personaldetails_frm")
    assert form.is_displayed()


@step(u'enter the client\'s personal details')
def step_impl(context):
    if not hasattr(context, 'personal_details_form'):
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    for name, value in context.personal_details_form.items():
        element = context.helperfunc.find_by_name(name)
        assert element is not None
        if element.tag_name == 'select':
            select_element = Select(element)
            select_element.select_by_visible_text(value)
        else:
            element.send_keys(value)


@step(u'I click the save button on the screen')
def step_impl(context):
    form = context.helperfunc.find_by_name("personaldetails_frm")
    btn = context.helperfunc.find_by_name("save-personal-details")
    assert btn is not None
    btn.click()

    def wait_until_personal_details_are_saved(*args):
        return not form.is_displayed()
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_personal_details_are_saved)


@then(u'I will see the users details')
def step_impl(context):
    personal_details = context.helperfunc.find_by_id("personal_details").text
    for name, value in context.personal_details_form.items():
        assert value in personal_details
