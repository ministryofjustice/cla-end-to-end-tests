from behave import step
from selenium.webdriver.common.by import By


@step("I am on the Find a legal aid adviser homepage")
def step_impl_homepage(context):
    homepage_url = f"{CLA_FALA_URL}"
    context.helperfunc.open(homepage_url)
    # path = context.helperfunc.find_by_xpath(f"//html/body/div/main/div/div/h1")
    # assert path is not None
    # strip_text = path.text.replace("\n", " ")
    # assert strip_text, "Find a legal aid adviser or family mediator"


@step("I provide the {location} details")
def step_impl_input_location(context):
    for row in context.table:
        location = row["location"]
        assert location is not None
        # context.add_location(row["location"])
        # assert location
        # f"The {location} is set."


@step("I select the {search} button on the FALA homepage")
def step_impl_click_search(context, search):
    search_button = context.helperfunc.find_by_id("searchButton")
    assert search_button is not None
    context.helperfunc.click_button(By.ID, search_button)


@step("I am taken to the search page")
def step_impl_result_page(context):
    def result_url(search, endpoint):
        return f"""{CLA_FALA_URL}/{search.zone.strip("=")}{endpoint.lstrip("/")}"""
        # return f"""{CLA_FALA_URL}/{search.zone.strip("=")}{dynamic_location}+{endpoint.lstrip("/")}"""

    # {https://find-legal-advice.justice.gov.uk}/{?postcode=}{Nottingham}+{&name=&search=}
    # https://find-legal-advice.justice.gov.uk/?postcode=Nottingham+&name=&search=

    # result_page_url = context.helperfunc.get_current_path(
    #     CLA_FALA_URL, result_url(arg1=step, arg2=step)
    # )
    # This is a method
    # heading = assert_header_on_page()
    # result_page_global = step_check_page(context, result_page_url, heading)
    # check that google maps container is in the DOM.
    # only check one class, and that's the wrapper / main body class of google
    result_container = context.helperfunc.find_by_class(
        "legal-adviser-results",
        "search-results-container",
        "map",
        "search-results",
        "search-results-list",
        "org-title",
        "org-details",
    )

    assert result_container is not None
    # f"Check if {result_page_global} is visible on the page and that {result_container} match items individually."
