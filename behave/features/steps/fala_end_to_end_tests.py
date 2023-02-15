from helper.constants import CLA_FALA_URL, FALA_HEADER, MINIMUM_SLEEP_SECONDS
from behave import step
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


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
    input_value = input_id.get_attribute("value")
    assert input_value == location


@step('I provide an organisation name "{organisation}"')
def step_impl_input_organisation(context, organisation):
    input_id = context.helperfunc.find_by_id("id_name")
    input_id.send_keys(organisation)
    input_value = input_id.get_attribute("value")
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
    location_url_string = location.replace(" ", "+")
    expected_url = f"""{CLA_FALA_URL}/?postcode={location_url_string}&name=&search="""

    assert current_url == expected_url
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath is not None
    assert result_number_paragraph is not None


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
    location_url_string = location.replace(" ", "+")
    expected_url = f"""{CLA_FALA_URL}/?postcode={location_url_string}&name=&categories={filter_label}&filter="""

    assert current_url == expected_url
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath is not None
    assert updated_result_number_paragraph is not None


@step("the page shows an error")
def step_impl_error_shown_on_page(context):
    alert = context.helperfunc.find_by_css_selector(".alert-message")
    assert alert is not None
    expected_text = "No results\nThere are no results matching your search criteria."
    assert alert.text == expected_text


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
    organisation_url_string = organisation.replace(" ", "+")
    location_url_string = location.replace(" ", "+")
    expected_url = f"""{CLA_FALA_URL}/?postcode={location_url_string}&name={organisation_url_string}&search="""

    assert current_url == expected_url
    assert title_xpath == f"{FALA_HEADER}"
    assert result_container_xpath is not None
    assert result_number_paragraph is not None


@step("{count:d} result is visible on the results page")
def step_impl_count_results_visible_on_results_page(context, count):
    count = int(count)
    listitems = context.helperfunc.find_many_by_xpath("//ul[@Class='org-list']/li")
    assert listitems is not None
    list_count = len(listitems)
    assert list_count == count, f"actual count is {list_count}"


@step('I select the language "{language}" and select "{code_indicator}"')
def step_impl_select_language(context, language, code_indicator):
    def select_text(*args):
        Select(context.helperfunc.find_by_xpath("//select")).select_by_visible_text(
            f"{language}"
        )
        return True

    def check_first_option(*args):
        select_chosen_language = Select(
            context.helperfunc.find_by_xpath("//select")
        ).first_selected_option
        assert select_chosen_language.get_attribute("text") == f"{language}"
        assert select_chosen_language.get_attribute("value") == f"{code_indicator}"
        return True

    wait = WebDriverWait(context.helperfunc.driver(), MINIMUM_SLEEP_SECONDS)
    wait.until(select_text)

    wait = WebDriverWait(
        context.helperfunc.driver(),
        MINIMUM_SLEEP_SECONDS,
        ignored_exceptions=[StaleElementReferenceException],
    )
    wait.until(check_first_option)


@step(
    'the page is updated to "{code_indicator}" and title starts with "{title_text_starts_with}"'
)
def step_impl_translated(context, code_indicator, title_text_starts_with):
    updated_page = context.helperfunc.find_by_xpath("/html").get_attribute("lang")
    updated_title_gui = context.helperfunc.find_by_xpath(
        "//html/body/div/main/div/div/h1"
    ).text

    assert updated_page == f"{code_indicator}"
    assert updated_title_gui.startswith(f"{title_text_starts_with}")

    # find_code_indicator = context.helperfunc.find_by_xpath(f'/html').get_attribute('lang')
    # # find the xpath code
    # # find_code_indicator = context.helperfunc.find_by_xpath(f'//html[@lang="{code_indicator}')
    # # select the code and set the new xpath
    # # find the xpath language
    # create_new_current_path = context.helperfunc.get_current_path()
    # print(create_new_current_path + "\n")
    # # find_language_text = context.helperfunc.find_by_xpath(f'//select[contains(text(),"cy"')
    # find_language_text = context.helperfunc.find_by_xpath(f'//select').get_attribute('value')
    # # the code has to assert that it is truthy to the language
    # print(find_code_indicator + "\n")
    # print(find_language_text + "\n")
    # assert False, find_code_indicator
