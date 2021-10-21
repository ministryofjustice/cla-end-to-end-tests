import requests

from behave import *
    

@given(u'I go to the "{service}" status endpoint')
def step_impl(context, service):
    if service == "cla backend":
        context.response = requests.get('http://clabackend:8000/status/')
    elif service == "cla frontend":
        context.response_ready = requests.get('http://clafrontend:8000/status/ready')
        context.response_live = requests.get('http://clafrontend:8000/status/live')
    elif service == "cla public":
        context.response = requests.get('http://clapublic:8000/ping.json')

@then(u'I am shown that the "{service}" service is ready')
def step_impl(context, service):
    if service == "cla backend":
        assert context.response.json()['db']['ready'] == True
    elif service == "cla frontend":
        assert context.response_ready.status_code == 200
        assert context.response_live.status_code == 200
    elif service == "cla public":
        assert context.response.status_code == 200
