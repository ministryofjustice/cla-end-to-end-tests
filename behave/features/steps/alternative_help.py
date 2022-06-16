from behave import *
from features.constants import CLA_FRONTEND_URL, CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
from selenium.webdriver.common.by import By


@then(u'I complete the users details with \'Test Dummy User\' details')
def step_impl(context):
    context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
    context.execute_steps(u'''
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    ''')


@then(u'I navigate the call centre dashboard')
def step_impl(context):
    url = f"{CLA_FRONTEND_URL}/call_centre/"
    context.helperfunc.open(url)


@then(u'I go back to the previous case')
def step_impl(context):
    assert context.case_reference, "Context is missing case reference"
    url = f"{CLA_FRONTEND_URL}/call_centre/{context.case_reference}/diagnosis/"
    context.helperfunc.open(url)


@then(u'I should see the users previously entered details')
def step_impl(context):
    context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
    context.execute_steps(u'''
        Then I will see the users details
    ''')


@when(u'I select \'Assign Alternative Help\'')
def step_impl(context):
    # for some reason these seem to return stale element errors
    # use the wrapper function
    x_path = f".//a[@title='Assign alternative help']"
    context.helperfunc.click_button(By.XPATH, x_path)

