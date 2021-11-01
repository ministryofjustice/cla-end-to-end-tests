from behave import *
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
    radio_input = context.helperfunc.find_by_css_selector("input[name='your_details-specific_benefits-universal_credit'][value='false']")
    assert radio_input is not None
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"

@when(u'I move onto Finances tab')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I move onto Finances tab')


@when(u'I have no savings in the bank')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I have no savings in the bank')


@when(u'I have no investments, shares or ISAs')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I have no investments, shares or ISAs')


@when(u'I have no valuable items worth over £500 each')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I have no valuable items worth over £500 each')


@when(u'I have no money owed to me')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I have no money owed to me')


@when(u'I select Save assessment')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I select Save assessment')


@then(u'I am given a message \'The means test has been saved. The current result is eligible for Legal Aid\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I am given a message \'The means test has been saved. The current result is eligible for Legal Aid\'')


@then(u'the \'Diversity\' and \'Assign\' tabs become available')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the \'Diversity\' and \'Assign\' tabs become available')
