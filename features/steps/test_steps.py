import re
from behave import *


@given(u'that I am logged in')
def step_impl(context):

    config = context.config.userdata
    login_url = f"{config['cla_frontend_url']}/auth/login/"
    context.helperfunc.open(login_url)
    form = context.helperfunc.find_by_name('login_frm')
    assert form is not None
    form.find_element_by_name("username").send_keys(config["cla_frontend_operator_username"])
    form.find_element_by_name("password").send_keys(config["cla_frontend_operator_password"])
    form.find_element_by_name("login-submit").click()

    element = context.helperfunc.find_by_xpath("//html[@ng-app='cla.operatorApp']")
    assert element is not None


@given(u'that I am on the \'call centre dashboard\' page.')
def step_impl(context):
    current_path = context.helperfunc.get_current_path()
    assert current_path == "/call_centre/"


@when(u'I select to \'Create a case\'.')
def step_impl(context):
    context.helperfunc.find_by_id("create_case").click()


@then(u'I am taken to the \'case details\' page.')
def step_impl(context):
    assert context.helperfunc.find_by_xpath("//header/h1").text == "Case details"
    current_path = context.helperfunc.get_current_path()
    assert re.match(r"^/call_centre/\w{2}-\d{4}-\d{4}/diagnosis/$", current_path)


@then(u'I select \'Create new user\'.')
def step_impl(context):
    btn = context.helperfunc.find_by_name("create-newuser")
    assert btn is not None
    btn.click()
    form = context.helperfunc.find_by_name("personaldetails_frm")
    assert form.is_displayed()


@then(u'enter the client\'s personal details.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then enter the client\'s personal details.')


@then(u'I click the save button on the screen.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I click the save button on the screen.')


@then(u'I will see the users details.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I will see the users details.')