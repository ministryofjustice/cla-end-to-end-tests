from behave import step
from features.constants import (
    CLA_FRONTEND_URL,
    CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP,
    CLA_FRONTEND_PERSONAL_DETAILS_FORM,
)
from selenium.webdriver.common.by import By
from common_steps import click_on_hyperlink_and_get_href, switch_to_new_tab


@step("I complete the users details with {user_choice:w} details")
def step_impl(context, user_choice):
    try:
        context.personal_details_form = (
            CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP[user_choice]
        )
    except KeyError:
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    context.execute_steps(
        """
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    """
    )


@step("I navigate back to the call centre dashboard")
def step_impl(context):
    url = f"{CLA_FRONTEND_URL}/call_centre/"
    context.helperfunc.open(url)


@step("I go back to the previous case")
def step_impl(context):
    assert context.case_reference, "Context is missing case reference"
    url = f"{CLA_FRONTEND_URL}/call_centre/{context.case_reference}/diagnosis/"
    context.helperfunc.open(url)


@step("I see the users previously entered {user_choice:w} details")
def step_impl(context, user_choice):
    try:
        context.personal_details_form = (
            CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP[user_choice]
        )
    except KeyError:
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    context.execute_steps(
        """
        Then I will see the users details
    """
    )


@step("I click on the Assign Alternative Help icon")
def step_impl(context):
    # no hyperlink text as it is just an icon in top RH corner
    x_path = ".//a[@title='Assign alternative help']"
    context.helperfunc.click_button(By.XPATH, x_path)


@step('I select "{face_to_face_text}" and I am taken to a new tab displaying FALA')
def step_impl(context, face_to_face_text):
    context.old_tabs = context.helperfunc.driver().window_handles
    last_hyperlink_selected = click_on_hyperlink_and_get_href(
        context, face_to_face_text
    )
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


@step("a Missing Information validation message is displayed to the user")
def step_impl(context):
    alert = context.helperfunc.find_by_css_selector("div[class='modal-dialog '")
    error_text = "You must collect at least a name and a postcode or phone number"
    assert error_text in alert.text
