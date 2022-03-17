from features.constants import CLA_FRONTEND_URL, CLA_SPECIALIST_PROVIDERS_NAME
from features.steps.cla_in_scope import wait_until_page_is_loaded
from selenium.common.exceptions import TimeoutException

@when(u'I choose "{provider}" as Specialist Provider')
def step_impl_choose_provider(context, provider):
    # Check to see who the current provider is:
    auto_provider_name = ''
    try:
        auto_provider_name = context.helperfunc.find_by_css_selector('.ContactBlock-heading').text
    except TimeoutException:
        pass       
    if auto_provider_name != CLA_SPECIALIST_PROVIDERS_NAME:
        # assign manually to get chosen provider
        context.helperfunc.find_by_name("assign-manually").click()
        for i in context.helperfunc.driver().find_elements_by_xpath('//input[@name="provider"]'): 
            check_name = i.find_element_by_xpath('..').find_element_by_xpath('descendant::strong').text
            if check_name == CLA_SPECIALIST_PROVIDERS_NAME:
                # click on the radio button which chooses the correct provider
                i.click()

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
    # check the cases available
    case_found = False
    table = context.helperfunc.driver().find_element_by_css_selector(".ListTable")
    import pdb
    pdb.set_trace()
    cases = table.find_elements_by_xpath('//tr')
    case_new = context.helperfunc.get_case_from_backend(context.case_id)
    for case in cases:
        print(case.find_element_by_xpath('//td//a').text)
        if case.find_element_by_xpath('//td//a').text == context.case_id:
            case_found = True
    # assert case_found
    # //table[@class='ListTable']/tbody/tr//a
    # context.case_id not in table.text
