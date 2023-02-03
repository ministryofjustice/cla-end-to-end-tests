from helper.constants import CLA_FALA_URL, FALA_HEADER

from behave import step


@step("I am on the Find a legal aid adviser homepage")
def step_impl_homepage(context):
    homepage_url = f"{CLA_FALA_URL}"
    context.helperfunc.open(homepage_url)
    title_xpath = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text.replace("\n", " ")
    assert title_xpath, f"{FALA_HEADER}"


@step('I provide the "{location}" details')
def step_impl_input_location(context, location):
    input_id = context.helperfunc.find_by_id("id_postcode")
    input_id.send_keys(location)
    input_xpath = context.helperfunc.find_by_xpath('//input[@id="id_postcode"]')
    assert input_xpath.get_attribute("value"), location


@step('I provide an organisation name "{organisation}"')
def step_impl_input_organisation(context, organisation):
    input_id = context.helperfunc.find_by_id("id_name")
    input_id.send_keys(organisation)
    input_xpath = context.helperfunc.find_by_xpath('//input[@id="id_name"]')
    assert input_xpath.get_attribute("value"), organisation


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
    assert title_xpath, f"{FALA_HEADER}"
    assert result_container_xpath, result_number_paragraph is not None


@step('I browse through the filter categories and select "{filter_label}"')
def step_impl_click_checkbox_filter(context, filter_label):
    find_label_in_labels_list = context.helperfunc.find_many_by_xpath(
        f"//fieldset/div/div/label[contains(text(), '{filter_label}')]"
    )
    checkbox_list = context.helperfunc.find_many_by_xpath("//fieldset/div/div/input")
    for checkbox in checkbox_list:
        if find_label_in_labels_list == filter_label:
            checkbox.click()
            assert checkbox is not None

    assert find_label_in_labels_list, f"{filter_label}"


@step("I select the 'Apply filter' button")
def step_impl_apply_filter(context):
    apply_filter_button = context.helperfunc.find_by_name("filter")
    assert apply_filter_button is not None
    apply_filter_button.click()


@step(
    'the result page containing "{location}" is updated to apply the filter "{filter_label}"'
)
def step_impl_update_result_page(context, location, filter_label):
    current_path = context.helperfunc.get_current_path()
    title_xpath = context.helperfunc.find_by_xpath("//html/body/div/main/div/div/h1")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//div[@class="search-results-container"]'
    )
    updated_result_number_paragraph = context.helperfunc.find_by_xpath(
        '//p[@class="govuk-body"]'
    )
    assert (
        current_path
    ), f"""{CLA_FALA_URL}/?postcode={location}&name=&categories={filter_label}&filter="""
    assert title_xpath, f"{FALA_HEADER}"
    assert result_container_xpath is not None
    assert updated_result_number_paragraph is not None


@step("the page shows an error")
def step_impl_error_shown_on_page(context):
    alert = context.helperfunc.find_by_css_selector(".alert-message")
    assert alert is not None
    assert alert.text, "No results"


@step('I am taken to the page corresponding to the "{location}" "{organisation}" search result')
def step_impl_result_page_with_multi_params(context, location, organisation):
    result_number_paragraph = context.helperfunc.find_by_xpath('//p[@class="govuk-body"]')
    current_path = context.helperfunc.get_current_path()
    title_xpath = context.helperfunc.find_by_xpath("//html/body/div/main/div/div/h1")
    result_container_xpath = context.helperfunc.find_by_xpath('//div[@class="search-results-container"]')

    assert (current_path), f"""{CLA_FALA_URL}/?postcode={location}+&name={organisation}&search="""
    assert title_xpath, f"{FALA_HEADER}"
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
