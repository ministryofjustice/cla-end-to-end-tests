from behave import step
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helper.constants import (
    CLA_BACKEND_SECURITY_URL,
)


@step("The session warning is not visible")
def step_impl_session_warning_not_visible(context):
    try:
        WebDriverWait(context.helperfunc.driver(), 5).until(
            EC.invisibility_of_element((By.ID, "session_security_warning"))
        )
    except TimeoutException:
        logging.error("Warning message present during active session")


@step("I wait for the session warning")
def step_impl_wait_session_warnings(context):
    try:
        WebDriverWait(context.helperfunc.driver(), 5).until(
            EC.visibility_of_element_located((By.ID, "session_security_warning"))
        )
    except TimeoutException:
        logging.error("Warning message not displayed after inactivity")


@step("I wait for the page to timeout")
def step_impl_session_timeout(context):
    WebDriverWait(context.helperfunc.driver(), 30).until(
        EC.visibility_of_element_located((By.ID, "id_username"))
    )


@step("I am logged out")
def step_impl_logged_out(context):
    assert WebDriverWait(context.helperfunc.driver(), 30).until(
        EC.visibility_of_element_located((By.ID, "id_password"))
    )


@step("I close the browser")
def step_impl_close_browser(context):
    context.helperfunc.close()


@step("I open a new CHS browser")
def step_impl_open_chs_browser(context):
    context.helperfunc.open(CLA_BACKEND_SECURITY_URL)


@step("I am on a passive URL")
def step_impl_open_passive_url(context):
    context.helperfunc.open(CLA_BACKEND_SECURITY_URL & "/reports/mi-cb1-extract/")
