import os

BROWSER = os.environ.get("BROWSER")
ARTIFACTS_DIRECTORY = os.environ.get("ARTIFACTS_DIRECTORY")
DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIRECTORY")
CLA_BACKEND_URL = os.environ.get("CLA_E2E_BACKEND_URL")
CLA_FRONTEND_URL = os.environ.get("CLA_E2E_FRONTEND_URL")
CLA_FRONTEND_CSV_URL = "/provider/csvupload/"
CLA_PUBLIC_URL = os.environ.get("CLA_E2E_PUBLIC_URL")
SELENIUM_WEB_DRIVER_URL = os.environ.get("CLA_E2E_SELENIUM_WEB_DRIVER_URL")
MINIMUM_WAIT_UNTIL_TIME = 10
CLA_NUMBER = "0345 345 4 345"
CALL_CENTRE_ZONE = {
    "client_id": os.environ.get("CALL_CENTRE_CLIENT_ID"),
    "client_secret": os.environ.get("CALL_CENTRE_SECRET_ID"),
    "grant_type": "password",
    "username": os.environ.get("CALL_CENTRE_TEST_USER"),
    "password": os.environ.get("CALL_CENTRE_TEST_USER")
}
USERS = {
    "CHS_GENERAL_USER": {"username": "test_operator",
                         "password": "test_operator",
                         "login_url": f"{CLA_FRONTEND_URL}/auth/login/",
                         "user_type": "OPERATOR",
                         "application": "FRONTEND"},
    "TEST_SPECIALIST_PROVIDER": {"username": "test_howells",
                                 "password": "test_howells",
                                 "login_url": f"{CLA_FRONTEND_URL}/auth/login/",
                                 "user_type": "SPECIALIST_PROVIDER",
                                 "application": "FRONTEND"},
    # whilst this user is said to be a general user, they are actually also in the superuser group on foxadmin
    "FOX_ADMIN_GENERAL_USER": {"username": "cla_admin",
                               "password": "cla_admin",
                               "login_url": f"{CLA_BACKEND_URL}/admin/login",
                               "user_type": "OPERATOR",
                               "application": "BACKEND"},
    "NEWLY_CREATED_OPERATOR": {"username": "elvis.presley",
                           "password": "rockandroll",
                           "login_url": f"{CLA_FRONTEND_URL}/auth/login/",
                           "user_type": "OPERATOR",
                           "application": "FRONTEND"},
}
# value_key is linked to NEWLY_CREATED_OPERATOR
FOX_ADMIN_FORM_FIELDS = {"username": {"label": "Username:", "value_key": "username"},
                          "password": {"label": "Password:", "value_key": "password"},
                          "password_confirmation": {"label": "Password confirmation:", "value_key": "password"}}

USER_HTML_TAGS = {
    "FRONTEND":
        {"form_identifier": "login_frm"},
    "BACKEND":
        {"form_identifier": "login-form"}
}
CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO = "test_staff"

CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK = 3

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
CLA_SPECIALIST_CASE_TO_REJECT = "FA-3465-9114"
CLA_SPECIALIST_CASE_TO_SPLIT = "C4-6754-5886"
CASE_SPLIT_TEXT = f"This case is split from {CLA_SPECIALIST_CASE_TO_SPLIT}"
CLA_SPECIALIST_CASE_BANNER_BUTTONS = {
    "Accept": "accept-case",
    "Reject": "reject-case",
    "Split": "split-case",
    "Close": "provider-close-case"
}
CLA_SPECIALIST_SPLIT_CASE_RADIO_OPTIONS = {
    "Internally to Howells": "true",
    "To operator for assignment": "false"
}
CLA_SPECIALIST_REJECTION_OUTCOME_CODES = {
    "MIS-OOS": "Misdiagnosed, out of scope"
}
CLA_SPECIALIST_CSV_UPLOAD_PATH = "/uploads/csvupload.csv"
CLA_SPECIALIST_CSV_UPLOAD_PATH_ERRORS = "/uploads/csvupload_errors.csv"
# Used for text fields or text areas that just need a random string entered.
LOREM_IPSUM_STRING = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus fringilla tincidunt consectetur."

# THESE ARE CASES FROM TEXT FIXTURE test_callbacks.json
CLA_CALLBACK_CASES = ["TC-0001-0001",
                      "TC-0001-0002",
                      "TC-0001-0003",
                      "TC-0001-0004",
                      "TC-0001-0005"]

ASSIGN_F2F_CASE = "AS-0001-0001"

# This is so we can check personal details against the backend (LH block on diagnosis page)
CLA_CASE_PERSONAL_DETAILS_BACKEND_CHECK = {
    "Full name": {"form_element_type": "h2", "form_element_title": "Full name", "backend_id": "full_name"},
    "Telephone": {"form_element_type": "p", "form_element_title": "Phone number", "backend_id": "mobile_phone"},

}
# Used for P5 - first step checks to see if we can find cases for a particular test user
CLA_EXISTING_USER = "Obi-Wan Kenobi"
# P9 users for contact us options
ClA_CONTACT_US_USER = "Nathan Drake"
CLA_CONTACT_US_USER_PERSON_TO_CALL = "Elena Fisher"

MINIMUM_SLEEP_SECONDS = 2

