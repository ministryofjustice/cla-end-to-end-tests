from features.constants import CLA_CALLBACK_CASES, CLA_FRONTEND_URL
from features.steps.common_steps import assert_header_on_page, wait_until_page_is_loaded


@given(u'I am viewing a callback slot')
def step_impl(context):
    # this is actually a composite of several of the steps in another scenario
    # context.execute_steps(u'''
    #     Given that I am on cases callback page
    #     When I select a callback slot
    # ''')
    start_page_url = f"{CLA_FRONTEND_URL}/call_centre/callbacks/"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Cases", context)
    callbacks = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    callbacks[0].click()


@given(u'callback slot contains a case created on CLA Public')
def step_impl(context):
    xpath_string = f'//table[@class="ListTable"]/tbody/tr[./td/abbr[@title="WEB CASE"]]/td/a'
    cla_callback_case = context.helperfunc.find_by_xpath(xpath_string)
    assert cla_callback_case is not None, f"Cannot find any cases created on CLA Public in the chosen callback slot"
    # find the reference of the case associated with this icon and use it for next step
    context.callback_case_element_link = cla_callback_case


@when(u'I select a case created on CLA Public from the callback slot')
def step_impl(context):
    # find and click on the case in the callback list
    assert context.callback_case_element_link is not None, f"No callback case to link to"
    context.callback_case_element_link.click()


@step(u'I am taken to the call centre case details page')
def step_on_case_details_page(context):
    # check the url of the page
    # will look like /call_centre/CASEID/diagnosis/
    callback_case_ref = context.callback_case_element_link.text
    page = f"/call_centre/{callback_case_ref}/diagnosis/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page(callback_case_ref, context)












