from features.constants import CLA_FRONTEND_URL, CLA_SPECIALIST_PROVIDERS_NAME
from features.steps.cla_in_scope import wait_until_page_is_loaded, assert_header_on_page
from selenium.common.exceptions import TimeoutException

@step(u'I am logged in as a Specialist Provider')
def step_logged_in(context):
    config = context.config.userdata
    login_url = f"{CLA_FRONTEND_URL}/auth/login/"
    context.helperfunc.open(login_url)
    form = context.helperfunc.find_by_name('login_frm')
    assert form is not None
    form.find_element_by_name("username").send_keys(config["cla_specialist_provider_username"])
    form.find_element_by_name("password").send_keys(config["cla_specialist_provider_password"])
    form.find_element_by_name("login-submit").click()

    
@given(u'that I am on the specialist provider cases dashboard page')
def step_on_spec_providers_dashboard(context):
    element = context.helperfunc.find_by_xpath("//html[@ng-app='cla.providerApp']")
    assert element is not None
    
@given(u'there is a case available')
def step_check_cases(context):
    # check there are cases available
    table = context.helperfunc.driver().find_element_by_css_selector(".ListTable")
    cases = table.find_elements_by_xpath('//tr')
    # how many cases?
    assert len(cases) > 0

@when(u'I select a case from the dashboard')
def step_select_special_provider_case(context):
    table = context.helperfunc.driver().find_element_by_css_selector(".ListTable")
    cases = table.find_elements_by_xpath('//tr')
    # select the first case from the list
    # previous step checks that there is at least one
    selected_case = cases[0].find_element_by_xpath('//td//a')
    context.selected_case_id = cases[0].find_element_by_xpath('//td//a').text
    assert selected_case is not None
    selected_case.click()

@then(u'I am taken to the case details page')
def step_on_case_details_page(context):
    # check the url of the page
    # will look like /provider/CASEID/diagnosis/
    page = f"/provider/{context.selected_case_id}/diagnosis/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page(context.selected_case_id, context)
    

