from behave import *
from features.constants import CLA_FRONTEND_URL, CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
from selenium.webdriver.common.by import By
from common_steps import click_on_hyperlink, switch_to_new_tab


@step(u'I complete the users details with \'Test Dummy User\' details')
def step_impl(context):
    context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
    context.execute_steps(u'''
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    ''')


@step(u'I navigate back to the call centre dashboard')
def step_impl(context):
    url = f"{CLA_FRONTEND_URL}/call_centre/"
    context.helperfunc.open(url)


@step(u'I go back to the previous case')
def step_impl(context):
    assert context.case_reference, "Context is missing case reference"
    url = f"{CLA_FRONTEND_URL}/call_centre/{context.case_reference}/diagnosis/"
    context.helperfunc.open(url)


@step(u'I see the users previously entered details')
def step_impl(context):
    context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP
    context.execute_steps(u'''
        Then I will see the users details
    ''')


@step(u'I select \'Assign Alternative Help\'')
def step_impl(context):
    # no hyperlink text as it is just a gif
    x_path = f".//a[@title='Assign alternative help']"
    context.helperfunc.click_button(By.XPATH, x_path)


@step(u'I select "{face_to_face_text}" and I am taken to a new tab displaying FALA')
def step_impl(context, face_to_face_text):
    context.old_tabs = context.helperfunc.driver().window_handles
    last_hyperlink_selected = click_on_hyperlink(context, face_to_face_text)
    new_tabs = context.helperfunc.driver().window_handles
    for tab in new_tabs:
        if tab in context.old_tabs:
            pass
        else:
            new_tab = tab
    switch_to_new_tab(context, new_tab, last_hyperlink_selected)
    context.helperfunc.driver().switch_to.window(new_tab)
    # check the url
    assert last_hyperlink_selected == context.helperfunc.driver().current_url

