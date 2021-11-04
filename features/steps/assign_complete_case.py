from behave import *
from features.constants import MATTER_TYPE_1, MATTER_TYPE_2


@given(u'I enter the case notes "{case_notes_text}"')
def step_impl(context, case_notes_text):
    print(case_notes_text)
    notes = context.helperfunc.find_by_name('case.notes')
    # Focus on element first
    notes.click()
    notes.send_keys(case_notes_text)
    assert len(notes.get_attribute('value')) == 0


@when(u'I select a category from Matter Type 1')
def step_impl(context):
    # Todo: Remove - Only used to aid in the writing of this test whilst some base tests are being developed by others
    # Created a dummy case with all the prerequisites required to assign a case
    config = context.config.userdata
    login_url = f"{config['cla_frontend_url']}/call_centre/RY-6964-7113/assign/"
    context.helperfunc.open(login_url)

    # Find matter type 1 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector('#s2id_matter_type1')
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_1}']").click()
    assert element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_1


@when(u'I select a category from Matter Type 2')
def step_impl(context):
    # Find matter type 2 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector('#s2id_matter_type2')
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(F"//*[text()='{MATTER_TYPE_2}']").click()
    assert element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_2

