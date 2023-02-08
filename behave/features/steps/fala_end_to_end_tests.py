from helper.constants import CLA_FALA_URL, FALA_HEADER

from behave import step


@step("I am on the Find a legal aid adviser homepage")
def step_impl_homepage(context):
    homepage_url = f"{CLA_FALA_URL}"
    context.helperfunc.open(homepage_url)
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    assert title_xpath == FALA_HEADER


@step('I provide the "{location}" details')
def step_impl_input_location(context, location):
    input_id = context.helperfunc.find_by_id("id_postcode")
    input_id.send_keys(location)
    input_xpath = context.helperfunc.find_by_xpath('//input[@id="id_postcode"]')
    input_value = input_xpath.get_attribute("value")
    assert input_value == location


@step('I provide an organisation name "{organisation}"')
def step_impl_input_organisation(context, organisation):
    input_id = context.helperfunc.find_by_id("id_name")
    input_id.send_keys(organisation)
    input_xpath = context.helperfunc.find_by_xpath('//input[@id="id_name"]')
    input_value = input_xpath.get_attribute("value")
    assert input_value == organisation


@step("I select the 'search' button on the FALA homepage")
def step_impl_click_search(context):
    search_button = context.helperfunc.find_by_id("searchButton")
    assert search_button is not None
    search_button.click()


@step('I am taken to the page corresponding to "{location}" result')
def step_impl_result_page(context, location):
    current_url = context.helperfunc.driver().current_url
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//div[@class="search-results-container"]'
    )
    result_number_paragraph = context.helperfunc.find_by_xpath(
        '//p[@class="govuk-body"]'
    )
    location = location.replace(" ", "+")

    assert current_url == f"""{CLA_FALA_URL}/?postcode={location}&name=&search="""
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath, result_number_paragraph is not None


@step('I browse through the filter categories and select "{filter_label}"')
def step_impl_click_checkbox_filter(context, filter_label):
    checkbox_input = context.helperfunc.find_by_css_selector(
        f"input[type='checkbox'][value='{filter_label}']"
    )
    checkbox_input.click()
    assert checkbox_input.get_attribute("checked") == "true"


@step("I select the 'Apply filter' button")
def step_impl_apply_filter(context):
    apply_filter_button = context.helperfunc.find_by_name("filter")
    assert apply_filter_button is not None
    apply_filter_button.click()


@step(
    'the result page containing "{location}" is updated to apply the filter "{filter_label}"'
)
def step_impl_update_result_page(context, location, filter_label):
    current_url = context.helperfunc.driver().current_url
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//div[@class="search-results-container"]'
    )
    updated_result_number_paragraph = context.helperfunc.find_by_xpath(
        '//p[@class="govuk-body"]'
    )
    location = location.replace(" ", "+")

    assert (
        current_url
        == f"""{CLA_FALA_URL}/?postcode={location}&name=&categories={filter_label}&filter="""
    )
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath is not None
    assert updated_result_number_paragraph is not None


@step("the page shows an error")
def step_impl_error_shown_on_page(context):
    alert = context.helperfunc.find_by_css_selector(".alert-message")
    assert alert is not None
    assert (
        alert.text == "No results\nThere are no results matching your search criteria."
    )


@step(
    'I am taken to the page corresponding to the "{location}" "{organisation}" search result'
)
def step_impl_result_page_with_multi_params(context, location, organisation):
    result_number_paragraph = context.helperfunc.find_by_xpath(
        '//p[@class="govuk-body"]'
    )
    current_url = context.helperfunc.driver().current_url
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//div[@class="search-results-container"]'
    )
    organisation = organisation.replace(" ", "+")
    location = location.replace(" ", "+")

    assert (
        current_url
        == f"""{CLA_FALA_URL}/?postcode={location}&name={organisation}&search="""
    )
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath, result_number_paragraph is not None


@step('"{count}" result is visible on the results page')
def step_impl_count_results_visible_on_results_page(context, count):
    count = int(count)
    listitems = context.helperfunc.find_many_by_xpath(
        "//main/div/div[3]/div[1]/section/div/div[2]/div/ul/li"
    )
    assert listitems is not None
    list_count = len(listitems)
    assert list_count == count
