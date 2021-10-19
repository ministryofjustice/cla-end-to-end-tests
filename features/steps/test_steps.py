from behave import *


@given(u'that I am logged in')
def step_impl(context):
    page = context.helperfunc.open('https://training.cases.civillegaladvice.service.gov.uk/call_centre/')
    form = page.find_by_name('login_frm')
    # raise NotImplementedError(u'STEP: Given that I am logged in')


@given(u'that I am on the \'call centre dashboard\' page.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given that I am on the \'call centre dashboard\' page.')


@when(u'I select to \'Create a case\'.')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I select to \'Create a case\'.')


@then(u'I am taken to the \'case details\' page.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I am taken to the \'case details\' page.')


@then(u'I select \'Create new user\'.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I select \'Create new user\'.')


@then(u'enter the client\'s personal details.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then enter the client\'s personal details.')


@then(u'I click the save button on the screen.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I click the save button on the screen.')


@then(u'I will see the users details.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I will see the users details.')