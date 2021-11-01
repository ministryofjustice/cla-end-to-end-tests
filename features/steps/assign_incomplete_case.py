from behave import *
from create_scope_helper import create_valid_discrimination_scope
from create_eligible_finances import create_eligible_finance


@given(u'case notes are empty')
def step_impl(context):
    notes = context.helperfunc.find_by_name('case.notes')
    assert len(notes.text) == 0


@step(u'I have created a user')
def step_impl(context):
    context.execute_steps(u'''
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    ''')


@given(u'I have created a valid discrimination scope')
def step_impl(context):
    create_valid_discrimination_scope(context)


@given(u'I am on the Diversity tab')
def step_impl(context):
    create_eligible_finance(context)


@when(u'I select \'Prefer not say\' for all diversity questions')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I select \'Prefer not say\' for all diversity questions')


@when(u'select the Assign tab')
def step_impl(context):
    raise NotImplementedError(u'STEP: When select the Assign tab')


@then(u'I get a message with the text "Case notes must be added to close a case"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get a message with the text "Case notes must be added to close a case"')