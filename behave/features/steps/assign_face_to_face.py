from features.constants import ASSIGN_F2F_CASE
from features.steps.common_steps import search_and_select_case
from behave import step
from selenium.webdriver.common.by import By


@step("that I am on the Alternative Help page")
def step_impl_alt_help(context):
    # The case used has been created for this test case.
    # we select and then go through to alternative help
    search_and_select_case(context, ASSIGN_F2F_CASE)
    context.execute_steps(
        """
        When I click on the Assign Alternative Help icon
        Then I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    """
    )


@step("I can select the Assign F2F button")
def step_impl_assign_f2f(context):
    # This clicks the face to face link, which is hidden as a tab.
    page = context.helperfunc
    tabs = page.find_by_css_selector("ul.Tabs")
    face_to_face_tab = tabs.find_element_by_link_text("Face to Face")
    page.driver().execute_script("arguments[0].click();", face_to_face_tab)
    # This clicks the actual assign F2F button.
    page.click_button(By.NAME, "assign-f2f")
