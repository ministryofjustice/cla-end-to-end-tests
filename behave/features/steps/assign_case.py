from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from features.constants import MATTER_TYPE_1, MATTER_TYPE_2, CLA_FRONTEND_URL


@given("case notes are empty")
def step_impl(context):
    notes = context.helperfunc.find_by_name("case.notes")
    assert len(notes.text) == 0


@step("I have created a user")
def step_impl(context):
    context.execute_steps(
        """
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    """
    )


@step("I have created a valid discrimination scope")
def step_impl(context):
    context.execute_steps(
        """
        When I select ‘Create Scope Diagnosis'
        And I select the diagnosis <category> and click next <number> times
        | category                                                | number |
        | Discrimination                                          | 2      |
        | Direct discrimination                                   | 1      |
        | Disability                                              | 1      |
        | Work                                                    | 1      |
        Then I get an "INSCOPE" decision
        And select 'Create financial assessment'
    """
    )


@given("I am on the Diversity tab")
def step_impl(context):
    def wait_until_finance_is_complete(*args):
        # this waits until all the finance questions have been answered
        classes = (
            context.helperfunc.find_by_css_selector("ul.Tabs")
            .find_element_by_link_text("Finances")
            .get_attribute("class")
        )
        return "Icon--solidTick" in classes and "Icon--green" in classes

    # first need to complete the finances tab
    context.execute_steps(
        """
        Given I am taken to the Finances tab with the ‘Details’ sub-tab preselected
        And I do not have a partner
        And I am aged 60 or over
        And I <answer> to Details <question>
          | question                                          | answer |
          | Universal credit                                  | No     |
          | Income Support                                    | No     |
          | Income-based Job Seekers Allowance                | No     |
          | Guarantee State Pension Credit                    | Yes    |
          | Income-related Employment and Support Allowance   | No     |
        Then I move onto Finances inner-tab
        And I <answer> to Finances <question>
          | question                                              | answer |
          | How much was in your bank account/building society    | 0.00   |
          | Do you have any investments, shares or ISAs?          | 0.00   |
          | Do you have any valuable items worth over £500 each?  | 0.00   |
          | Do you have any money owed to you?                    | 0.00   |
        And I select Save assessment
        And the 'Diversity' and 'Assign' tabs become available
    """
    )

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_finance_is_complete)
    context.helperfunc.find_by_partial_link_text("Diversity").click()
    assert (
        "Gender"
        in context.helperfunc.find_by_css_selector(
            "h2[class='FormBlock-label ng-binding']"
        ).text
    )


@when("I select 'Prefer not say' for all diversity questions")
def step_impl(context):
    page = context.helperfunc
    radio = page.find_by_css_selector("input[name='gender'][value='Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='ethnicity'][value='Prefer not to say']"
    )
    assert (
        "Ethnic origin"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()
    # We need o either locate a new element that is not currently on the page
    # OR do an explicit wait, gone with find a new element that wasn't previously on the page
    radio = page.find_by_css_selector(
        "input[name='disability'][value='PNS - Prefer not to say']"
    )
    assert (
        "Disabilities"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='religion'][value='Prefer not to say']"
    )
    assert (
        "Religion / belief"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='sexual_orientation'][value='Prefer Not To Say']"
    )
    assert (
        "Sexual orientation"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-save").click()

    def wait_until_diversity_is_complete(*args):
        try:
            return (
                "The client has completed diversity monitoring."
                in page.find_by_class("SummaryBlock").text
            )
        except StaleElementReferenceException:
            return False

    wait = WebDriverWait(page.driver(), 10)
    wait.until(wait_until_diversity_is_complete)


@when("select the Assign tab")
def step_impl(context):
    context.helperfunc.find_by_partial_link_text("Assign").click()


@then('I get a message with the text "Case notes must be added to close a case"')
def step_impl(context):
    alert = context.helperfunc.find_by_css_selector("div[class='modal-dialog '")
    assert "Case notes must be added to close a case" in alert.text


@given('I enter the case notes "{case_notes_text}"')
def step_impl_case_notes(context, case_notes_text):
    notes = context.helperfunc.find_by_name("case.notes")
    # Focus on element first
    notes.click()
    notes.send_keys(case_notes_text)
    assert notes.get_attribute("value") == case_notes_text


@when("I select a category from Matter Type 1")
def step_impl_matter_type1(context):
    # Find matter type 1 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector("#s2id_matter_type1")
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_1}']").click()
    assert (
        element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_1
    )


@when("I select a category from Matter Type 2")
def step_impl_matter_type2(context):
    # Find matter type 2 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector("#s2id_matter_type2")
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_2}']").click()
    assert (
        element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_2
    )


@when("there is only one provider")
def step_impl_one_provider(context):
    form = context.helperfunc.find_by_name("assign_provider_form")

    # Providers are loaded via ajax after clicking the assign tab
    def wait_for_assign_providers_to_load(*args):
        return form.find_element_by_css_selector("div.ContactBlock") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_assign_providers_to_load)

    # Find matter type 2 wrapper and focus on it
    headings = form.find_elements_by_css_selector("h2.ContactBlock-heading")
    context.provider_selected = headings[0].text
    assert len(headings) == 1


@when("I select 'Assign Provider'")
def step_impl_assign_provider(context):
    context.case_id = context.helperfunc.find_by_css_selector(".CaseBar-caseNum a").text
    context.helperfunc.find_by_name("assign-provider").click()


@then("the case is assigned to the Specialist Provider")
def step_impl_case_assigned(context):
    def wait_until_case_is_assigned(*args):
        element = context.helperfunc.find_by_css_selector(
            ".NoticeContainer--fixed li.Notice"
        )
        return (
            element is not None
            and element.text
            == f"Case {context.case_id} assigned to {context.provider_selected}"
        )

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_case_is_assigned)


@then("the case does not show up on the call centre dashboard")
def step_impl_case_removed_from_list(context):
    dashboard_url = f"{CLA_FRONTEND_URL}/call_centre/?ordering=-modified&page=1"
    context.helperfunc.open(dashboard_url)

    def wait_until_dashboard_page_is_loaded(*args):
        try:
            table = context.helperfunc.driver().find_element_by_css_selector(
                ".ListTable"
            )
            return context.case_id not in table.text
        except Exception:
            return False

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_dashboard_page_is_loaded)
