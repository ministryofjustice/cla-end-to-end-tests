import requests
from helper.constants import CLA_BACKEND_URL


class Backend:
    def __init__(self, zone):
        self.token = None
        self.zone = zone
        self.headers = {"Content-Type": "application/json", "Accept": "*/*"}

    def url(self, endpoint):
        # url needs to have the / on the end , do not remove
        return f"{CLA_BACKEND_URL}/{self.zone.strip('/')}/{endpoint.lstrip('/')}"

    def authenticate(
        self, client_id, client_secret, username, password, grant_type="password"
    ):
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "username": username,
            "password": password,
        }
        response = requests.post(
            f"{CLA_BACKEND_URL}/oauth2/access_token/", data=payload
        )

        print(f"{CLA_BACKEND_URL}/oauth2/access_token/")
        assert response.status_code == 200, "Could not login into backend"
        access_token = self.token = response.json()["access_token"]
        self.headers["Authorization"] = f"Bearer {access_token}"

    def get_case(self, case_reference):
        response = requests.get(
            self.url(f"/case/{case_reference}/"), headers=self.headers
        )
        assert response.status_code == 200, f"Could not get case {case_reference}"
        return response.json()

    def get_case_personal_details(self, case_reference):
        response = requests.get(
            self.url(f"/case/{case_reference}/personal_details"), headers=self.headers
        )
        assert (
            response.status_code == 200
        ), f"Could not get personal details for case {case_reference}"
        return response.json()

    def get_case_callback_details(self, case_reference):
        response = requests.get(
            self.url(f"/case/{case_reference}/logs"), headers=self.headers
        )
        assert (
            response.status_code == 200
        ), f"Could not get logs for case {case_reference}"
        return response.json()

    def update_case_callback_details(self, case_reference, call_back_json):
        callback_url = self.url(f"/case/{case_reference}/call_me_back/")
        response = requests.post(
            url=callback_url, json=call_back_json, headers=self.headers
        )
        # if this fails then it might be because max no callbacks has been created
        # return a dict with details of the response
        if response.status_code == 204:
            response_json = None
        else:
            response_json = response.json()
        return {
            "response_status_code": response.status_code,
            "case_reference": case_reference,
            "call_back_json": call_back_json,
            "response_json": response_json,
        }

    def get_future_callbacks(self):
        response = requests.get(
            self.url("/case/future_callbacks/"), headers=self.headers
        )
        return response.json()
