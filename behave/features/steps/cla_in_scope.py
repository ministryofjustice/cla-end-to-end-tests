from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from features.constants import CLA_PUBLIC_URL
# change to allow commit to reset main
def assert_header_on_page(title, context):
    heading = context.helperfunc.find_by_xpath('//h1')
    assert heading is not None
    assert heading.text == title
    
def wait_until_page_is_loaded(path, context):
    def do_test(*args):
        return context.helperfunc.get_current_path() == path
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(do_test)
     
@given(u'I have selected the start now button on the start page')
def step_start_page(context):
    start_page_url = f"{CLA_PUBLIC_URL}"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Check if you can get legal aid", context)
    start_button = context.helperfunc.find_by_id('start')
    assert start_button is not None
    assert start_button.text == "Start now"
    start_button.click()

@given(u'I am on the scope diagnosis page')
def step_scope_page(context):
    wait_until_page_is_loaded("/scope/diagnosis/", context)
    assert_header_on_page("Choose the area you most need help with", context)
    
@when(u'I select the category Education')
def step_select_category_education(context):
    education_link = context.helperfunc.find_by_xpath('//a[@title="Education"]')
    next_page_path = education_link.get_attribute("pathname")
    assert education_link is not None
    education_link.click()    
    wait_until_page_is_loaded(next_page_path, context)

@when(u'the category Special Educational needs')
def step_select_category_special_educational_needs(context):
    assert_header_on_page("What is your education problem about?", context)
    special_education_link = context.helperfunc.find_by_xpath('//a[@title="Special educational needs"]')
    assert special_education_link is not None    
    special_education_link.click()

@then(u'I am taken to the Legal aid is available for this type of problem page')
def step_on_legal_aid_is_available_page(context):
    wait_until_page_is_loaded ("/legal-aid-available", context)
    assert_header_on_page("Legal aid is available for this type of problem", context)