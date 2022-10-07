from features.steps.common_steps import compare_client_details_with_backend
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


@given("I am viewing a callback slot")
def step_impl(context):
    # this is actually a composite of several of the steps in another scenario
    context.execute_steps(
        """
        Given that I am on cases callback page
        When I select a callback slot
    """
    )


@given("callback slot contains a case created on CLA Public")
def step_impl(context):
    xpath_string = (
        f'//table[@class="ListTable"]/tbody/tr[./td/abbr[@title="WEB CASE"]]/td/a'
    )
    cla_callback_case = context.helperfunc.find_by_xpath(xpath_string)
    assert (
        cla_callback_case is not None
    ), f"Cannot find any cases created on CLA Public in the chosen callback slot"
    # find the reference of the case associated with this icon and use it for next step
    context.callback_case_element_link = cla_callback_case
    context.selected_case_ref = cla_callback_case.text


@when("I select a case created on CLA Public from the callback slot")
def step_impl(context):
    # find and click on the case in the callback list
    assert (
        context.callback_case_element_link is not None
    ), f"No callback case to link to"
    context.callback_case_element_link.click()


@step("I can view the client details of a case created on CLA Public")
def step_on_case_details_page(context):
    case_id = context.selected_case_ref
    client_section = context.helperfunc.find_by_id("personal_details")
    compare_client_details_with_backend(context, case_id, client_section)
    # and check that this shows the source is WEB
    element = "p"
    title_value = "Case source"
    xpath_string = f'//{element}[@title="{title_value}"]'
    assert (
        client_section.find_element_by_xpath(xpath_string).text == "Web"
    ), f"Case is not from WEB"


@when('I select "Start Call"')
def step_impl(context):
    callback_btn = context.helperfunc.find_by_css_selector("callback-status button")
    assert (
        callback_btn is not None
    ), f"Could not find callback button for case {context.selected_case_ref}"
    assert callback_btn.text == "Start call"
    context.start_callback_btn = callback_btn
    context.start_callback_btn.click()
    assert (
        context.helperfunc.driver().switch_to.alert is not None
    ), "Could not confirm start call"
    context.helperfunc.driver().switch_to.alert.accept()

    def wait_until_callback_is_started(*args, **kwargs):
        try:
            return not context.start_callback_btn.is_displayed()
        except StaleElementReferenceException:
            return True

    wait = WebDriverWait(context.helperfunc.driver(), 5)
    wait.until(wait_until_callback_is_started)


@then("the call has started")
def step_impl(context):
    assert context.selected_case_ref is not None, "Not viewing a case"
    case_logs = context.helperfunc.get_case_callback_details_from_backend(
        context.selected_case_ref
    )
    assert (
        len(case_logs) >= 2
    ), f"Logs needs at least 2 events(callback scheduled/started) - found {len(case_logs)} logs"
    callback_started_log = case_logs.pop(0)
    callback_created_log = case_logs.pop(0)
    assert callback_created_log["code"] == "CB1", "CB1 code not found in case logs"
    assert (
        callback_started_log["code"] == "CALL_STARTED"
    ), "CALL_STARTED code not found in case logs"
    wrapper_element = context.helperfunc.find_by_css_selector(".CaseHistory")
    for case_log in case_logs:
        note_element = wrapper_element.find_element_by_xpath(
            f".//span[text()='{case_log['notes']}']"
        )
        assert note_element is not None, f"Could not find case log: {case_log['notes']}"


@then("I remove the callback")
def step_impl(context):
    callback_wrapper_element = context.helperfunc.find_by_css_selector(
        "callback-status"
    )
    print(callback_wrapper_element.get_attribute("innerHTML"))
    remove_btn_element = callback_wrapper_element.find_element_by_xpath(
        ".//a[text()='Remove callback']"
    )
    assert remove_btn_element is not None, "Could not find  Remove callback button"
    remove_btn_element.click()

    assert (
        context.helperfunc.driver().switch_to.alert is not None
    ), "Could not confirm remove call back"
    context.helperfunc.driver().switch_to.alert.accept()
    case_history_wrapper_element = context.helperfunc.find_by_css_selector(
        ".CaseHistory"
    )

    def wait_until_callback_is_stopped(*args, **kwargs):
        callback_stopped_element = case_history_wrapper_element.find_element_by_xpath(
            ".//span[text()='Callback stopped']"
        )
        if callback_stopped_element:
            return True
        return False

    wait = WebDriverWait(context.helperfunc.driver(), 5)
    wait.until(wait_until_callback_is_stopped)


@then("this case is removed from callback list (calendar view)")
def step_impl(context):
    assert context.selected_case_ref is not None, "Case reference missing"
    callbacks = context.helperfunc.get_future_callbacks()
    for callback in callbacks:
        assert (
            callback["reference"] != context.selected_case_ref
        ), f"Case {context.selected_case_ref} is still present in the callbacks dashboard"
