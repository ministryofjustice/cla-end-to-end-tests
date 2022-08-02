from behave import *
from features.constants import CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO, CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK
from features.steps.common_steps import wait_until_page_is_loaded, assert_header_on_page
from selenium.webdriver.common.by import By


@step(u'I select a non-staff user from the list')
def step_impl(context):
    # just click on a user that we know has non-staff status
    context.execute_steps(f'''
    Given I select the link "{CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO}"
    ''')


@when(u'I am taken to the user\'s details page')
def step_impl(context):
    # user details page is at /admin/auth/user/{pk}
    page = f"/admin/auth/user/{CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK}/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page("Change user", context)


@step(u'I select Staff status under permissions')
def step_impl(context):
    # click on the staff status checkbox
    xpath = f"//div[@class='checkbox-row']/input[@id='id_is_staff']"
    context.helperfunc.find_by_xpath(xpath).click()
    # for some reason this doesn't work
    # context.helperfunc.click_button(By.XPATH, xpath)


@step(u'I select save')
def step_impl(context):
    context.helperfunc.click_button(By.NAME, "_save")


@step(u'the users details are saved and I am taken back to the list of users')
def step_impl(context):
    # check that you have moved back to the list of users page
    page = f"/admin/auth/user/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page("Select user to change", context)
    # check there is a message that says the user was changed successfully
    link_text = 'The user "test_staff" was changed successfully'
    xpath = f"//ul/li[@class='success'][contains(text(), '{link_text}')]"
    assert len(context.helperfunc.find_many_by_xpath(xpath)) > 0, f"Cannot find success message"