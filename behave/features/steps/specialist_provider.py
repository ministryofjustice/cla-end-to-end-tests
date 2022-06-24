from behave import *
from features.constants import CLA_FRONTEND_URL, CLA_SPECIALIST_PROVIDERS_NAME, CLA_SPECIALIST_CASE_TO_ACCEPT
from features.steps.common_steps import compare_client_details_with_backend, select_case_from_caselist
from selenium.common.exceptions import NoSuchElementException


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
    # only carry on if there are cases that have not been accepted
    x_path = f".//table[@class='ListTable']/tbody/tr/td/abbr[@title='Case status'][not(@class='Icon Icon--folderAccepted')]"
    cases_not_accepted = context.helperfunc.driver().find_elements_by_xpath(x_path)
    assert len(cases_not_accepted) > 0, f"No unaccepted cases"


@step(u'I can view the client details')
def step_impl(context):
    case_id = context.selected_case_ref
    client_section = context.helperfunc.find_by_id('personal_details')
    compare_client_details_with_backend(context, case_id, client_section)


@step(u'I select a case from the dashboard')
def step_select_special_provider_case(context):
    case_reference = CLA_SPECIALIST_CASE_TO_ACCEPT
    select_case_from_caselist(context, case_reference)


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
    scope_description = context.helperfunc.find_by_xpath(
        '//section[@class="SummaryBlock SummaryBlock--compact ng-scope"]')
    assert scope_description is not None
    # check that there is a category of law and that it is INSCOPE
    scope_inscope = scope_description.find_elements_by_xpath(f'.//div/p[text()="INSCOPE"]')
    assert scope_inscope is not None
    # this would find all descriptors if needed
    # scope_descriptors = scope_description.find_element_by_xpath(f'.//div/p')
    scope_cat_of_law = scope_description.find_element_by_xpath(f'.//div/p[starts-with(.,"Category of law")]')
    assert scope_cat_of_law is not None and len(scope_cat_of_law.text) > len("Category of law:")


@given(u'I select \'Accept\'')
def step_impl(context):
    # find the accept button and click it
    accept_button = context.helperfunc.find_by_xpath('//button[@name="accept-case"]')
    assert accept_button is not None
    accept_button.click()


@given(u'I can see a \'Case accepted successfully\' message')
def step_impl(context):
    # wait for the flash message to appear. 
    flash_message = context.helperfunc.find_by_xpath('//*[text()="Case accepted successfully"]')
    assert flash_message is not None


@when(u'I return to the specialist provider cases dashboard page')
def step_impl(context):
    # click on the 'back to cases' link
    back_to_cases = context.helperfunc.find_by_xpath('//a[@class="SubNav-link SubNav-link--back"]')
    assert back_to_cases is not None
    back_to_cases.click()


@when(u'I select the Accepted tab')
def step_impl(context):
    # click on the 'Accepted' tab
    accepted_tab = context.helperfunc.find_by_xpath('//a[@class="Label Icon Icon--folderAccepted"]')
    assert accepted_tab is not None
    accepted_tab.click()


@then(u'I can see my accepted case reference number')
def step_impl(context):
    # click on the 'back to cases' link
    my_case = context.helperfunc.find_by_xpath(f"//*[text()='{context.selected_case_ref}']")
    assert my_case is not None


@given(u'that I am viewing a case that I have accepted as a specialist provider')
def step_impl(context):
    case_reference = CLA_SPECIALIST_CASE_TO_ACCEPT
    login_url = f"{CLA_FRONTEND_URL}/provider/{case_reference}/diagnosis/"
    context.helperfunc.open(login_url)


@given(u'I select the Legal help form')
def step_impl(context):
    wrapper = context.helperfunc.find_by_css_selector('.CaseBar-actions')
    legal_help_form_link = wrapper.find_element_by_xpath("//a[text()='Legal help form']")
    assert legal_help_form_link is not None, "Could not find legal help form link"
    legal_help_form_link.click()


