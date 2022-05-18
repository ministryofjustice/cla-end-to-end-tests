from features.constants import CLA_CALLBACK_CASES, CLA_FRONTEND_URL
from features.steps.cla_in_scope import assert_header_on_page


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
    import pdb
    pdb.set_trace()
    callbacks = context.helperfunc.find_many_by_class("CallbackMatrix-slot")
    callbacks[0].click()


@given(u'callback slot contains a case created on CLA Public')
def step_impl(context):
    xpath_string = f'//table[@class="ListTable"]/tbody/tr[./td/abbr[@title="WEB CASE"]]/td/a'
    cla_callback_case = context.helperfunc.find_by_xpath(xpath_string)
    assert cla_callback_case is not None, f"Cannot find any cases created on CLA Public in the chosen callback slot"
    # find the reference of the case associated with this icon and use it for next step


@when(u'I select a case created on CLA Public from the callback slot')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I select a case created on CLA Public from the callback slot')













