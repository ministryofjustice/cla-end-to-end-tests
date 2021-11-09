from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from features.constants import MATTER_TYPE_1, MATTER_TYPE_2, CLA_FRONTEND_URL


@given(u'I enter the case notes "{case_notes_text}"')
def step_impl_case_notes(context, case_notes_text):
    notes = context.helperfunc.find_by_name('case.notes')
    # Focus on element first
    notes.click()
    notes.send_keys(case_notes_text)
    assert notes.get_attribute('value') == case_notes_text


@when(u'I select a category from Matter Type 1')
def step_impl_matter_type1(context):
    # Find matter type 1 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector('#s2id_matter_type1')
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_1}']").click()
    assert element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_1


@when(u'I select a category from Matter Type 2')
def step_impl_matter_type2(context):
    # Find matter type 2 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector('#s2id_matter_type2')
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(F"//*[text()='{MATTER_TYPE_2}']").click()
    assert element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_2


@when(u'there is only one provider')
def step_impl_one_provider(context):
    # Find matter type 2 wrapper and focus on it
    form = context.helperfunc.find_by_name('assign_provider_form')
    headings = form.find_elements_by_css_selector("h2.ContactBlock-heading")
    context.provider_selected = headings[0].text
    assert len(headings) == 1

@when(u'I select \'Assign Provider\'')
def step_impl_assign_provider(context):
    context.case_id = context.helperfunc.find_by_css_selector('.CaseBar-caseNum a').text
    context.helperfunc.find_by_name("assign-provider").click()

@then(u'the case is assigned to the Specialist Provider')
def step_impl_case_assigned(context):

    def wait_until_case_is_assigned(*args):
        element = context.helperfunc.find_by_css_selector(".NoticeContainer--fixed li.Notice")
        return element is not None and element.text == f'Case {context.case_id} assigned to {context.provider_selected}'
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_case_is_assigned)

@then(u'I am taken to the call centre dashboard')
def step_impl_taken_to_call_centre_dashboard(context):
    current_path = context.helperfunc.get_current_path()
    assert current_path == "/call_centre/"

@then(u'the case does not show up on the call centre dashboard')
def step_impl_case_removed_from_list(context):
    dashboard_url = f"{CLA_FRONTEND_URL}/call_centre/?ordering=-modified&page=1"
    context.helperfunc.open(dashboard_url)
    table = context.helperfunc.find_by_css_selector(".ListTable")
    assert context.case_id not in table.text