def assert_your_details(table, root_element):
    for row in table:
        label_element = root_element.find_element_by_xpath(f".//*[text()='{row['field']}']")
        assert label_element is not None, f"Could not find question on legal help form: {row['field']}"
        parent_element = label_element.find_element_by_xpath(f"./..")
        try:
            value_element = parent_element.find_element_by_tag_name('input')
        except NoSuchElementException:
            value_element = parent_element.find_element_by_tag_name('textarea')

        assert value_element is not None, f"Could not find value for question: {row['field']}"

        expected_label = row['field'].upper()
        expected_value = row['value'].upper()
        actual_value = value_element.get_attribute('value').upper()
        actual_label = label_element.text.upper()

        assert actual_label == expected_label, f"Expected label: {expected_label} - Actual value:{actual_label}"
        assert actual_value == expected_value, f"Expected value: {expected_value} - Actual value:{actual_value}"


def assert_four_column_table(table, root_element):
    QUESTION_COL_KEY = 0
    COL_TWO_KEY = 1
    COL_THREE_KEY = 2
    COL_FOUR_KEY = 3

    def assert_cell(element, question, expected_value):
        value = element.get_attribute("value")
        assert value == expected_value, f"Question: {question} - Expected: {expected_value} - Actual: {value}"

    for row in table:
        question = row[QUESTION_COL_KEY]
        label_element = root_element.find_element_by_xpath(f".//*[text()='{question}']")
        assert label_element is not None, f"Could not find question on legal help form: {question}"
        parent_element = label_element.find_element_by_xpath("./..//ancestor::tr")
        elements = parent_element.find_elements_by_tag_name("td input")

        assert_cell(elements[0], question, row[COL_TWO_KEY])
        if len(row) > 2 and row[COL_THREE_KEY].lower() != 'n/a':
            assert_cell(elements[1], question, row[COL_THREE_KEY])
        if len(row) > 3 and row[COL_FOUR_KEY].lower() != 'n/a':
            assert_cell(elements[2], question, row[COL_FOUR_KEY])


@given(u'The legal help form Your details section has the values')
def step_impl(context):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element_by_xpath(f"//h2[text()='Your Details']")
    wrapper_element = heading_element.find_element_by_xpath("./..")
    assert_your_details(context.table, wrapper_element)

@given(u'The legal help form "{section_heading}" section has the values')
def step_imple(context, section_heading):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element_by_xpath(f"//h2[text()='{section_heading}']")
    wrapper_element = heading_element.find_element_by_xpath("./..")
    assert_four_column_table(context.table, wrapper_element)


@given(u'The legal help form Your Income section (less Monthly allowances) has the values')
def step_impl(context):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element_by_xpath(f"//h2[text()='Your Income']")
    wrapper_element = heading_element.find_element_by_xpath("./..")
    sub_heading_element = wrapper_element.find_element_by_xpath(".//*[text()='Less monthly allowances']")
    wrapper_element = sub_heading_element.find_element_by_xpath("./..//ancestor::table")
    assert_four_column_table(context.table, wrapper_element)

     
@when(u'I select Finances')
def step_impl(context):
    tabs = context.helperfunc.find_by_css_selector("ul.Tabs")
    finance_tab_link = tabs.find_element_by_link_text("Finances")
    assert finance_tab_link is not None

    # click on the link
    finance_tab_link.click()

@then(u'I can view the financial assessment entered by the Operator')
def step_impl(context):
    tabs = context.helperfunc.find_by_css_selector("ul.Tabs")
    finance_tab_link = tabs.find_element_by_link_text("Finances")
    classes = finance_tab_link.get_attribute("class")
    # Checking that the green tick is present for having the finance previously completed.
    assert "Icon--solidTick" in classes and "Icon--green" in classes
    # Checking that the overall form has loaded by checking one of the elements are there.
    assert context.helperfunc.find_by_id("id_your_details-has_partner_1") is not None
    
