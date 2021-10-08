import pdb
import requests
from pdb import Pdb

from behave import *
    

@given(u'I go to the cla backend status endpoint')
def step_impl(context):
    context.response = requests.get('http://clabackend:8000/status/')


@then(u'I am shown that the service is ready')
def step_impl(context):
    assert context.response.json()['db']['ready'] == True

@given(u'I go to the cla frontend status endpoint')
def step_impl(context):
    pdb.set_trace()
    context.response = requests.get('http://clafrontend:8000/status/status.json')