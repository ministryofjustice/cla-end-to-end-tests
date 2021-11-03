import time

from behave import *
from selenium.webdriver.common.action_chains import ActionChains
import re


@given(u'that I am on the case details page')
def step_impl(context):
    context.execute_steps(u'''
        Given I select to 'Create a case'
    ''')

@step(u'I am on the Finances tab with the ‘Details’ sub-tab preselected')
def step_impl(context):
    context.execute_steps(u'''
        When I select ‘Create Scope Diagnosis'
        And I select the categories Discrimination, Direct Discrimination, Disability, Work
        Then I get an INSCOPE decision
        And select 'Create financial assessment'
        Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected
    ''')

@when(u'I do not have a partner')
def step_impl(context):
    radio_input = context.helperfunc.find_by_css_selector("input[name='your_details-has_partner'][value='false']")
    assert radio_input is not None
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


@when(u'I am not aged 60 or over')
def step_impl(context):
    radio_input = context.helperfunc.find_by_css_selector("input[name='your_details-older_than_sixty'][value='false']")
    assert radio_input is not None
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"

@when(u'I am on universal credit benefits')
def step_impl(context):
    radio_input = context.helperfunc.find_by_css_selector("input[name='your_details-specific_benefits-universal_credit'][value='true']")
    assert radio_input is not None
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"

@when(u'I move onto Finances inner-tab')
def step_impl(context):
    page = context.helperfunc
    finance_inner_tab = page.find_by_xpath("//*[@id='pills-section-list']/li[2]")
    assert 'Finances' in finance_inner_tab.text
    actions = ActionChains(page.driver())
    actions.move_to_element(finance_inner_tab).perform()
    finance_inner_tab.click()
    active_inner_tab = context.helperfunc.find_by_class("Pills-pill.is-active") # Confirm finance inner tab is active
    assert "Finances" in active_inner_tab.text


@when(u'I have no savings in the bank')
def step_impl(context):
    label = "How much was in your bank account/building society before your last payment went in? "
    input = context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../input")
    assert input is not None
    input.send_keys('0')


@when(u'I have no investments, shares or ISAs')
def step_impl(context):
    label = "Do you have any investments, shares or ISAs? "
    input = context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../input")
    assert input is not None
    input.send_keys('0')

@when(u'I have no valuable items worth over £500 each')
def step_impl(context):
    label = "Do you have any valuable items worth over £500 each? "
    input = context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../input")
    assert input is not None
    input.send_keys('0')

@when(u'I have no money owed to me')
def step_impl(context):
    label = "Do you have any money owed to you? "
    input = context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../input")
    assert input is not None
    input.send_keys('0')

@when(u'I select Save assessment')
def step_impl(context):
    button = context.helperfunc.find_by_name("save-means-test")
    assert button is not None
    button.click()


@then(u'I am given a message \'The means test has been saved. The current result is eligible for Legal Aid\'')
def step_impl(context):
    element = context.helperfunc.find_by_css_selector(".Notice.Notice--closeable.success")
    assert element is not None
    message = 'The means test has been saved. The current result is eligible for Legal Aid'
    assert element.text == message


@then(u'the \'Diversity\' and \'Assign\' tabs become available')
def step_impl(context):
    # Get the parent element of diversity tab
    # Since it's an <a> tag and sits in a li element which is what gets enabled
    diversity_tab = context.helperfunc.find_by_xpath(f"//a[text()='Diversity']/..")
    assert 'is-disabled' not in diversity_tab.get_attribute("class")
    # Get the parent element of assign tab
    # Since it's an <a> tag and sits in a li element which is what gets enabled
    assign_tab = context.helperfunc.find_by_xpath(f"//a[text()='Assign']/..")
    assert 'is-disabled' not in assign_tab.get_attribute("class")
