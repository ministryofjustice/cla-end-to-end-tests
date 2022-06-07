from cla_common.call_centre_availability import OpeningHours
from cla_common.constants import OPERATOR_HOURS
from features.constants import CLA_CALLBACK_CASES, CLA_FRONTEND_URL
from features.steps.cla_in_scope import assert_header_on_page
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


@given(u'that I have created cases with callbacks')
# This is the background step that takes test cases and assigns a callback slot some time over the next few days
def step_impl(context):
    slots_chosen = get_next_available_callback_slots()
    for index, case in enumerate(CLA_CALLBACK_CASES):
        # don't create a callback for the case if there is already one for this case
        callback_check = context.helperfunc.get_case_callback_details_from_backend(case)
        # look for CB code in logs, if no logs or if  no 'code' about callbacks in logs then no callback created
        callback_already_created = next(
            (item for item in callback_check if item["code"] in ['CB1', 'CB2', 'CB3']), None)
        if callback_already_created is None:
            # slots passed to backend must be utc but times from cla_common are not timezone aware.
            next_slot = pytz.timezone('Europe/London').localize(slots_chosen[index])
            next_slot_utc = next_slot.astimezone(pytz.utc)
            time_slot_start = next_slot_utc.strftime("%d/%m/%Y %H:%M")
            case_reference = case
            # create the json to pass to the api
            # format of the json that we need for the callback is
            # {
            #     "datetime": "05/05/2022 09:00",
            #     "notes": "",
            #     "priority_callback": false
            # }
            callback_json = {
                'datetime': time_slot_start,
                'notes': '',
                'priority_callback': False
            }
            # should always work, return error if not 204 response
            # we don't try and add another callback after one created and
            # Opening Hours returns only available slots
            new_callback = context.helperfunc.update_case_callback_details(case_reference, callback_json)
            message = f'Error for case {new_callback["case_reference"]}, ' \
                      f'data {new_callback["call_back_json"]} returned {new_callback["response_json"]}'
            assert new_callback["response_status_code"] == 204, message


@given(u'that I am on cases callback page')
def step_impl(context):
    start_page_url = f"{CLA_FRONTEND_URL}/call_centre/callbacks/"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Cases", context)


@given(u'multiple cases with a callback exists')
def step_impl(context):
    #  there will be at least one <a> element that shows callbacks are booked
    callbacks_exist = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    assert len(callbacks_exist) > 1, f"Found only {len(callbacks_exist)} callbacks, expected to have more than one."


@when(u'I select a callback slot')
def step_impl(context):
    # look for the callbacks and click on the first one
    callbacks = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    callbacks[0].click()


@then(u'I can see the cases where a callback is booked for that slot')
def step_impl(context):
    # look for the cases displayed alongside the calendar
    list_cases = context.helperfunc.find_by_class("ListTable")
    case_rows = list_cases.find_elements_by_xpath(f'//tbody/tr/td')
    assert case_rows is not None








