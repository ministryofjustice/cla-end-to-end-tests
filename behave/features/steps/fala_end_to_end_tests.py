from helper.constants import CLA_FALA_URL

from behave import step


@step("I am on the Find a legal aid adviser homepage")
def step_impl_homepage(context):
    homepage_url = f"{CLA_FALA_URL}"
    context.helperfunc.open(homepage_url)
    title_xpath = context.helperfunc.find_by_xpath("//html/body/div/main/div/div/h1")
    assert title_xpath is not None
    strip_text = title_xpath.text.replace("\n", " ")
    assert strip_text, "Find a legal aid adviser or family mediator"


@step('I provide the "{location}" details')
def step_impl_input_location(context, location):
    input_id = context.helperfunc.find_by_id("id_postcode")
    input_id.send_keys(location)
    input_xpath = context.helperfunc.find_by_xpath(
        '//main/div/div[@class="find-legal-adviser"]/div/form/div/div/div/input[@id="id_postcode"]'
    )
    assert input_xpath.get_attribute("value"), location


@step("I select the 'search' button on the FALA homepage")
def step_impl_click_search(context):
    search_button = context.helperfunc.find_by_id("searchButton")
    assert search_button is not None
    search_button.click()


@step("I am taken to the result page")
def step_impl_result_page(context, dynamic_location=True):
    result_url = f"""{CLA_FALA_URL}/?postcode={dynamic_location}+&name=&search="""
    assert result_url is not None
    title_xpath = context.helperfunc.find_by_xpath("//html/body/div/main/div/div/h1")
    result_container_xpath = context.helperfunc.find_by_xpath(
        '//html/body/div/main/div/div/div/section/div[@class="search-results-container"]'
    )
    assert title_xpath, result_container_xpath is not None

