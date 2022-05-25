from features.steps.common_steps import assert_header_on_page, wait_until_page_is_loaded, compare_client_details_with_backend


@given(u'I am viewing a callback slot')
def step_impl(context):
    # this is actually a composite of several of the steps in another scenario
    context.execute_steps(u'''
        Given that I am on cases callback page
        When I select a callback slot
    ''')


@given(u'callback slot contains a case created on CLA Public')
def step_impl(context):
    xpath_string = f'//table[@class="ListTable"]/tbody/tr[./td/abbr[@title="WEB CASE"]]/td/a'
    cla_callback_case = context.helperfunc.find_by_xpath(xpath_string)
    assert cla_callback_case is not None, f"Cannot find any cases created on CLA Public in the chosen callback slot"
    # find the reference of the case associated with this icon and use it for next step
    context.callback_case_element_link = cla_callback_case
    context.selected_case_ref = cla_callback_case.text


@when(u'I select a case created on CLA Public from the callback slot')
def step_impl(context):
    # find and click on the case in the callback list
    assert context.callback_case_element_link is not None, f"No callback case to link to"
    context.callback_case_element_link.click()


@step(u'I can view the client details of a case created on CLA Public')
def step_on_case_details_page(context):
    case_id = context.selected_case_ref
    client_section = context.helperfunc.find_by_id('personal_details')
    compare_client_details_with_backend(context, case_id, client_section)
    # and check that this shows the source is WEB
    element = "p"
    title_value = "Case source"
    xpath_string = f'//{element}[@title="{title_value}"]'
    assert client_section.find_element_by_xpath(xpath_string).text == "Web", f"Case is not from WEB"











