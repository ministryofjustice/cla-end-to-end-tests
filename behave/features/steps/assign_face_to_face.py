from features.steps.common_steps import search_and_select_case, wait_until_page_is_loaded
from features.steps.cla_in_scope import assert_header_on_page
from selenium.webdriver.common.by import By


@step(u'that I am on the Alternative Help page')
def step_impl(context):
    # The case used has been created for this test case.
    # we select and then go through to alternative help
    search_and_select_case(context, "AS-0001-0001")
    context.execute_steps(u'''
        When I click on the Assign Alternative Help icon
        Then I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    ''')


@step(u'I am can select Assign F2F button')
def step_impl(context):
    # This clicks the face to face link, which is hidden as a tab.
    page = context.helperfunc
    tabs = page.find_by_css_selector("ul.Tabs")
    finance_tab_link = tabs.find_element_by_link_text("Face to Face")
    page.driver().execute_script("arguments[0].click();", finance_tab_link)
    page.click_button(By.NAME, "assign-f2f")


@step(u'I am taken to the call centre dashboard page')
def step_impl(context):
    # Make sure that we get redirected to the call centre dashboard
    wait_until_page_is_loaded("/call_centre/", context)
    assert_header_on_page("Cases", context)