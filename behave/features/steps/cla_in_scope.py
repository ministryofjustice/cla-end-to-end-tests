from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from features.constants import CLA_PUBLIC_URL

def assert_header_on_page(title, context):
    heading = context.helperfunc.find_by_xpath('//h1')
    assert heading is not None
    assert heading.text == title
    
def wait_until_page_is_loaded(path, context):
    def do_test(*args):
        return context.helperfunc.get_current_path() == path
    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(do_test)
     
# this is a shared step
@step(u'I am taken to the "{header}" page located on "{page}"')
def step_check_page(context, page, header):
    wait_until_page_is_loaded(page, context)
    assert_header_on_page(header, context)

# this is a shared step   
@step(u'I click continue')
def step_click_continue(context):
    # click on the continue button
    continue_button = context.helperfunc.find_by_id("submit-button")
    assert continue_button is not None
    continue_button.click()
        
@given(u'I have selected the start now button on the start page')
def step_start_page(context):
    start_page_url = f"{CLA_PUBLIC_URL}"
    context.helperfunc.open(start_page_url)
    assert_header_on_page("Check if you can get legal aid", context)
    start_button = context.helperfunc.find_by_id('start')
    assert start_button is not None
    assert start_button.text == "Start now"
    start_button.click()

    
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
    
@then(u'I click on the \'Check if you qualify financially\' button') 
def step_taken_to_about_page(context):
    check_if_you_qualify_link = context.helperfunc.find_by_xpath('//a[@href="/about"]')
    assert check_if_you_qualify_link is not None
    check_if_you_qualify_link.click()    

@then(u'I <answer> the <question>')
def step_impl_means_test(context):
    # answer tells me if I say yes or no
    # question helps me find the radio buttons
    for row in context.table:
        value = row['question']
        question_fieldset = context.helperfunc.find_by_xpath(f"//*[contains(text(),'{row['question']}')]")
        question_field_id = question_fieldset.get_attribute("id")
        question_radio_id_start = str(question_field_id).split('-')[2]
        if row['answer'] == 'No': 
            question_radio_id = question_radio_id_start + '-1'
        elif row['answer'] == 'Yes':
             question_radio_id = question_radio_id_start + '-0'
        else:
            raise ValueError(f"Can only process Yes or No answers. You entered {row['answer']}")
        # Find the parent of the legend so can look at it's children
        question_fieldset_parent = question_fieldset.find_element_by_xpath('..')
        # Need to look for the label not the radio input as that is what is clicked
        question_radio = context.helperfunc.driver().find_element_by_xpath(f"//input[@id='{question_radio_id}']")
        assert question_radio is not None, f"Could not find: {value}"
        question_radio.click()
        # check that the input is selected
        assert question_radio.get_attribute('checked') == 'true'