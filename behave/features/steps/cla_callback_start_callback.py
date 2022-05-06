from behave import *
from features.constants import CLA_FRONTEND_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


@given(u'that I am viewing the case "{case_reference}" which has a callback')
def step_impl(context, case_reference):
    # Todo: can be removed when feature branch is rebased with https://dsdmoj.atlassian.net/browse/LGA-1824
    context.case_reference = case_reference
    url = f"{CLA_FRONTEND_URL}/call_centre/{case_reference}/"
    context.helperfunc.open(url)
    # callback_btn = context.helperfunc.find_by_css_selector('callback-status button')
    # assert callback_btn is not None, f"Could not find callback button for case {case_reference}"
    # assert callback_btn.text == "Start call"
    # context.start_callback_btn = callback_btn


@when(u'I select "Start Call"')
def step_impl(context):
    assert hasattr(context, "start_callback_btn"), "Call button not found"
    context.start_callback_btn.click()
    assert context.helperfunc.driver().switch_to.alert is not None, "Could not confirm start call"
    context.helperfunc.driver().switch_to.alert.accept()

    def wait_until_callback_is_started(*args, **kwargs):
        try:
            return not context.start_callback_btn.is_displayed()
        except StaleElementReferenceException:
            return True

    wait = WebDriverWait(context.helperfunc.driver(), 5)
    wait.until(wait_until_callback_is_started)


@then(u'the call has started')
def step_impl(context):
    assert context.case_reference is not None, "Not viewing a case"
    case_logs = context.helperfunc.get_case_callback_details_from_backend(context.case_reference)
    assert len(case_logs) >= 2, f"Logs needs at least 2 events(callback scheduled/started) - found {len(case_logs)} logs"
    callback_started_log = case_logs.pop(0)
    callback_created_log = case_logs.pop(0)
    assert callback_created_log["code"] == "CB1", "CB1 code not found in case logs"
    assert callback_started_log["code"] == "CALL_STARTED", "CALL_STARTED code not found in case logs"
    wrapper_element = context.helperfunc.find_by_css_selector('.CaseHistory')
    for case_log in case_logs:
        note_element = wrapper_element.find_element_by_xpath(f".//span[text()='{case_log['notes']}']")
        assert note_element is not None, f"Could not find case log: {case_log['notes']}"


@then(u'I remove the callback')
def step_impl(context):
    callback_wrapper_element = context.helperfunc.find_by_css_selector('callback-status')
    print(callback_wrapper_element.get_attribute("innerHTML"))
    remove_btn_element = callback_wrapper_element.find_element_by_xpath(".//a[text()='Remove callback']")
    assert remove_btn_element is not None, "Could not find  Remove callback button"
    remove_btn_element.click()

    assert context.helperfunc.driver().switch_to.alert is not None, "Could not confirm remove call back"
    context.helperfunc.driver().switch_to.alert.accept()
    case_history_wrapper_element = context.helperfunc.find_by_css_selector('.CaseHistory')

    def wait_until_callback_is_stopped(*args, **kwargs):
        callback_stopped_element = case_history_wrapper_element.find_element_by_xpath(".//span[text()='Callback stopped']")
        if callback_stopped_element:
            return True
        return False

    wait = WebDriverWait(context.helperfunc.driver(), 5)
    wait.until(wait_until_callback_is_stopped)


@then(u'this case is removed from callback list (calendar view)')
def step_impl(context):
    assert context.case_reference is not None, "Case reference missing"
    callbacks = context.helperfunc.get_future_callbacks()
    for callback in callbacks:
        assert callback["reference"] != context.case_reference, f"Case {context.case_reference} is still present in the callbacks dashboard"

    # Todo: requires https://dsdmoj.atlassian.net/browse/LGA-1824 to confirm case is not present in the UI
    raise NotImplementedError(u'STEP: Then this case is removed from callback list (calendar view)')

