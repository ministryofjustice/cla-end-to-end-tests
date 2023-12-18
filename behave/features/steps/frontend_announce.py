import logging
from behave import step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

CALL_ANNOUNCE_WARNING_ID = "cla-call-announce-warning"


@step("The 'do not announce the call is from CLA' warning is present")
def step_impl_cla_announce_warning_present(context):
    try:
        element = context.helperfunc.find_by_id(CALL_ANNOUNCE_WARNING_ID)
    except TimeoutException:
        logging.error("The call announce warning element is not present.")
    assert element is not None


@step("the 'do not announce the call is from CLA' warning is not present")
def step_impl_cla_announce_warning_not_present(context):
    try:
        WebDriverWait(context.helperfunc.driver(), 5).until(
            EC.invisibility_of_element((By.ID, CALL_ANNOUNCE_WARNING_ID))
        )
    except TimeoutException:
        logging.error("The call announce warning element is present.")
    except NoSuchElementException:
        # Pass because this is expected result.
        pass
