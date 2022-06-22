from features.constants import CLA_EXISTING_USER
from selenium.webdriver.common.by import By


@when(u'I search for a client name with an existing case')
def step_impl(context):
    # find the search box
    search_box = context.helperfunc.find_by_name("q")
    user_name = CLA_EXISTING_USER
    search_box.click()
    # add in the user fullname to search for
    search_box.send_keys(user_name)
    # add in the user fullname to search for
    search_submit = context.helperfunc.find_by_name("case-search-submit")
    search_submit.click()


@then(u'I am taken to search results that shows cases belonging to that client')
def step_impl(context):
    context.execute_steps(u'''
        Given I am on the 'call centre dashboard' page
    ''')
    # now check and see if we have cases that are assigned to this user
    case_rows = context.helperfunc.driver().find_elements_by_xpath(f'//div/table[@class="ListTable"]/tbody/tr')
    assert case_rows is not None and filter(
        lambda case_row:
        CLA_EXISTING_USER in case_row.text, case_rows), f"No cases associated with user {CLA_EXISTING_USER}"


@then(u'I select the name hyperlink for an existing case')
def step_impl(context):
    # use the name hyperlink in the first row, we know there are cases because of previous steps
    # often fails with stale element exception
    x_path = f'//div/table[@class="ListTable"]/tbody/tr/td/span/a'
    assert context.helperfunc.find_by_xpath(x_path) is not None
    context.helperfunc.click_button(By.XPATH, x_path)


@then(u'I select the button to create a case for the client originally searched for')
def step_impl(context):
    # this button has the same id as when it just says 'create a case' so can use the original step
    context.execute_steps(u'''
        Given I select to 'Create a case'
    ''')


