import os
CLA_BACKEND_URL = os.environ.get("CLA_E2E_BACKEND_URL")
CLA_FRONTEND_URL = os.environ.get("CLA_E2E_FRONTEND_URL")
CLA_PUBLIC_URL = os.environ.get("CLA_E2E_PUBLIC_URL")
SELENIUM_WEB_DRIVER_URL = os.environ.get("CLA_E2E_SELENIUM_WEB_DRIVER_URL")
CLA_NUMBER = "0345 345 4 345"
CALL_CENTRE_ZONE = {
    "client_id": os.environ.get("CALL_CENTRE_CLIENT_ID"),
    "client_secret": os.environ.get("CALL_CENTRE_SECRET_ID"),
    "grant_type": "password",
    "username": os.environ.get("CALL_CENTRE_TEST_USER"),
    "password": os.environ.get("CALL_CENTRE_TEST_USER")
}

CLA_FRONTEND_PERSONAL_DETAILS_FORM = {
    "full_name": "Bob Merchandise",
    "postcode": "SW1H 9AJ",
    "street": "102 Petty France\nLondon",
    "mobile_phone": "02031301123",
    "email": "test@digital.justice.gov.uk",
    "dob_day": "1",
    "dob_month": "1",
    "dob_year": "1990",
    "ni_number": "KB902094B",
    "adaptations": "No adaptations required",
    "media_code": "Don't Know",
    "source": "Phone"
}

MATTER_TYPE_1 = "QEMP - Employment"
MATTER_TYPE_2 = "QDIS - Disability"
