import requests
from behave import step
from helper.constants import CLA_PUBLIC_URL, CLA_FRONTEND_URL, CLA_BACKEND_URL


@step('I go to the "{service}" status endpoint')
def step_impl_service_status_endpoint(context, service):
    if service == "cla backend":
        context.response = requests.get(f"{CLA_BACKEND_URL}/status/")
    elif service == "cla frontend":
        context.response_ready = requests.get(f"{CLA_FRONTEND_URL}/status/ready")
        context.response_live = requests.get(f"{CLA_FRONTEND_URL}/status/live")
    elif service == "cla public":
        context.response = requests.get(f"{CLA_PUBLIC_URL}/ping.json")


@step('I am shown that the "{service}" service is ready')
def step_impl_service_ready(context, service):
    if service == "cla backend":
        assert context.response.json()["db"]["ready"] is True
    elif service == "cla frontend":
        assert context.response_ready.status_code == 200
        assert context.response_live.status_code == 200
    elif service == "cla public":
        assert context.response.status_code == 200
