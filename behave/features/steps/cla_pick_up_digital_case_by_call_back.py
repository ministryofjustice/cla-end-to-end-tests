from cla_common.call_centre_availability import OpeningHours
from cla_common.constants import OPERATOR_HOURS
from features.constants import CLA_CALLBACK_CASES, CLA_FRONTEND_URL
from features.steps.cla_in_scope import assert_header_on_page
import random


@given(u'that I have created cases with callbacks')
# This is the background step that takes test cases and assigns a callback slot some time over the next few days
def step_impl(context):
    # format of the json that we need for the callback is
    # {
    #     "datetime": "05/05/2022 09:00",
    #     "notes": "",
    #     "priority_callback": false
    # }
    # Need to get available slots from cla_common.
    # Use OpeningHours class with correct setup so that it knows about bank holidays
    # Choose 6 days so can be sure that will not get three bank holidays/sunday etc
    operator_hours = OpeningHours(**OPERATOR_HOURS)
    available_days_from_common = operator_hours.available_days(6)
    all_available_slots = []
    for day in available_days_from_common:
        available_slots = operator_hours.time_slots(day.date())
        all_available_slots.extend(available_slots)
    slots_chosen = all_available_slots[4:]
    slots_chosen.append(all_available_slots[0])
    for index, case in enumerate(CLA_CALLBACK_CASES):
        # don't create a callback for the case if there is already one for this case
        # this may not produce two in the same slot
        try:
            callback_already_created = context.helperfunc.get_case_callback_details_from_backend(case)
            # look for CB code in logs
            assert callback_already_created[0]['code'] in ['CB1', 'CB2', 'CB3'], "Callback not created"
        except AssertionError:
            next_slot = slots_chosen[index]
            time_slot_start = next_slot.strftime("%d/%m/%Y %H:%M")
            case_reference = case
            # create the json to pass to the api
            callback_json = {
                'datetime': time_slot_start,
                'notes': '',
                'priority_callback': False
            }
            # may fail sometimes
            did_it_work = context.helperfunc.update_case_callback_details(case_reference, callback_json)
            if did_it_work["response_status_code"] != 204:
                # try again?
                # if are we in the first time-slot
                # then need to update this and the last slot so have two in same slot
                new_slot = random.choice(all_available_slots[-4:])
                if index == 0:
                    slots_chosen[-1] = new_slot
                new_time_slot_start = new_slot.strftime("%d/%m/%Y %H:%M")
                callback_json['datetime'] = new_time_slot_start
                last_chance = context.helperfunc.update_case_callback_details(case_reference, callback_json)
                message = f'Assertion error for case {last_chance["case_reference"]}, data {last_chance["call_back_json"]} returned {last_chance["response_json"]}'
                assert last_chance["response_status_code"] != 204, message


@given(u'that I am on cases callback page located at /call_centre/callbacks/')
def step_impl(context):
    start_page_url = f"{CLA_FRONTEND_URL}/call_centre/callbacks/"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Cases", context)


@given(u'multiple cases with a callback exists')
def step_impl(context):
    #  there will be at least one <a> element that shows callbacks are booked
    callbacks_exist = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    assert len(callbacks_exist) > 1, f"Only {len(callbacks_exist)} callback, want more than one "


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








