from helper.constants import CLA_EXISTING_USER
from selenium.webdriver.common.by import By
from behave import step
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceExce


@step("I search for a client name with an existing case")
def step_impl_search_client(context):
    # find the search box
    search_box = context.helperfunc.find_by_name("q")
    user_name = CLA_EXISTING_USER
    search_box.click()
    # add in the user fullname to search for
    search_box.send_keys(user_name)
    # add in the user fullname to search for
    search_submit = context.helperfunc.find_by_name("case-search-submit")
    search_submit.click()


@step("I am taken to search results that shows cases belonging to that client")
def step_impl_search_results(context):
    context.execute_steps("""
        Given I am on the 'call centre dashboard' page
    """)
    # now check and see if we have cases that are assigned to this user
    case_rows = context.helperfunc.driver().find_elements(
        By.XPATH, '//div/table[@class="ListTable"]/tbody/tr'
    )
    assert case_rows is not None and filter(
        lambda case_row: CLA_EXISTING_USER in case_row.text, case_rows
    ), "No cases associated with user {CLA_EXISTING_USER}"


@step("I select the name hyperlink for an existing case")
def step_impl_select_name_hyperlink(context):
    wait = WebDriverWait(context.helperfunc.driver(), 15)
    x_path = '//div/table[@class="ListTable"]/tbody/tr/td/span/a'

    for attempt in range(4):
        try:
            link = wait.until(EC.element_to_be_clickable((By.XPATH, x_path)))
            link.click()
            return
        except StaleElementReferenceException:
            if attempt == 3:
                raise


@step("I select the button to create a case for the client originally searched for")
def step_impl_create_case_button(context):
    # this button has the same id as when it just says 'create a case' so can use the original step
    context.execute_steps("""
        Given I select to 'Create a case'
    """)
