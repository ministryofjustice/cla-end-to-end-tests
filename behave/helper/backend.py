import requests
from constants import CLA_BACKEND_URL


class Backend:

    def __init__(self, zone):
        self.token = None
        self.zone = zone
        self.headers = {
            'Content-Type': 'application/json',
            "Accept": "*/*",
        }

    def url(self, endpoint):
        return f"{CLA_BACKEND_URL}/{self.zone.strip('/')}/{endpoint.strip('/')}"

    def authenticate(self, client_id, client_secret, username, password, grant_type="password"):
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "username": username,
            "password": password,
        }
        response = requests.post(f"{CLA_BACKEND_URL}/oauth2/access_token/", data=payload)

        print(f"{CLA_BACKEND_URL}/oauth2/access_token/")
        assert response.status_code == 200, "Could not login into backend"
        access_token = self.token = response.json()["access_token"]
        self.headers["Authorization"] = f"Bearer {access_token}"

    def get_case(self, case_reference):
        response = requests.get(self.url(f"/case/{case_reference}/"), headers=self.headers)
        assert response.status_code == 200, f"Could not get case {case_reference}"
        return response.json()

    def get_case_personal_details(self, case_reference):
        response = requests.get(self.url(f"/case/{case_reference}/personal_details"), headers=self.headers)
        assert response.status_code == 200, f"Could not get personal details for case {case_reference}"
        return response.json()
