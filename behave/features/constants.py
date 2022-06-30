import os

BROWSER = os.environ.get("BROWSER")
ARTIFACTS_DIRECTORY = os.environ.get("ARTIFACTS_DIRECTORY")

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

CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP = {
    "FULL": {
    "full_name": "Test Dummy User",
    "postcode": "SW1H 9AJ",
    "street": "102 Petty France",
    "mobile_phone": "020 3334 3555",
    "email": "102pettyfrance@digital.justice.gov.uk",
    "dob_day": "1",
    "dob_month": "1",
    "dob_year": "1990",
    "ni_number": "PA102030F",
    "adaptations": "No adaptations required",
    "media_code": "Don't Know",
    "source": "Phone"
    },
    "LIMITED": {
    "full_name": "Rey Skywalker incomplete details",
    "postcode": "",
    "street": "102 Petty France",
    "mobile_phone": "",
    "email": "102pettyfrance@digital.justice.gov.uk",
    "dob_day": "1",
    "dob_month": "1",
    "dob_year": "1990",
    "ni_number": "PA102030F",
    "adaptations": "No adaptations required",
    "media_code": "Don't Know",
    "source": "Phone"
    }
}

CLA_MEANS_TEST_PERSONAL_DETAILS_FORM = {
    "full_name": {"form_element_id": "full_name", "form_element_value": "John Smith"},
    "postcode": {"form_element_id": "address-post_code", "form_element_value": "SW1H 9AJ"},
    "street": {"form_element_id": "address-street_address", "form_element_value": "102 Petty France"},
    "email": {"form_element_id": "email", "form_element_value": "test@digital.justice.gov.uk"},
}
CLA_MEANS_TEST_CALL_BACK_NUMBER = {   
    "mobile_phone": {"form_element_id": "callback-contact_number", "form_element_value": "020 1234 67890"}}

MATTER_TYPE_1 = "QEMP - Employment"
MATTER_TYPE_2 = "QDIS - Disability"

CLA_SPECIALIST_PROVIDERS_NAME = "Howells"
CLA_SPECIALIST_CASE_TO_ACCEPT = "JT-4272-9443"
# THESE ARE CASES FROM TEXT FIXTURE test_callbacks.json
CLA_CALLBACK_CASES = ["TC-0001-0001",
                      "TC-0001-0002",
                      "TC-0001-0003",
                      "TC-0001-0004",
                      "TC-0001-0005"]

# This is so we can check personal details against the backend (LH block on diagnosis page)
CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK = {
    "Full name": {"form_element_type": "h2", "form_element_title": "Full name", "backend_id": "full_name"},
    "Telephone": {"form_element_type": "p", "form_element_title": "Phone number", "backend_id": "mobile_phone"},

}
# Used for P5 - first step checks to see if we can find cases for a particular test user
CLA_EXISTING_USER = "Obi-Wan Kenobi"
CLA_CASE_DETAILS_INNER_TAB = {"Details": 1,
                              "Finances": 2,
                              "Income": 3,
                              "Expenses": 4}
# P9 users for contact us options
ClA_CONTACT_US_USER = "Nathan Drake"
CLA_CONTACT_US_USER_PERSON_TO_CALL = "Elena Fisher"

MINIMUM_SLEEP_SECONDS = 2
