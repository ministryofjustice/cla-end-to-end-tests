from features.constants import CLA_FRONTEND_URL, CLA_SPECIALIST_PROVIDERS_NAME
from features.steps.cla_in_scope import wait_until_page_is_loaded, assert_header_on_page
from helper.helper_base import HelperFunc
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

    
@step(u'that I am on the specialist provider cases dashboard page')
def step_on_spec_providers_dashboard(context):
    element = context.helperfunc.find_by_xpath("//html[@ng-app='cla.providerApp']")
    assert element is not None
    
@step(u'there is a case available')
def step_check_cases(context):
    # check there are cases available
    table = context.helperfunc.driver().find_element_by_css_selector(".ListTable")
    cases = table.find_elements_by_xpath('//tr')
    # how many cases?
    assert len(cases) > 0

@step(u'I select a case from the dashboard')
def step_select_special_provider_case(context):
    table = context.helperfunc.driver().find_element_by_css_selector(".ListTable")
    cases = table.find_elements_by_xpath('//tr')
    # select the first case from the list
    # previous step checks that there is at least one
    selected_case = cases[0].find_element_by_xpath('//td//a')
    context.selected_case_ref = cases[0].find_element_by_xpath('//td//a').text
    assert selected_case is not None
    selected_case.click()

@step(u'I am taken to the case details page')
def step_on_case_details_page(context):
    # check the url of the page
    # will look like /provider/CASEID/diagnosis/
    page = f"/provider/{context.selected_case_ref}/diagnosis/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page(context.selected_case_ref, context)
    
@given(u'I can view the client details')
def step_impl(context):
    # look for the client details on the left hand side of screen
    client_section = context.helperfunc.find_by_id('personal_details')
    assert client_section is not None
    # check it is the right client
    displayed_name = client_section.find_element_by_xpath(f'//h2[@title="Full name"]').text
    backend_name = context.helperfunc.get_case_personal_details_from_backend(context.selected_case_ref)['full_name']
    assert displayed_name == backend_name

@given(u'I can view the case details and notes entered by the Operator')
def step_impl(context):
    # check there is a case history on the rhs
    case_history = context.helperfunc.find_by_class("CaseHistory")
    assert case_history is not None
    # check that there are operator comments
    operator_comments = context.helperfunc.find_by_class("CommentBlock").find_elements_by_xpath("./child::*")
    # "operator said" is the second child and then there are case notes below that.
    assert len(operator_comments) >= 3   

    
@when(u'I select Scope')
def step_impl(context):
    scope_link = context.helperfunc.find_by_xpath('//a[@ui-sref="case_detail.edit.diagnosis"]')
    assert scope_link is not None
    # click on the link
    scope_link.click()
    
@then(u'I can view the scope assessment entered by the Operator')
def step_impl(context):
    # <section class="SummaryBlock SummaryBlock--compact ng-scope" ng-if="diagnosis.nodes">
    # check that the scope assessment exists
    scope_description = context.helperfunc.find_by_xpath('//section[@class="SummaryBlock SummaryBlock--compact ng-scope"]')
    assert scope_description is not None
    # check that there is a category of law and that it is INSCOPE
    scope_inscope = scope_description.find_elements_by_xpath(f'.//div/p[text()="INSCOPE"]')
    assert scope_inscope is not None
    # this would find all descriptors if needed
    # scope_descriptors = scope_description.find_element_by_xpath(f'.//div/p')
    scope_cat_of_law = scope_description.find_element_by_xpath(f'.//div/p[starts-with(.,"Category of law")]')
    assert scope_cat_of_law is not None and len(scope_cat_of_law.text)>len("Category of law:")


    
