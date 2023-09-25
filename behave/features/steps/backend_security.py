from behave import step
from selenium.webdriver.common.by import By
import datetime
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
from helper.constants import (
    MINIMUM_WAIT_UNTIL_TIME,
    CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO,
    CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK,
    FOX_ADMIN_FORM_FIELDS,
    USERS,
)
from features.steps.common_steps import wait_until_page_is_loaded, assert_header_on_page

@step("The session warning is not visible")
def step_impl_session_warning_not_visible(context):
    warning = context.helperfunc.find_by_id('session_security_warning')
    assert warning.getCSSValue("display") == None

@step("I wait for the session warning")
def step_impl_wait_session_warnings(context):
    try:
        WebDriverWait(context.browser, 9999).until(
        EC.visibility_of_element_located((By.ID, "session_security_warning")))
    except TimeoutException:
        logging.error("Warning message not displayed after inactivity")