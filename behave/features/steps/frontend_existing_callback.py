from cla_common.call_centre_availability import OpeningHours
from cla_common.constants import OPERATOR_HOURS
from helper.constants import CLA_CALLBACK_CASES, CLA_FRONTEND_URL
from features.steps.common_steps import (
    compare_client_details_with_backend,
    assert_header_on_page,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from behave import step

import pytz


def get_next_available_callback_slots():
    # Need to get available slots from cla_common.
    # Use OpeningHours class with correct setup so that it knows about bank holidays
    operator_hours = OpeningHours(**OPERATOR_HOURS)
    available_days_from_common = operator_hours.available_days(2)
    all_available_slots = []
    for day in available_days_from_common:
        available_slots = operator_hours.time_slots(day.date())
        all_available_slots.extend(available_slots)
    # do every other slot as on the display they lump two slots together on website
    slots_chosen = all_available_slots[:8:2]
    slots_chosen.append(all_available_slots[0])
    return slots_chosen


@step("I have created cases with callbacks")
# This is the background step that takes test cases and assigns a callback slot some time over the next few days
def step_impl_created_cases_and_callbacks(context):
    slots_chosen = get_next_available_callback_slots()
    for index, case in enumerate(CLA_CALLBACK_CASES):
        # don't create a callback for the case if there is already one for this case
        callback_check = context.helperfunc.get_case_callback_details_from_backend(case)
        # look for CB code in logs, if no logs or if  no 'code' about callbacks in logs then no callback created
        callback_already_created = next(
            (item for item in callback_check if item["code"] in ["CB1", "CB2", "CB3"]),
            None,
        )
        if callback_already_created is None:
            # slots passed to backend must be utc but times from cla_common are not timezone aware.
            next_slot = pytz.timezone("Europe/London").localize(slots_chosen[index])
            next_slot_utc = next_slot.astimezone(pytz.utc)
            time_slot_start = next_slot_utc.strftime("%d/%m/%Y %H:%M")
            case_reference = case
            callback_json = {
                "datetime": time_slot_start,
                "notes": "",
                "priority_callback": False,
            }
            # we don't try and add another callback after one created and
            # Opening Hours returns only available slots
            new_callback = context.helperfunc.update_case_callback_details(
                case_reference, callback_json
            )
            message = (
                f'Error for case {new_callback["case_reference"]}, '
                f'data {new_callback["call_back_json"]} returned {new_callback["response_json"]}'
            )
            # return error if not 204 response
            assert new_callback["response_status_code"] == 204, message


@step("that I am on cases callback page")
def step_impl_cases_callback_page(context):
    start_page_url = f"{CLA_FRONTEND_URL}/call_centre/callbacks/"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Cases", context)


@step("multiple cases with a callback exists")
def step_impl_multiple_cases(context):
    #  there will be at least one <a> element that shows callbacks are booked
    callbacks_exist = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    assert (
        len(callbacks_exist) > 1
    ), f"Found only {len(callbacks_exist)} callbacks, expected to have more than one."


@step("I select a callback slot")
def step_impl_select_callback_slot(context):
    # look for the callbacks and click on the first one
    callbacks = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    callbacks[0].click()


@step("I can see the cases where a callback is booked for that slot")
def step_impl_callback_booked(context):
    # look for the cases displayed alongside the calendar
    list_cases = context.helperfunc.find_by_class("ListTable")
    case_rows = list_cases.find_elements_by_xpath("//tbody/tr/td")
    assert case_rows is not None


@step("I am viewing a callback slot")
def step_impl_view_callback(context):
    # this is actually a composite of several of the steps in another scenario
    context.execute_steps(
        """
        Given that I am on cases callback page
        When I select a callback slot
    """
    )


@step("callback slot contains a case created on CLA Public")
def step_impl_contains_case(context):
    xpath_string = (
        '//table[@class="ListTable"]/tbody/tr[./td/abbr[@title="WEB CASE"]]/td/a'
    )
    cla_callback_case = context.helperfunc.find_by_xpath(xpath_string)
    assert (
        cla_callback_case is not None
    ), "Cannot find any cases created on CLA Public in the chosen callback slot"
    # find the reference of the case associated with this icon and use it for next step
    context.callback_case_element_link = cla_callback_case
    context.selected_case_ref = cla_callback_case.text


@step("I select a case created on CLA Public from the callback slot")
def step_impl_select_case(context):
    # find and click on the case in the callback list
    assert context.callback_case_element_link is not None, "No callback case to link to"
    context.callback_case_element_link.click()


@step("I can view the client details of a case created on CLA Public")
def step_on_case_details_page(context):
    case_id = context.selected_case_ref
    client_section = context.helperfunc.find_by_id("personal_details")
    compare_client_details_with_backend(context, case_id, client_section)
    element = "p"
    title_value = "Case source"
    xpath_string = f'//{element}[@title="{title_value}"]'
    assert (
        client_section.find_element_by_xpath(xpath_string).text == "Web"
    ), "Case is not from WEB"


@step('I select "Start Call"')
def step_impl_start_call(context):
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


@step("the call has started")
def step_impl_call_has_started(context):
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


@step("I remove the callback")
def step_impl_remove_callback(context):
    callback_wrapper_element = context.helperfunc.find_by_css_selector(
        "callback-status"
    )
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


@step("this case is removed from callback list (calendar view)")
def step_impl_callback_removed(context):
    assert context.selected_case_ref is not None, "Case reference missing"
    callbacks = context.helperfunc.get_future_callbacks()
    for callback in callbacks:
        assert (
            callback["reference"] != context.selected_case_ref
        ), f"Case {context.selected_case_ref} is still present in the callbacks dashboard"
