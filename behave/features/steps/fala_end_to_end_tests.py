from helper.constants import CLA_FALA_URL, FALA_HOMEPAGE_HEADER

from behave import step


@step("I am on the Find a legal aid adviser homepage")
def step_impl_homepage(context):
    homepage_url = f"{CLA_FALA_URL}"
    context.helperfunc.open(homepage_url)
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    assert title_xpath, f"{FALA_HOMEPAGE_HEADER}"


@step('I provide the "{location}" details')
def step_impl_input_location(context, location):
    input_id = context.helperfunc.find_by_id("id_postcode")
    input_id.send_keys(location)
    input_xpath = context.helperfunc.find_by_xpath('//input[@id="id_postcode"]')
    assert input_xpath.get_attribute("value"), location


@step("I select the 'search' button on the FALA homepage")
def step_impl_click_search(context):
    search_button = context.helperfunc.find_by_id("searchButton")
    assert search_button is not None
    search_button.click()


@step('I am taken to the page corresponding to "{location}" result')
def step_impl_result_page(context, location):
    current_path = context.helperfunc.get_current_path()
    title_xpath = context.helperfunc.find_by_xpath("//html/body/div/main/div/div/h1")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//div[@class="search-results-container"]'
    )
    result_number_paragraph = context.helperfunc.find_by_xpath(
        '//p[@class="govuk-body"]'
    )

    assert current_path, f"""{CLA_FALA_URL}/?postcode={location}+&name=&search="""
    assert title_xpath, f"{FALA_HOMEPAGE_HEADER}"
    assert result_container_xpath, result_number_paragraph is not None
