import requests

from behave import *
    

@given(u'I go to the cla backend status endpoint')
def step_impl(context):
    context.response = requests.get('http://clabackend:8000/status/')


@given(u'I go to the cla frontend status endpoint')
def step_impl(context):
    context.response_ready = requests.get('http://clafrontend:8000/status/ready')
    context.response_live = requests.get('http://clafrontend:8000/status/live')
    

@then(u'I am shown that the cla backend service is ready')
def step_impl(context):
    assert context.response.json()['db']['ready'] == True


@then(u'I am shown that the cla frontend service is ready')
def step_impl(context):
    assert context.response_ready.status_code == 200
    assert context.response_live.status_code == 200